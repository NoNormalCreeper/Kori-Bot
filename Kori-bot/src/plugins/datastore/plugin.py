""" 插件数据 """
import json
import os
import pickle
from pathlib import Path
from typing import IO, Any, Callable, Dict, Optional, TypeVar, Union, overload

import httpx
from nonebot.log import logger

from .config import plugin_config

_T = TypeVar("_T")


class Config:
    """插件配置管理"""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._data = {}
        if self._path.exists():
            self._load_config()
        else:
            self._save_config()

    def _load_config(self) -> None:
        """读取配置"""
        with self._path.open("r", encoding="utf8") as f:
            self._data = json.load(f)

    def _save_config(self) -> None:
        """保存配置"""
        with self._path.open("w", encoding="utf8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def _get(self, key: str) -> Any:
        """获取配置键值"""
        # TODO: 支持从数据库读取数据
        return self._data[key]

    @overload
    def get(self, __key: str) -> Union[Any, None]:
        ...

    @overload
    def get(self, __key: str, __default: _T) -> _T:
        ...

    def get(self, key, default=None):
        """获得配置

        如果配置获取失败则使用 `default` 值并保存
        如果不提供 `default` 默认返回 None
        """
        try:
            value = self._get(key)
        except:
            value = default
            # 保存默认配置
            self.set(key, value)
        return value

    def set(self, key: str, value: Any) -> None:
        """设置配置"""
        self._data[key] = value
        self._save_config()


class NetworkFile:
    """从网络获取文件

    暂时只支持 json 格式
    """

    def __init__(
        self,
        url: str,
        filename: str,
        plugin_data: "PluginData",
        process_data: Callable[[Dict], Dict] = None,
        cache: bool = False,
    ) -> None:
        self._url = url
        self._filename = filename
        self._plugin_data = plugin_data
        self._process_data = process_data
        self._cache = cache

        self._data = None

    async def load_from_network(self) -> Optional[Dict]:
        """从网络加载文件"""
        logger.info("正在从网络获取数据")
        async with httpx.AsyncClient() as client:
            r = await client.get(self._url, timeout=30)
            rjson = r.json()
            # 同时保存一份文件在本地，以后就不用从网络获取
            with self._plugin_data.open(
                self._filename,
                "w",
                encoding="utf8",
                cache=self._cache,
            ) as f:
                json.dump(rjson, f, ensure_ascii=False, indent=2)
            logger.info("已保存数据至本地")
            if self._process_data:
                rjson = self._process_data(rjson)
            return rjson

    def load_from_local(self) -> Optional[Dict]:
        """从本地获取数据"""
        logger.info("正在加载本地数据")
        if self._plugin_data.exists(self._filename):
            with self._plugin_data.open(
                self._filename,
                encoding="utf8",
                cache=self._cache,
            ) as f:
                data = json.load(f)
                if self._process_data:
                    data = self._process_data(data)
                return data

    @property
    async def data(self) -> Optional[Dict]:
        """数据

        先从本地加载，如果失败则从仓库加载
        """
        if not self._data:
            self._data = self.load_from_local()
        if not self._data:
            self._data = await self.load_from_network()
        return self._data

    async def update(self) -> None:
        """从网络更新数据"""
        self._data = await self.load_from_network()


class Singleton(type):
    """单例

    每个相同名称的插件数据只需要一个实例
    """

    _instances = {}

    def __call__(cls, name: str):
        if not cls._instances.get(name):
            cls._instances[name] = super().__call__(name)
        return cls._instances[name]


class PluginData(metaclass=Singleton):
    """插件数据管理

    将插件数据保存在 `data` 文件夹对应的目录下。
    提供保存和读取文件/数据的方法。
    """

    def __init__(self, name: str) -> None:
        # 插件名，用来确定插件的文件夹位置
        self._name = name

        # 插件配置
        self._config = None

        self.init_dir()

    def init_dir(self) -> None:
        """初始化目录"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)

    @property
    def cache_dir(self) -> Path:
        """缓存目录"""
        return plugin_config.datastore_cache_dir / self._name

    @property
    def config_dir(self) -> Path:
        """配置目录"""
        return plugin_config.datastore_config_dir

    @property
    def data_dir(self) -> Path:
        """数据目录"""
        return plugin_config.datastore_data_dir / self._name

    @property
    def config(self) -> Config:
        """获取配置管理"""
        if not self._config:
            self._config = Config(self.config_dir / f"{self._name}.json")
        return self._config

    def dump_pkl(self, data: Any, filename: str, cache: bool = False, **kwargs) -> None:
        with self.open(filename, "wb", cache=cache) as f:
            pickle.dump(data, f, **kwargs)

    def load_pkl(self, filename: str, cache: bool = False, **kwargs) -> Any:
        with self.open(filename, "rb", cache=cache) as f:
            data = pickle.load(f, **kwargs)
        return data

    def dump_json(
        self, data: Any, filename: str, cache: bool = False, **kwargs
    ) -> None:
        with self.open(filename, "w", cache=cache) as f:
            json.dump(data, f, **kwargs)

    def load_json(self, filename: str, cache: bool = False, **kwargs) -> Any:
        with self.open(filename, "r", cache=cache) as f:
            data = json.load(f, **kwargs)
        return data

    def open(self, filename: str, mode: str = "r", cache: bool = False, **kwargs) -> IO:
        """打开文件，默认打开数据文件夹下的文件"""
        path = self.cache_dir / filename if cache else self.data_dir / filename
        return open(path, mode, **kwargs)

    def exists(self, filename: str, cache: bool = False) -> bool:
        """判断文件是否存在，默认判断数据文件夹下的文件"""
        path = self.cache_dir / filename if cache else self.data_dir / filename
        return path.exists()

    def network_file(
        self,
        url: str,
        filename: str,
        process_data: Callable[[Dict], Dict] = None,
        cache: bool = False,
    ):
        """网络文件

        从网络上获取数据，并缓存至本地，仅支持 json 格式
        且可以在获取数据之后同时处理数据
        """
        return NetworkFile(url, filename, self, process_data, cache)

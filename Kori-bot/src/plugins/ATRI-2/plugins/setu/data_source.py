import asyncio
from random import choice
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request
from ATRI.config import Setu as ST
from .tf_dealer import detect_image


LOLICON_URL = "https://api.lolicon.app/setu/v2"
DEFAULT_SETU = (
    "https://i.pixiv.cat/img-original/img/2021/02/28/22/44/49/88124144_p0.jpg"
)


class Setu(Service):
    def __init__(self):
        Service.__init__(self, "涩图", "hso!", rule=is_in_service("涩图"))

    @staticmethod
    def _use_proxy(url: str) -> str:
        if ST.reverse_proxy:
            return url.replace("i.pixiv.cat", ST.reverse_proxy_domain)
        else:
            return url

    @classmethod
    async def random_setu(cls) -> tuple:
        """
        随机涩图.
        """
        res = await request.get(LOLICON_URL)
        data: dict = res.json()
        temp_data: dict = data.get("data", [])
        if not temp_data:
            return "涩批爬", None

        data: dict = temp_data[0]
        title = data.get("title", "木陰のねこ")
        p_id = data.get("pid", 88124144)
        url: str = data["urls"].get("original", "ignore")

        setu = MessageSegment.image(cls._use_proxy(url), timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @classmethod
    async def tag_setu(cls, tag: str) -> tuple:
        """
        指定tag涩图.
        """
        url = f"{LOLICON_URL}?tag={tag}"
        res = await request.get(url)
        data: dict = res.json()

        temp_data: dict = data.get("data", [])
        if not temp_data:
            return f"没有 {tag} 的涩图呢...", None

        data = temp_data[0]
        title = data.get("title", "木陰のねこ")
        p_id = data.get("pid", 88124144)
        url = data["urls"].get(
            "original",
            cls._use_proxy(DEFAULT_SETU),
        )
        setu = MessageSegment.image(url, timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @staticmethod
    async def detecter(url: str, file_size: int) -> list:
        """
        涩值检测.
        """
        data = await detect_image(url, file_size)
        return data

    @classmethod
    async def scheduler(cls) -> str:
        """
        每隔指定时间随机抽取一个群发送涩图.
        格式：
            是{tag}哦~❤
            {setu}
        """
        res = await request.get(LOLICON_URL)
        data: dict = res.json()
        temp_data: dict = data.get("data", [])
        if not temp_data:
            return ""

        tag = choice(temp_data.get("tags", ["女孩子"]))

        url = temp_data[0]["urls"].get(
            "original",
            cls._use_proxy(DEFAULT_SETU),
        )
        setu = MessageSegment.image(url, timeout=114514)
        return f"是{tag}哦~❤\n{setu}"

    @staticmethod
    async def async_recall(bot: Bot, event_id):
        await asyncio.sleep(30)
        await bot.delete_msg(message_id=event_id)

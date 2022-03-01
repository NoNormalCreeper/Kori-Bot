from pathlib import Path
import nonebot
from nonebot.drivers import Driver
from datetime import datetime
import asyncio
from nonebot.matcher import matchers

try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: Driver = nonebot.get_driver()

DATA_PATH = driver.config.statistical_path if driver.config.statistical_path else 'data/statistical/'
BLACK_LIST = driver.config.statistical_black_model if driver.config.statistical_black_model else []
BLACK_PRIORITY = driver.config.statistical_black_priority if driver.config.statistical_black_priority else []

DATA_PATH = str(Path(DATA_PATH).absolute()) + '/'
# print(DATA_PATH)

statistics_group_file = Path(f'{DATA_PATH}/_prefix_group_count.json')
statistics_user_file = Path(f'{DATA_PATH}/_prefix_user_count.json')
plugin2cmd_file = Path(f'{DATA_PATH}/plugin2cmd.json')

statistics_user_file.parent.mkdir(exist_ok=True, parents=True)


def _init():
    return {
        'total_statistics': {
            'total': {},
        },
        'day_statistics': {
            'total': {},
        },
        'week_statistics': {
            'total': {},
        },
        'month_statistics': {
            'total': {},
        },
        'start_time': str(datetime.now().date()),
        'day_index': 0
    }


# 保存数据
def save_data(plugin2cmd_, _group_count_dict, _user_count_dict):
    global _prefix_group_count_dict, _prefix_user_count_dict, plugin2cmd
    if _group_count_dict:
        with open(statistics_group_file, 'w', encoding='utf8') as f:
            json.dump(_group_count_dict, f, indent=4, ensure_ascii=False)
        _prefix_group_count_dict = _group_count_dict
    if _user_count_dict:
        with open(statistics_user_file, 'w', encoding='utf8') as f:
            json.dump(_user_count_dict, f, ensure_ascii=False, indent=4)
        _prefix_user_count_dict = _user_count_dict
    if plugin2cmd_:
        with open(plugin2cmd_file, 'w', encoding='utf8') as f:
            json.dump(plugin2cmd_, f, indent=4, ensure_ascii=False)
        plugin2cmd = plugin2cmd_


try:
    with open(statistics_group_file, 'r', encoding='utf8') as f:
        _prefix_group_count_dict: dict = json.load(f)
except FileNotFoundError:
    _prefix_group_count_dict: dict = _init()

try:
    with open(statistics_user_file, 'r', encoding='utf8') as f:
        _prefix_user_count_dict: dict = json.load(f)
except FileNotFoundError:
    _prefix_user_count_dict: dict = _init()


# 检测cmd是否重复
def check_cmd_exists(cmd: str = None):
    global plugin2cmd
    _cmd_list = []
    for _plugin in plugin2cmd:
        if _plugin != 'white_list':
            if cmd:
                for _cmd in plugin2cmd[_plugin]['cmd']:
                    if cmd == _cmd:
                        raise ValueError(f'别名 {_cmd} 有重复，请修改文件后重新启动....')
            else:
                for _cmd in plugin2cmd[_plugin]['cmd']:
                    if str(_cmd) in _cmd_list:
                        print(_cmd)
                        raise ValueError(f'别名 {_cmd} 有重复，请修改文件后重新启动....')
                    _cmd_list.append(str(_cmd))
    return _cmd_list


# 替换显示关键字
def _replace_key():
    global _prefix_group_count_dict, _prefix_user_count_dict
    for data in [_prefix_group_count_dict, _prefix_user_count_dict]:
        for itype in list(data.keys()):
            if itype in ['start_time', 'day_index']:
                continue
            for key in list(data[itype].keys()):
                if itype in ['total_statistics', 'day_statistics'] or key == 'total':
                    for plugin_name in list(data[itype][key].keys()):
                        for plugin in list(plugin2cmd.keys()):
                            if plugin != 'white_list':
                                if plugin_name in plugin2cmd[plugin]['cmd']:
                                    if plugin_name != plugin2cmd[plugin]['cmd'][0]:
                                        data[itype][key][plugin2cmd[plugin]['cmd'][0]] = \
                                            data[itype][key][plugin_name]
                                        del data[itype][key][plugin_name]
                                    break
                else:
                    for day in list(data[itype][key].keys()):
                        for plugin_name in list(data[itype][key][day].keys()):
                            for plugin in list(plugin2cmd.keys()):
                                if plugin != 'white_list':
                                    if plugin_name in plugin2cmd[plugin]['cmd']:
                                        if plugin_name != plugin2cmd[plugin]['cmd'][0]:
                                            data[itype][key][day][plugin2cmd[plugin]['cmd'][0]] = \
                                                data[itype][key][day][plugin_name]
                                            del data[itype][key][day][plugin_name]
                                        break


# 重新加载数据...
def _reload_data(check_flag: bool = False):
    global plugin2cmd, _prefix_group_count_dict, _prefix_user_count_dict
    plugin2cmd = json.load(open(plugin2cmd_file, 'r', encoding='utf8'))
    if check_flag:
        check_cmd_exists()
        _replace_key()
        save_data(None, _prefix_group_count_dict, _prefix_user_count_dict)
        # print(_prefix_group_count_dict)
    else:
        with open(plugin2cmd_file, 'r', encoding='utf8') as f:
            plugin2cmd = json.load(f)
        with open(statistics_group_file, 'r', encoding='utf8') as f:
            _prefix_group_count_dict = json.load(f)
        with open(statistics_user_file, 'r', encoding='utf8') as f:
            _prefix_user_count_dict = json.load(f)
    # print(_prefix_group_count_dict)


try:
    with open(plugin2cmd_file, 'r', encoding='utf8') as f:
        plugin2cmd: dict = json.load(f)
    check_cmd_exists()
    _reload_data(True)
except FileNotFoundError:
    plugin2cmd = {'white_list': []}
    for priority in matchers:
        for matcher in matchers[priority]:
            module = matcher.module
            if module not in BLACK_LIST and priority not in BLACK_PRIORITY:
                plugin2cmd[module] = {'cmd': []}
    save_data(plugin2cmd, None, None)


# 重新加载数据...
async def reload_data(check_flag: bool = False):
    await asyncio.get_event_loop().run_in_executor(None, _reload_data, check_flag)


def get_plugin2cmd():
    return plugin2cmd


def get_prefix_user_count_dict():
    return _prefix_user_count_dict


def get_prefix_group_count_dict():
    return _prefix_group_count_dict


# 删除cmd
async def del_cmd(cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _del_cmd, cmd)


# 添加cmd
async def add_cmd(cmd: str, new_cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _add_cmd, cmd, new_cmd)


# 查找cmd
async def query_cmd(cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _query_cmd, cmd)


# 修改cmd顺序
async def update_cmd_priority(cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _update_cmd_priority, cmd)


# 添加显示白名单
async def add_white(cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _add_white, cmd)


# 删除显示白名单
async def del_white(cmd: str):
    return await asyncio.get_event_loop().run_in_executor(None, _del_white, cmd)


# 显示白名单
def show_white():
    return _show_white()


# 白名单所有cmd
def get_white_cmd():
    tmp = []
    for model in list(plugin2cmd.keys()):
        if model in plugin2cmd['white_list']:
            for cmd in plugin2cmd[model]['cmd']:
                tmp.append(cmd)
    return tmp


def _del_cmd(cmd: str):
    global plugin2cmd
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                if cmd == plugin2cmd[model]['cmd'][0]:
                    if len(plugin2cmd[model]['cmd']) < 2:
                        return False
                    tmp = plugin2cmd[model]['cmd'][1]
                    plugin2cmd[model]['cmd'][1] = plugin2cmd[model]['cmd'][0]
                    plugin2cmd[model]['cmd'][0] = tmp
                    _replace_key()
                    # await reload_data(True)
                plugin2cmd[model]['cmd'].remove(cmd)
                save_data(plugin2cmd, _prefix_group_count_dict, _prefix_user_count_dict)
                return True
    return False


def _add_cmd(cmd: str, new_cmd: str):
    global plugin2cmd
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                check_cmd_exists(new_cmd)
                plugin2cmd[model]['cmd'].append(new_cmd)
                save_data(plugin2cmd, None, None)
                return True
    return False


def _query_cmd(cmd: str):
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                return plugin2cmd[model]['cmd']
    return []


def _update_cmd_priority(cmd: str):
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                if cmd == plugin2cmd[model]['cmd'][0]:
                    return True
                index = plugin2cmd[model]['cmd'].index(cmd)
                tmp = plugin2cmd[model]['cmd'][index]
                plugin2cmd[model]['cmd'][index] = plugin2cmd[model]['cmd'][0]
                plugin2cmd[model]['cmd'][0] = tmp
                # print(plugin2cmd)
                _replace_key()
                save_data(plugin2cmd, _prefix_group_count_dict, _prefix_user_count_dict)
                return True
    return False


def _add_white(cmd: str):
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                if model not in plugin2cmd['white_list']:
                    plugin2cmd['white_list'].append(model)
                    save_data(plugin2cmd, None, None)
                return True
    return False


def _del_white(cmd: str):
    for model in plugin2cmd:
        if model != 'white_list':
            if cmd in plugin2cmd[model]['cmd']:
                if model in plugin2cmd['white_list']:
                    plugin2cmd['white_list'].remove(model)
                    print(plugin2cmd['white_list'])
                    save_data(plugin2cmd, None, None)
                return True
    return False


def _show_white():
    return plugin2cmd['white_list']

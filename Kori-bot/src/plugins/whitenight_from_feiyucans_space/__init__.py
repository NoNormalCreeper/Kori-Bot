import requests
from .config import Config
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import nonebot
from nonebot.adapters.onebot.v11 import Message
import time as timeplugin
import datetime


global_config = nonebot.get_driver().config
nonebot.logger.info(f"global_config:{global_config}")
plugin_config = Config(**global_config.dict())
nonebot.logger.info(f"plugin_config:{plugin_config}")
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler

def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())#去除imageUrl可能存在的不可见字符

async def whitenight():
    #global msg  # msg改成全局，方便在另一个函数中使用
    msg = await suijitu()
    '''
    for qq in plugin_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg))
'''
    if msg:
        for qq_group in plugin_config.read_qq_groups:
            await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg))# MessageEvent可以使用CQ发图片



async def suijitu():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d') + ' 0:00:00'
    now_timeArray = timeplugin.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    now_timeStamp = int(timeplugin.mktime(now_timeArray))
    #获取当前日期

    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=45858772&offset_dynamic_id=0&need_top=1&platform=web'
    headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    #获取最近十条动态数据


    getdata = eval(response.text)
    data = getdata["data"]
    cards = data["cards"]


    for count in range(len(cards)):
        #逐个筛选出标签符合条件的动态
        target = cards[count]
        desc = target['desc']
        timestamp = desc['timestamp']
        if timestamp < now_timeStamp:
            #判断动态是否为最新动态 若不是 则终止操作
            break
        timeArray = timeplugin.localtime(timestamp)
        posttime = timeplugin.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        card = json.loads(target['card'])
        item = card["item"]
        description = item["description"]
        if '#鲱鱼 今夜无眠#' in description:
            #判断标签是否符合条件
            pictures_array = item['pictures']
            pictures_count = len(pictures_array)
            initext = description+ "\n"+posttime+ "\nfrom bilibili:鲱鱼罐头app\n"
            for n in range(pictures_count):
                pic = pictures_array[n]
                initext = f'{initext}[CQ:image,file=' + pic['img_src'] + ']'
            return f"{initext}"
    

for index, time in enumerate(plugin_config.read_inform_time):
    nonebot.logger.info(f"id:{index},time:{time}")
    scheduler.add_job(whitenight, "cron", hour=22, minute=30, id=str(146487))
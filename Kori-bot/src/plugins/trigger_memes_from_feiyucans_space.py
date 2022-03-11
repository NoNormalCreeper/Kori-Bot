from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot import on_command
import time as timeplugin
import datetime
import requests
import json


feiyucan = on_command("feiyucan", aliases={'昨日最佳'})


@feiyucan.handle()
async def handle(bot: Bot, event: Event, matcher: Matcher):

    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=45858772&offset_dynamic_id=0&need_top=1&platform=web'
    headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    #获取最近十条动态数据


    getdata = eval(response.text)
    data = getdata["data"]
    cards = data["cards"]


    for count in range (0,len(cards)) :
        #逐个筛选出标签符合条件的动态
        target = cards[count]
        desc = target['desc']
        timestamp = desc['timestamp']
        timeArray = timeplugin.localtime(timestamp)
        posttime = timeplugin.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        card = json.loads(target['card'])
        item = card["item"]
        description = item["description"]
        if '#鲱鱼 昨日最佳#' in description :
            #判断标签是否符合条件
            pictures_array = item['pictures']
            pictures_count = len(pictures_array)
            initext = description+ "\n"+posttime+ "\nfrom bilibili:鲱鱼罐头app\n"
            for n in range (0,pictures_count) :
                pic = pictures_array[n]
                initext = initext+'[CQ:image,file='+pic['img_src']+']'
            pic_ti = f"{initext}"
            await feiyucan.finish(message=Message(pic_ti))

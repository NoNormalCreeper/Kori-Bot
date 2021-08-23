from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command, on_keyword
import time
import requests

# http://api.chengzhecheng.cn/api/lsjt/api.php

tih=on_command("tih")

nums=[str(x) for x in range(0,10)]

@tih.handle()
async def tih_handle(bot: Bot, event: Event, state: T_State):
    arg=str(event.get_message()).strip()
    if arg:
        req=requests.get("http://api.chengzhecheng.cn/api/lsjt/api.php?max="+str(arg))
    else:
        req=requests.get("http://api.chengzhecheng.cn/api/lsjt/api.php?max=6")
    
    txt=req.text
    ltxt=list(txt)
    txt=''

    for i in range(len(ltxt)-1):
        if ltxt[i]=='：':
            if (ltxt[i-1] in nums) and (ltxt[i-2] in nums):
                ltxt[i-3]='\n'
            else:
                ltxt[i-2]='\n'
    
    for i in ltxt:
        txt+=i

    result="【历史上的今天】\n"+(((txt.replace(" -"," - "))).replace('：','. '))

    await tih.send(result)

    print('2',333)
    print(('2',333))
    print('2'+333)
    print(('2'+333))
    
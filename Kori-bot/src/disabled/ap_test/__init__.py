from nonebot.permission import *
from nonebot.adapters.cqhttp.permission import PRIVATE
from nonebot.adapters import Bot, Event
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot import on_command, on_keyword
import datetime

# def checker():
#     async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
#         if 
#         if True:
#             #记住，返回值一定要是个bool类型的值！
#             return True
#     return Rule(_checker)

ap=on_keyword(keywords=["生","日",'快','happy','birthday','蛋糕','🍰','🎂','㊗','🎁','🎉'],permission=PRIVATE)

content='''这是一条自动回复。
程序检测到了你在祝福我生日快乐，
但我此时已经在学校上课了qwq
你的祝福我收到了，总之非常感谢你的祝福！'''

@ap.handle()
async def ap_handle(bot: Bot, event: Event, state: T_State):

    await ap.send(content)
    
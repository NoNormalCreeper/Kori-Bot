from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.matcher import Matcher
from nonebot import on_command
# import requests
import json
# import get_answer as ga
from .get_answer import *


tellme = on_command("tellme")

@tellme.handle()
async def tellme_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State(), arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    # print(("args:",arg))
    result = get_tellme(arg)

    await tellme.send(('[Result]\n'+result))


calc = on_command("calc", aliases={'计算'})

@calc.handle()
async def calc_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State(), arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    try:
        result = get_calc(arg)
        await calc.send(MessageSegment.image(result))
    except Exception as e:
        await calc.send(str(e))
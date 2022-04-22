from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.matcher import Matcher
from nonebot import on_command
import json
from .get_answer import *


tellme = on_command("tellme")

@tellme.handle()
async def tellme_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State(), arg: Message = CommandArg()):
    try:
        arg = arg.extract_plain_text().strip()
        if not arg:
            await calc.finish("[错误]\n你的问题呢？")

        result = get_tellme(arg)
        await tellme.send(('[计算结果]\n'+result))
    except Exception as e:
        await tellme.send(('[错误]\n'+str(e)))


calc = on_command("calc", aliases={'计算'})

@calc.handle()
async def calc_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State(), arg: Message = CommandArg()):
    try:
        arg = arg.extract_plain_text().strip()
        if not arg:
            await calc.finish("[错误]\n你的问题呢？")
        result = get_calc(arg)
        await calc.send(MessageSegment.image(result))
    except Exception as e:
        await calc.send(f"[错误]\n{str(e)}")
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.matcher import Matcher
from nonebot import on_command, get_bot
# import requests
import json


test = on_command("test")

@test.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, arg: Message = CommandArg(), state: T_State = State()):
    arg = arg.extract_plain_text().strip()

    if arg == "1":
        msg = (f"大家好，我是 SB[CQ:xml,data=<?xml version='1.0' encoding='UTF-8' ?><msg serviceID=\"104\" templateID=\"1\" brief=\"大家好，我是 SB\"><item layout=\"2\"><picture cover=\"\" /><title>新人入群</title></item><source /></msg>,resid=104]")
        await test.send(message=Message(msg))

    if "tts" in arg:
        text = arg.replace("tts", "").strip()
        await test.send(Message('[CQ:tts,text=0]'.format(text)))

    # await test.finish("Unkown arguement(s)!")


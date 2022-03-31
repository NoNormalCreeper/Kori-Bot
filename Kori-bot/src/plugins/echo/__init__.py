#{"author":"HornCopper","version":"v1.0","name":"echo","admin":"10","aliases":"无","desc":"让机器人发送指定内容。$纯文本：+echo <message>$CQ码：+say <cqcode>"}!
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.matcher import Matcher
import sys
sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
from tools.permission import checker, error

from functools import reduce
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    unescape,
)


echo = on_command("echo")


@echo.handle()
async def echo_(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),9):
        await echo.finish(args)
    else:
        await echo.finish(error(9))


say = on_command("say")


@say.handle()
async def say_(matcher: Matcher, event: Event, args: Message = CommandArg()): 
    def _unescape(message: Message, segment: MessageSegment):
        if segment.is_text():
            return message.append(unescape(str(segment)))
        return message.append(segment)
    if checker(str(event.user_id),9):
        message = reduce(_unescape, args, Message())
        await say.finish(message)
    else:
        await say.finish(error(9))

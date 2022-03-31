#{"author":"HornCopper","version":"v1.0","name":"公告/API调用","admin":"仅Owner(3349104868)","aliases":"sign=公告$call_api=api","desc":"无"}!
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from aiocqhttp import MessageSegment as ms
import json

import sys
sys.path.append("..")
from .tools.permission import checker, error
import sys
sys.path.append("..")
from .tools.http_ import get_url

sign = on_command("sign",aliases={"公告"})

@sign.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    if str(event.user_id) == "3349104868" or str(event.user_id) == "2560359315":
        groups = await bot.call_api("get_group_list")
        for i in groups:
            await bot.call_api("send_group_msg",group_id=i["group_id"],message=f"[开发者全域公告]{cmd}")
    else:
        await sign.finish(f"啊咧，权限不够哦，这个命令只能由Owner(3349104868、2560359315)执行哦~")
        
call_api = on_command("call_api",aliases={"api"})
@call_api.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    if str(event.user_id) == "3349104868" or str(event.user_id) == "2560359315":
        await get_url(f"http://127.0.0.1:2334/{cmd}",300)
    else:
        await sign.finish(f"啊咧，权限不够哦，这个命令只能由Owner(3349104868、2560359315)执行哦~")

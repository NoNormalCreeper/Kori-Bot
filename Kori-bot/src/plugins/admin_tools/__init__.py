from nonebot import on_command, get_driver
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from aiocqhttp import MessageSegment
import json
import os
import httpx


async def get_url(url: str,timeout_: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(url,timeout=timeout_)
        return res.text


global_config = get_driver().config
supersuers = global_config.superusers
port = global_config.http_port


call_api = on_command("callapi", aliases={"api"})
@call_api.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    args = args.strip()
    if str(event.user_id) in supersuers:
        await get_url(f"http://127.0.0.1:{port}/{args}", 300)
    else:
        await call_api.finish("😅 你谁啊")


run = on_command("run", aliases={})
@run.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()
    args = args.strip()
    if str(event.user_id) in supersuers:
        msg = os.popen(args).read()
        await run.finish(f"[Run] Done!\n{msg}")
    else:
        await call_api.finish("😅 你谁啊")

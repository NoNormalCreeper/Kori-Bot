from .data import get_server_status, get_status_image
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.matcher import Matcher
from nonebot import on_command, get_bot

mcserver = on_command("mcserver")

@mcserver.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, arg: Message = CommandArg(), state: T_State = State()):
    default_list = {"540786009": ""}
    arg = arg.extract_plain_text().strip()
    if arg == '':
        ip = default_list[str(event.group_id)]
    else:
        ip = arg
        if '-img' in ip:
            ip = ip.replace('-img', '')
            ip = ip.strip()
            result = await get_status_image(ip)
            if result is None:
                await mcserver.finish('获取信息失败...')
            else:
                await mcserver.finish(MessageSegment.image(result))
    result = await get_server_status(ip)
    await mcserver.finish(result)
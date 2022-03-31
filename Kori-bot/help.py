from nonebot.adapters import Bot, Event, Message
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot import on_command


help = on_command("help", aliases={'帮助'})


@help.handle()
async def handle(bot: Bot, event: Event, matcher: Matcher):
    result = "在线命令手册: \nhttp://u6.gg/kpxbr"
    await help.send(result)

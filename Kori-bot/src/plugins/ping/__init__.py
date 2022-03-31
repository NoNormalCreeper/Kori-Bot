#{"author":"HornCopper","version":"v1.0","name":"ping","admin":"仅时间(0)$含系统占用(≥1)","aliases":"测试","desc":"测试机器人是否在线的命令。$+ping"}!
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Event
import time
import sys
import psutil
from typing import Dict, List

sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
import sys
sys.path.append("..")
from tools.permission import checker, error

ping = on_command("ping", aliases={"测试"})

@ping.handle()
async def _(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),1):
        def per_cpu_status() -> List[float]:
            return psutil.cpu_percent(interval=1, percpu=True)
        def memory_status() -> float:
            return psutil.virtual_memory().percent
        times = str("现在是"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n当前版本v0.0.1(Nonebot 2.0.0b1)")
        msg = f"CPU占用：{str(per_cpu_status()[0])}%\n内存占用：{str(memory_status())}%\n"
        await ping.finish(msg+times)
    else:
        times = str("现在是"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n当前版本v0.0.1(Nonebot 2.0.0b1)")
        await ping.finish(times)
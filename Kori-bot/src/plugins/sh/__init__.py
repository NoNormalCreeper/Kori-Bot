#{"author":"HornCopper","version":"v1.0","name":"sh","admin":"仅Owner(3349104868)$或SuperAdmin(1445957253)","aliases":"无","desc":"执行系统命令。$获得输出：+screen <cmd>$不获得输出：+bash <cmd>$$请注意这两个概念实际上不同！"}!
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Event
import os

bash = on_command("bash")

@bash.handle()
async def bash_(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if str(event.user_id) == "3349104868" or str(event.user_id) == "1445957253" or str(event.user_id) == "2560359315": 
        os.system(args.extract_plain_text())
        await bash.finish("执行完毕！")
        return
    else:
        await bash.finish("权限不够哦，此命令仅Owner(3349104868、2560359315)和SuperAdmin(1445957253)可以玩。")

screen = on_command("screen")

@screen.handle()
async def screen_(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if str(event.user_id) == "3349104868" or str(event.user_id) == "1445957253" or str(event.user_id) == "2560359315": 
        msg = os.popen(args.extract_plain_text()).read()
        await screen.finish(f"{msg}")
    else:
        await bash.finish("权限不够哦，此命令仅Owner(3349104868、2560359315)和SuperAdmin(1445957253)可以玩。")

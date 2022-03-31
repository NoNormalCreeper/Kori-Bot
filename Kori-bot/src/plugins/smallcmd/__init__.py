#{"author":"HornCopper","version":"v1.0","name":"指令集","admin":"0-10","aliases":"edithelpimagesize=ehis$nowhelpimagesize=nhis","desc":"无"}!
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.params import CommandArg
from nonebot.plugin import on_startswith
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot import on_command
import sys, os
sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
import sys
sys.path.append("..")
from tools.permission import checker, error

edithelpimagesize = on_command("edithelpimagesize",aliases={"ehis"})

@edithelpimagesize.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    size = args.extract_plain_text()
    cache = open("./src/plugins/help/size",mode="w")
    cache.write(size)
    cache.close()
    await edithelpimagesize.finish("图片尺寸已修改为"+size+"。")
    
nowhelpimagesize = on_command("nowhelpimagesize",aliases={"nhis"})

@nowhelpimagesize.handle()
async def __(bot: Bot, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),1):
        cache = open("./src/plugins/help/size",mode="r")
        size = cache.read()
        cache.close()
        await nowhelpimagesize.finish("查到了！当前图片尺寸为"+size+"。")
    else:
        await nowhelpimagesize.finish(error(1))

purge = on_command("purge")

@purge.handle()
async def ___(bot: Bot, event: Event, args: Message = CommandArg()):
    os.system("rm -rf ./src/plugins/help/help.png")
    os.system("rm -rf ./src/plugins/help/help.html")
    await purge.finish("唔……已清除图片缓存！")

shutdown = on_command("shutdown",aliases={"poweroff"})

@shutdown.handle()
async def ____(bot: Bot, event: Event, args: Message = CommandArg()):
    await shutdown.send("请稍候，正在关闭中……")
    await shutdown.send("关闭成功！请联系Owner(3349104868、2560359315)到后台手动开启哦~")
    os.system("killall nb")
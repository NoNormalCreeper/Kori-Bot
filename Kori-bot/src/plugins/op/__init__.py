#{"author":"HornCopper","version":"v1.0","name":"op","admin":"10","aliases":"admin、setadmin","desc":"设置管理员的命令。$+op <qqnumber> <level>"}!
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import Arg, CommandArg, ArgPlainText
import json
import sys

sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
import sys
sys.path.append("..")
from tools.permission import checker, error

op = on_command("op", aliases={"admin","setadmin"}, priority=1)

def checknumber(number):
    return number.isdecimal()
    
@op.handle()
async def handle_first_receive(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10):
        info = args.extract_plain_text()
        if info:
            try:
                arguments = info.split(' ')
            except:
                pass
            try:
                if checknumber(str(arguments[0])) == False or checknumber(str(arguments[1])) == False:
                    await op.finish("唔……QQ号和权限等级必须都是数字哦~")
                    return
            except:
                await op.finish("啊这，你这参数不够哦")
            else:
                file_1 = open("./src/plugins/op/permission.json",mode="r")
                adminlist = json.loads(file_1.read())
                if arguments[0] == "3349104868":
                    await op.finish("呼呼呼，主人的等级你是改不了的啦。")
                    return
                if arguments[1] not in ["0","1","2","3","4","5","6","7","8","9","10"]:
                    await op.finish("哪来这种等级啊喂"+ms.face(146))
                    return
                if arguments[1] == "10":
                    await op.finish("你不能添加这么高的权限啊。")
                    return
                if arguments[0] in adminlist:
                    if arguments[1] == "0":
                        adminlist.pop(arguments[0])
                        msg = f"管理员账号({arguments[0]})已经给他撤喽。"
                    else:
                        msg = f"管理员账号({arguments[0]})已经有了，本来是{str(adminlist[arguments[0]])}，已经改成{str(arguments[1])}喽。"
                        adminlist[arguments[0]] = int(arguments[1])
                else:
                    adminlist[arguments[0]] = int(arguments[1])
                    msg = f"已添加管理员账号({arguments[0]})及权限等级{str(arguments[1])}了哦。"
                file_2 = open("./src/plugins/op/permission.json",mode="w")
                file_2.write(json.dumps(adminlist))
                await op.finish(msg)
                return
        else:
            await op.finish("试问您输入了什么？")
            return
    else:
        await op.finish(error("10"))
        return

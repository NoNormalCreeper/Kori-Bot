#{"author":"HornCopper","version":"v1.0","name":"结婚插件","admin":"无","aliases":"+gm - 求婚$+cm - 同意$+dm - 拒绝$+lm - 离婚","desc":"结婚插件$+getmarry <qq> - 结婚，后面跟对象QQ号$+delmarry <qq> - 离婚，后面跟对象QQ号$温馨提示：被求婚的是老婆哦~"}!
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.params import Arg, CommandArg, ArgPlainText
from aiocqhttp import MessageSegment as ms
import os
import re
import json
import sys
from .marry import already_married
sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
import sys
sys.path.append("..")
from .tools.permission import checker, error

def checknumber(number):
    return number.isdecimal()

gm = on_command("gm",aliases={"getmarry"})

@gm.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    husband = str(event.user_id)
    wife = args.extract_plain_text()
    if husband == wife:
        await gm.finish("诶？不能自娱自乐啊！")
        return
    if checknumber(wife) == True or wife == "3438531564":
        pass
    else:
        await gm.finish("你在跟谁求婚啊喂？！")
        return
    if already_married(husband):
        await gm.finish("你已经求过婚了哦，不能再要了。")
        return
    elif already_married(wife):
        await gm.finish("可惜别人抢先求婚/结婚了，除非对方拒绝/离婚，否则您只能下次早点了。")
        return
    else:
        newmarry = {"wife":wife,"husband":husband,"confirm":"No"}
        cache = open("./src/plugins/marry/marry.json",mode="r")
        nowlist = json.loads(cache.read())
        cache.close()
        nowlist.append(newmarry)
        cache = open("./src/plugins/marry/marry.json",mode="w")
        cache.write(json.dumps(nowlist))
        cache.close()
        msg = ms.at(husband) + " 已收到！请提醒对方使用+cm <你的QQ号>来同意哦，其他人都没办法抢哦~"
        await gm.finish(msg)
        
cm = on_command("confirmmarryapply",aliases={"cm","cmp"})

@cm.handle()
async def __(bot: Bot, event: Event, args: Message = CommandArg()):
    husband = args.extract_plain_text()
    wife = str(event.user_id)
    cache = open("./src/plugins/marry/marry.json",mode="r")
    nowlist = json.loads(cache.read())
    cache.close()
    cache = open("./src/plugins/marry/marry.json",mode="w")
    for i in nowlist:
        if i["wife"] == wife and i["husband"] == husband:
            if i["confirm"] == "Yes":
                await cm.finish("不能再同意了哦，你们已经结婚了。")
                return
            else:
                i["confirm"] = "Yes"
                cache.write(json.dumps(nowlist))
                cache.close()
                await cm.finish("恭喜" + ms.at(husband) + "和" + ms.at(wife) + "结婚！")
                return
    await cm.finish("你不能和他结婚，因为他还没有求婚呢！")
    return

dm = on_command("denymarryapply",aliases={"dm","dmp"})

@dm.handle()
async def ___(bot: Bot, event: Event, args: Message = CommandArg()):
    husband = args.extract_plain_text()
    wife = str(event.user_id)
    cache = open("./src/plugins/marry/marry.json",mode="r")
    nowlist = json.loads(cache.read())
    cache.close()
    cache = open("./src/plugins/marry/marry.json",mode="w")
    for i in nowlist:
        if i["wife"] == wife and i["husband"] == husband:
            if i["confirm"] == "No":
                nowlist.remove(i)
                cache.write(json.dumps(nowlist))
                cache.close()
                await dm.finish(ms.at(husband) + " 你的求婚被拒绝了！")
                return
            else:
                cache.close()
                await dm.finish("已经结婚了，不能拒绝求婚，请使用+lm进行离婚，非常不推荐的哦！")
                return
    cache.close()
    await dm.finish("你不能拒绝他的求婚，因为他还没向你求婚呢！")
    return
    
lm = on_command("leavemarry",aliases={"lm","delmarry"})

@lm.handle()
async def ____(bot: Bot, event: Event, args: Message = CommandArg()):
    self_id = str(event.user_id)
    cache = open("./src/plugins/marry/marry.json",mode="r")
    nowlist = json.loads(cache.read())
    cache.close()
    cache = open("./src/plugins/marry/marry.json",mode="w")
    for i in nowlist:
        if i["wife"] == self_id or i["husband"] == self_id:
            if i["confirm"] == "Yes":
                nowlist.remove(i)
                cache.write(json.dumps(nowlist))
                cache.close()
                await lm.finish("你们离婚了！")
                return
            else:
                cache.close()
                await lm.finish("你们不能离婚，因为尚未接受对方求婚！")
                return
    cache.close()
    await lm.finish("你和他没有任何瓜葛，不可以离婚。")
    return

m = on_command("marry",aliases={"老婆","我的老婆","老公","我的老公"})

@m.handle()
async def _____(bot: Bot, event: Event, args: Message = CommandArg()):
    self_id = str(event.user_id)
    cache = open("./src/plugins/marry/marry.json")
    nowlist = json.loads(cache.read())
    role = ""
    cache.close()
    for i in nowlist:
        if i["wife"] == self_id and i["confirm"] == "Yes":
            role = "老公"
            another = i["husband"]
        elif i["husband"] == self_id and i["confirm"] == "Yes":
            role = "老婆"
            another = i["wife"]
    if role:
        msg = ms.at(self_id) + f" 你的{role}是{another}！"
    else:
        msg = ms.at(self_id) + " 没有查到呢，你应该还没结婚吧！"
    await m.finish(msg)
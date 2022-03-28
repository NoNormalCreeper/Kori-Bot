#{"author":"HornCopper","version":"v1.0","name":"违禁词封锁","admin":"触发(0-4)$设置(5-10)","aliases":"+bwa$+bwr$+bwl","desc":"封禁指定词语$添加：+bwa <message>$移除：+bwr <message>"}!
from nonebot import on_command
from nonebot import on_message
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Event
from aiocqhttp import MessageSegment as ms

import json
import sys
sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
from permission import checker, error

global flag

def is_in(full_str, sub_str): 
  try: 
    full_str.index(sub_str) 
    return True
  except ValueError: 
    return False

bw = on_message(priority=5)

@bw.handle()
async def _(bot: Bot, event: MessageEvent):
    if checker(str(event.user_id),5) == False:
        flag = False
        cache = open("./src/plugins/banword/banword.json",mode="r")
        banwordlist = json.loads(cache.read())
        cache.close()
        msg = str(event.raw_message)
        id = str(event.message_id)
        for i in banwordlist:
            if is_in(msg,i):
                flag = True
        if flag:
            sb = str(event.user_id)
            try:
                group = event.group_id
                await bot.call_api("delete_msg",message_id=id)
                await bot.call_api("set_group_ban", group_id = group, user_id = sb, duration = 60)
                msg = ms.at(sb) + "你触发了违禁词哦，呐，给你喝了1杯1分钟的红茶。"
                await bw.finish(msg)
            except:
                pass
        else:
            pass
    else:
        pass
    
bwa = on_command("banwordadd",aliases={"bwa","addbanword"})

@bwa.handle()
async def __(matcher: Matcher, event: Event, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    if checker(str(event.user_id),5):
        if cmd:
            nowjson = open("./src/plugins/banword/banword.json",mode="r")
            now = json.loads(nowjson.read())
            nowjson.close()
            now.append(cmd)
            future = open("./src/plugins/banword/banword.json",mode="w")
            future.write(json.dumps(now,ensure_ascii=False))
            future.close()
            await bwa.finish("成功封禁该词语，以后再发就会被我封禁了哦。")
        else:
            await bwa.finish("试问您输入了个什么？")
    else:
        await bwa.finish(error(5))

bwr = on_command("banwordremove",aliases={"removebanword","deletebanword","bwd","bwr"})

@bwr.handle()
async def ___(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),5):
        cmd = args.extract_plain_text()
        if cmd:
            cache = open("./src/plugins/banword/banword.json",mode="r")
            banwordlist = json.loads(cache.read())
            cache.close()
            try:
                banwordlist.remove(cmd)
                future = open("./src/plugins/banword/banword.json",mode="w")
                future.write(json.dumps(banwordlist,ensure_ascii=False))
                future.close()
                await bwr.finish("成功解禁该词语，以后再发也不会被我封禁了哦。")
            except ValueError:
                await bwr.finish("试问这词语被封禁了吗？")
        else:
            await bwr.finish("[CuBot]Failed：输入为空。")
    else:
        await bwr.finish(error(5))

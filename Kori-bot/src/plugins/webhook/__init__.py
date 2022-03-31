#{"author":"HornCopper","version":"v1.0","name":"GitHub Webhook监听设置","admin":"9","aliases":"+wa - 添加监听$+wr - 移除监听","desc":"添加/移除GitHub Webhook发送的群：$+webhookadd <group_id> - 添加$+webhookremove <group_id> - 移除"}!
from nonebot import on_command
from nonebot import on_message
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from aiocqhttp import MessageSegment as ms

import json

import sys
sys.path.append("..")
from .tools.permission import checker, error

wa = on_command("webhookadd",aliases={"wa"})

@wa.handle()
async def _(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),9):
        group_id = args.extract_plain_text()
        cache = open("./src/plugins/webhook/webhook.json",mode="r")
        grouplist = json.loads(cache.read())
        cache.close()
        for i in grouplist:
            if i == group_id:
                await wa.finish("没有办法添加嗷，因为已经添加过了。")
                return
        grouplist.append(group_id)
        cache = open("./src/plugins/webhook/webhook.json",mode="w")
        cache.write(json.dumps(grouplist))
        cache.close()
        await wa.finish(f"添加群{group_id}的Webhook监听成功！")
    else:
        await wa.finish(error(9))
        
wr = on_command("webhookremove",aliases={"wr"})

@wr.handle()
async def _(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),9):
        group_id = args.extract_plain_text()
        cache = open("./src/plugins/webhook/webhook.json",mode="r")
        grouplist = json.loads(cache.read())
        cache.close()
        for i in grouplist:
            if i == group_id:
                grouplist.remove(i)
                cache = open("./src/plugins/webhook/webhook.json",mode="w")
                cache.write(json.dumps(grouplist))
                cache.close()
                await wa.finish(f"移除群{group_id}的Webhook监听成功！")
                return
        await wa.finish(f"群{group_id}尚未设置Webhook监听哦。")
    else:
        await wr.finish(error(9))
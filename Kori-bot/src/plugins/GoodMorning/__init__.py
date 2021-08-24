# -*- coding: utf-8 -*-

from nonebot import *
import nonebot
from . import match

# bots = nonebot.get_bots()
# print(bots)
# bot=nonebot.get_bot(bots[0])
bot=nonebot.get_bot()

@bot.on_message("group")
async def entranceFunction(context):
    msg = str(context["message"])
    userQQ = context["user_id"]
    userGroup = context["group_id"]
    sender = context['sender']
    await match.starter(bot)
    await match.mainProgram(bot, userQQ, userGroup, msg, sender)
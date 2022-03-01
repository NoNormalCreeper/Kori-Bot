# -*- coding: utf-8 -*-

from nonebot import *
from .match import match

bot = get_bot()

@bot.on_message("group")
async def entranceFunction(context):
    msg = context['message']
    userGroup = context["group_id"]
    userQQ = context["user_id"]
    try:
        await match(msg, bot, userQQ, userGroup)
    except:
        pass

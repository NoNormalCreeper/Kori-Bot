# -*- coding: utf-8 -*-

from .constant import *
from .utils import commandMatching, pictureCqCode
from .throw import throw, creep

async def match(msg, bot, userQQ, userGroup):

    creepCommandList = ['爬', '爪巴', '给爷爬', '爬啊', '快爬']
    throwCommandList = ['丢', '我丢']

    plainText = str(msg)
    # creep features
    result = await commandMatching(plainText, creepCommandList, model = BLURRY)
    if result['mark']:
        # Parsing parameters
        qq = await parsingParameters(msg)
        if qq != FAILURE:
            outPath = await creep(qq)
            sendMsg = ''
            sendMsg += await pictureCqCode(outPath)
            await bot.send_group_msg(group_id = userGroup, message = sendMsg)
            return
    # throe features
    result = await commandMatching(plainText, throwCommandList, model = BLURRY)
    if result['mark']:
        # Parsing parameters
        qq = await parsingParameters(msg)
        if qq != FAILURE:
            outPath = await throw(qq)
            sendMsg = ''
            sendMsg += await pictureCqCode(outPath)
            await bot.send_group_msg(group_id = userGroup, message = sendMsg)
            return

async def parsingParameters(msg):
    for segment in msg:
        if segment['type'] == 'at':
            return segment['data']['qq']
    return FAILURE
# -*- coding: utf-8 -*-

from . import main
from . import utils

thesaurusReady = False
botQQ = 0

async def cleanUpExcessContent(msg):
    global botQQ
    atField = '[CQ:at,qq=' + str(botQQ) + ']'
    return msg.replace(atField, '').strip()


async def starter(bot):
    global thesaurusReady
    global botQQ
    if thesaurusReady == False:
        botQQ = await bot.get_login_info()
        botQQ = int(botQQ['user_id'])
        thesaurusReady = True
    

async def mainProgram(bot, userQQ, userGroup, msg, sender):
    # Clean at
    msg = await cleanUpExcessContent(msg)
    # Recognition instruction
    goodMorningInstructionSet = ['早', '早安', '哦哈哟', 'ohayo', 'ohayou', '早安啊', '早啊', '早上好']
    goodNightInstructionSet = ['晚', '晚安', '哦呀斯密', 'oyasumi', 'oyasimi', '睡了', '睡觉了']
    send = ''
    # Good morning match
    for i in goodMorningInstructionSet:
        if msg == i:
            send = await main.goodMorningInformation(userQQ, userGroup, sender)
            break
    mark = await utils.sendMsg(bot, userGroup, send)
    if mark:
        return
    # Good night detection
    for i in goodNightInstructionSet:
        if msg == i:
            send = await main.goodNightInformation(userQQ, userGroup, sender)
            break
    mark = await utils.sendMsg(bot, userGroup, send)
    if mark:
        return
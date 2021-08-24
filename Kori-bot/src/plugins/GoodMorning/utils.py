# -*- coding: utf-8 -*-

import os
import aiofiles
import ujson
from dateutil.parser import parse
import datetime
import random
from .config import *

async def jsonRead(p):
    if not os.path.exists(p):
        return ERROR
    async with aiofiles.open(p, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    return content

async def jsonWrite(p, info):
    async with aiofiles.open(p, 'w', encoding='utf-8') as f:
        await f.write(ujson.dumps(info))
    return SUCCESS

async def getTheCurrentTime():
    nowDate = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
    return nowDate

async def getAccurateTimeNow():
    nowDate = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d/%H:%M:%S'))
    return nowDate

async def timeDifferenceFromNowOn(original):
    a = parse(str(original))
    b = parse(await getTheCurrentTime())
    return int((b - a).days)

async def judgeTimeDifference(lastTime):
    timeNow = await getAccurateTimeNow()
    a = parse(lastTime)
    b = parse(timeNow)
    return int((b - a).total_seconds() / 3600)

async def calculateTheElapsedTimeCombination(lastTime):
    timeNow = await getAccurateTimeNow()
    a = parse(lastTime)
    b = parse(timeNow)
    seconds = int((b - a).total_seconds())
    return [int(seconds / 3600), int((seconds % 3600) / 60), int(seconds % 60)]

async def getTheCurrentHour():
    return int(str(datetime.datetime.strftime(datetime.datetime.now(),'%H')))

async def userInformationReading(userQQ):
    p = './GoodMorning/Data/User/' + str(userQQ) + '.json'
    content = await jsonRead(p)
    return content

async def userInformationWriting(userQQ, info):
    p = './GoodMorning/Data/User/' + str(userQQ) + '.json'
    await jsonWrite(p, info)
    return SUCCESS

async def groupRead(userGroup):
    p = './GoodMorning/Data/Group/' + str(userGroup) + '.json'
    group = await jsonRead(p)
    return group

async def groupWrite(userGroup, info):
    p = './GoodMorning/Data/Group/' + str(userGroup) + '.json'
    await jsonWrite(p, info)
    return SUCCESS

async def at(userQQ):
    return '[CQ:at,qq=' + str(userQQ) + ']\n'

async def readConfiguration(model):
    if model == MORNING_MODEL:
        return await jsonRead('./GoodMorning/Config/GoodMorning.json')
    if model == NIGHT_MODEL:
        return await jsonRead('./GoodMorning/Config/GoodNight.json')

async def extractRandomWords(model, sender):
    name = sender['card']
    if name == '':
        name = sender['nickname']
    return random.choice((await readConfiguration(model))['statement'])['content'].replace(r'{name}', name)

async def extractConfigurationInformationAccordingToSpecifiedParameters(parameter, model):
    return (await readConfiguration(model))[parameter]

async def replaceHourMinuteAndSecond(parameterList, msg):
    return (msg.replace(r'{hour}', str(parameterList[0]))
                .replace(r'{minute}', str(parameterList[1]))
                .replace(r'{second}', str(parameterList[2])))

async def sendMsg(bot, userGroup, send):
    if send != '' and send != ERROR:
        await bot.send_group_msg(group_id = int(userGroup), message = str(send))
        return True
    return False
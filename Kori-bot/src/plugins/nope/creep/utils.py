# -*- coding: utf-8 -*-

import aiohttp
import random
import os
from .constant import *


async def asyncGet(url, headers='', timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            img = await res.read()
    return img


async def getAvatar(url):
    img = await asyncGet(url)
    return img


async def checkFolder(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


# Match Command Tool
async def commandMatching(msg, commandList, model = ALL):
    backToCollection = {
        'mark': False
    }
    if model == ALL:
        for i in commandList:
            if msg.strip() == i:
                backToCollection['mark'] = True
                break
    if model == BLURRY:
        for command in commandList:
            if msg.find(command) != -1:
                backToCollection['mark'] = True
                break
    return backToCollection


# Picture tool
async def pictureCqCode(relativePosition):
    relativePosition = relativePosition.strip('./')
    back = relativePosition[relativePosition.find('/'):]
    filePath = 'file:///' + os.path.dirname(__file__) + back
    return '[CQ:image,file=' + filePath + ']'

# Common tools
async def atQQ(userQQ):
    return '[CQ:at,qq=' + str(userQQ) + ']\n'
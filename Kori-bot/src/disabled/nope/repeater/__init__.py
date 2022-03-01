# -*- coding: UTF-8 -*-
from nonebot import *
from aiocqhttp.exceptions import Error as CQHttpError
from . import main
import time,os,random
import aiofiles

bot = get_bot()

async def t_w():
    p = "repeater_data/time.txt"
    s = time.time()
    sub = 0
    if os.path.exists(p):
        async with aiofiles.open(p,"r",encoding = 'utf-8') as f:
            read = await f.read()
            read = read.strip()
            sub = s - float(read)
            print(sub)
    else:
        async with aiofiles.open(p,"w",encoding = 'utf-8') as f:
            await f.write(str(s))
    if sub>60:
        async with aiofiles.open(p,"w",encoding = 'utf-8') as f:
            await f.write(str(s))
        return 1
    else:
        return 0

async def gjc_on(qun):
    p = "repeater_data/gjc_no.txt"
    mark = 1
    if os.path.exists(p):
        async with aiofiles.open(p,"r",encoding = 'utf-8') as f:
            lines = await f.readlines()
            for line in lines:
                line = line.strip()
                if line == str(qun):
                    mark = 0
                    break
    return mark

@bot.on_message("group")
async def re(context):
    msg = context["message"]
    s_msg = str(msg)
    qun = context["group_id"]
    qq = context["user_id"]
    mark = await main.re(qun,msg)
    if mark == 1:
        if await gjc_on(qun)==1:
            await bot.send_msg(group_id=qun,message=msg)

    #关键词部分
    if await gjc_on(qun):
        if os.path.exists("repeater_data/gjc.txt"):
            async with aiofiles.open("repeater_data/gjc.txt","r",encoding = 'utf-8') as f:
                lines = await f.readlines()
                for line in lines:
                    line = line.strip().split(" ")
                    gjc = line[0]
                    model = int(line[1])
                    time_white = int(line[2])
                    send = line[3]
                    if model == 1:
                        #jingque
                        if gjc == s_msg:
                            if time_white == 1:
                                if await t_w()==1:
                                    await bot.send_msg(group_id=qun,message=send)
                            else:
                                await bot.send_msg(group_id=qun,message=send)
                            break
                    else:
                        #mohu
                        if s_msg.find(gjc)!=-1:
                            if time_white == 1:
                                if await t_w()==1:
                                    await bot.send_msg(group_id=qun,message=send)
                            else:
                                await bot.send_msg(group_id=qun,message=send)
                            break




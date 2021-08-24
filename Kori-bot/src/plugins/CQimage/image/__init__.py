# -*- coding: UTF-8 -*-
from nonebot import *
from aiocqhttp.exceptions import Error as CQHttpError
from . import main
from . import get
import os
bot = get_bot()

@bot.on_message("group")
async def Help(context):
    msg = str(context["message"])
    qq = context["user_id"]
    if msg=="img list":
        if os.path.exists("../data/image/list.jpg"):
            qun = context["group_id"]
            await bot.send_msg(group_id=qun,message="[CQ:image,file=list.jpg]")
    else:
        if msg.find("Img")!=-1 or msg.find("img")!=-1:
            mark = await get.setQqName(qq,msg)
            if mark == 1:
                msg = msg.split(" ")[1]
                qun = context["group_id"]
                await bot.send_msg(group_id=qun,message="[CQ:at,qq="+str(qq)+"] 表情更换为["+msg+"]")
        else:
            if msg.find(".jpg")!=-1 or msg.find(".JPG")!=-1:
                if msg.find("CQ:")==-1:
                    msg = msg[0:msg.find(".")]
                    qun = context["group_id"]
                    await main.img(msg,qq,qun,bot)

# -*- coding: UTF-8 -*-

import os
import aiofiles

async def re(qun,msg):
    mark = 0
    msg = str(msg)
    p="repeater_data/"+str(qun)+".txt"
    if msg.find(".jpg")!=-1 or msg.find(".JPG")!=-1:
        return 0
    else:
        if os.path.exists(p):
            async with aiofiles.open(p,"r",encoding = 'utf-8') as f:
                msg_old = await f.read()
                msg_old = msg_old.strip()
            if msg_old == msg:
                mark=1
                async with aiofiles.open(p, "w",encoding = 'utf-8') as f:
                    await f.write("")
        if mark==0:
            async with aiofiles.open(p,"w",encoding = 'utf-8') as f:
                    await f.write(msg)
        return mark

from nonebot.permission import Permission
from nonebot.typing import T_State
from nonebot import on_command
from PIL import Image
import os
import random as ra
from PIL import ImageDraw, ImageFont
from nonebot.adapters.cqhttp import Bot, Message, Event
from nonebot.adapters.cqhttp.message import MessageSegment
import glob
from pathlib import Path

xb=on_command("喜报")

dir="D:\\Files\\coding\\Kori-bot\\Kori-bot\\src\\plugins\\xibao\\pic\\"

@xb.handle()
async def help_handle(bot: Bot, event: Event, state: T_State):

    content = str(event.get_message()).strip()
    if content:
        print(1)
        state['content'] = content
        text=state['content']
        size=(1024,768)
        name=str(ra.randint(100,9999999))+".jpg"
        # os.system("cd "+dir)
        # os.system("copy "+dir+"origin.jpg "+dir+name)
        image = Image.open(dir+"origin.jpg")
        # image.show()
        # draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font='msyh.ttc', size=50)
        # draw.text(xy=(120, 320), text=text, fill=(255, 0, 0), font=font)

        # 设置字体
        font = ImageFont.truetype('msyh.ttc', 50)
        # 计算使用该字体占据的空间
        # 返回一个 tuple (width, height)
        # 分别代表这行字占据的宽和高
        text_width = font.getsize(text)
        draw = ImageDraw.Draw(image)

        # 计算字体位置
        text_coordinate = int((size[0]-text_width[0])/2), int((size[1]-text_width[1])/2)
        # 写字
        draw.text(text_coordinate, text,(255,0,0), font=font)
                
        image.save(dir+name)

        await xb.send(MessageSegment.image(f"file:///{(dir+name)}"),at_sender=True)

    else:
        await xb.send(MessageSegment.image(f"file:///{(dir+'origin.jpg')}"),at_sender=True)
        



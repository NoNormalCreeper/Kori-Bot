from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command
from nonebot.adapters.cqhttp.message import MessageSegment
# import web_1
import random
import requests
import cairosvg

# url_info=("https://latex.codecogs.com/svg.latex?\sqrt2",'test')

def download_img(url_info):
    if url_info[1]:
        print("-----------正在下载图片 %s"%(url_info[0]))
        # 这是一个图片的url
        try:
            url = url_info[0]
            response = requests.get(url)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            #保存路径
            path='%s.svg' % (url_info[1])
            with open(path, 'wb') as f:
                f.write(img)
        except Exception as ex:
            print("--------出错继续----")
            pass
    else:
        print(0)



latex=on_command("latex")

@latex.handle()
async def latex_handle(bot: Bot, event: Event, state: T_State):
    cmd = str(event.get_message()).strip()
    
    url="https://latex.codecogs.com/svg.latex?"+cmd

    name=str(random.randint(1000,999999))+".svg"

    download_img((url,("pics/"+name)))

    cairosvg.svg2png(url=svg_path, write_to=png_path)

    await latex.send(MessageSegment.image(f"file:///{('pics/'+name)}"))
# from nonebot.permission import Permission
from nonebot.adapters import Bot, Event, Message
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot import on_command
import requests
import json
import datetime

saying = on_command("saying", aliases={'一言'})

tih = on_command("tih")

school = on_command("school")

types = {'a':'动画',
          'b':'漫画',
          'c':'游戏',
          'd':'文学',
          'e':'原创',
          'f':'来自网络',
          'g':'其他',           'h':'影视',
          'i':'诗词',           'j':'网易云',
          'k':'哲学',           'l':'抖机灵'}

# e.g. {"id":6491,"uuid":"2fcd691a-ebb0-4cf3-b189-b991de5ee36d","hitokoto":"遗忘，也是种解脱：当人们为之逝去，活下来的为之蒙恨的时候。","type":"c","from":"«最后的老兵»，TNO启示录事件","from_who":"The New Order:Last Days of Europe","creator":"Forevercontinent","creator_uid":7134,"reviewer":6844,"commit_from":"web","created_at":"1599385727","length":29}

def caculate_school():
    now = datetime.datetime.now()
    start = datetime.datetime(2022,1,4,17,0,0)
    end = datetime.datetime(2022,4,8,7,30,0)
    delta = end - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = delta.seconds // 60 % 60
    seconds = delta.seconds % 60
    total_milliseconds = delta.total_seconds() * 1000

    # progress bar
    maxn = 24
    progress=int((now-start).total_seconds()/(end-start).total_seconds()*maxn)
    bar = f"[{('█' * progress + '░' * (maxn-progress))}]"

    return (f'{days} 天 {hours} 小时 {minutes} 分钟 {seconds} 秒', ('%.2f 秒'%(total_milliseconds/1000), bar))

@saying.handle()
async def handle(bot: Bot, event: Event, matcher: Matcher):
    content=(requests.get("https://v1.hitokoto.cn/?encode=json")).json()
    # content=json.loads(content)
    # print(content)

    result="【一言】"
    result+=content["hitokoto"]
    result+="\n来源："
    result+=content["from"]
    result+="\n作者："
    result+=content["creator"]
    result+="\n类型："
    result+=types[content["type"]]

    # print(result)

    # await saying.send(result)
    # await saying.finish(Message(result))
    await saying.send(result)


@tih.handle()   # Today in history
async def _(bot: Bot, event: Event, matcher: Matcher):
    try:
        resp = requests.get("https://api.iyk0.com/lishi")
    except:
        await tih.finish("Error!")
    content = resp.text
    content = content.replace(" ", "").replace("\n", "")
    c = json.loads(content)
    c = c[content[2:8]]
    msg = "历史上的今天: \n"
    for i in c:
        msg += "{0}的今天, {1}\n".format(i['year'], i['title'])
    await tih.send(msg)

@school.handle()
async def _(bot: Bot, event: Event, matcher: Matcher):
    result = '距离开学还有:\n'
    result += caculate_school()[0]
    result += '\n(共计: '
    result += caculate_school()[1]
    result += ' )\n'
    result += caculate_school()[2]
    await school.finish(result)

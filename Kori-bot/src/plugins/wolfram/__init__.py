from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.matcher import Matcher
from nonebot import on_command
# import requests
import json
# import get_answer as ga
# from get_answer import *


# ----- get_answer starts -----
import requests as re
import shutil
import json
import urllib


url_calc="http://api.wolframalpha.com/v1/simple?appid={1}&i={0}&units=metric"
url_tellme="https://api.wolframalpha.com/v1/result?appid={1}&i={0}&units=metric"
API_key="X9H8TV-QKGR82YQUY"


def get_calc(question: str):
    url=(url_calc.format(urllib.parse.quote(question), API_key))
    resp=re.get(url, stream=True)
    # with open("answer.gif","wb") as pic:
    #     # try:
    #         # pic.write(url.content)
    #     # for chunk in resp.iter_content(1024):
    #     #     pic.write(chunk)
    #     resp.raw.decode_content = True
    #     shutil.copyfileobj(resp.raw, pic)

    #     # except:
    #     #     return str(resp)
    return resp.content

    # return 0

def get_tellme(question: str):
    url=(url_tellme.format(urllib.parse.quote(question), API_key))
    resp=re.get(url)
    # try:
    #     result=resp.text
    # except:
    #     return str(resp)
    return resp.text
    # return resp.content.decode(resp.apparent_encoding).encode('ascii')

# ----- get_answer ends -----


def removeprefix(string, prefix):
    if not (isinstance(string, str) and isinstance(prefix, str)):
        raise TypeError('Param value type error')
    if string.startswith(prefix):
        return string[len(prefix):]
    return string



tellme = on_command("tellme")

@tellme.handle()
async def tellme_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State()):
    arg = removeprefix((str(event.get_message()).strip())[1:], "tellme")
    print(("args:",arg))
    result = get_tellme(arg)

    await tellme.send(('[Result]\n'+result))


calc = on_command("calc", aliases={'计算'})


@calc.handle()
async def calc_handle(bot: Bot, event: Event, matcher: Matcher, state: T_State = State()):
    arg = removeprefix((str(event.get_message()).strip())[1:], "calc")
    result = get_calc(arg)
    try:
        await calc.send(MessageSegment.image(result))
    except:
        await calc.send("Error!")
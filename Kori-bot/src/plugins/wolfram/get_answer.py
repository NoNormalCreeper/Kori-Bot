import imp
import requests as re
import urllib
import aiohttp
from nonebot import get_driver


url_calc = "http://api.wolframalpha.com/v1/simple?appid={1}&i={0}&units=metric"
url_tellme = "https://api.wolframalpha.com/v1/result?appid={1}&i={0}&units=metric"

def get_api_key():
    try:
        API_key = get_driver().config.wolfram_api_key
        return API_key
    except Exception as e:
        raise Exception(f"请先在配置文件中配置 WOLFRAM_API_KEY 哦~\n{str(e)}")

async def get_calc(question: str):
    API_key = get_api_key()
    url=(url_calc.format(urllib.parse.quote(question), API_key))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.content.read()


async def get_tellme(question: str):
    API_key = get_api_key()
    url=(url_tellme.format(urllib.parse.quote(question), API_key))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
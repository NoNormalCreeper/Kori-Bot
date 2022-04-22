import requests as re
import urllib
import nonebot


url_calc="http://api.wolframalpha.com/v1/simple?appid={1}&i={0}&units=metric"
url_tellme="https://api.wolframalpha.com/v1/result?appid={1}&i={0}&units=metric"
try:
    API_key=nonebot.config.WOLFRAM_API_KEY
except Exception as e:
    raise Exception("请先在配置文件中配置 WOLFRAM_API_KEY 哦~\n{str(e)}")


def get_calc(question: str):
    url=(url_calc.format(urllib.parse.quote(question), API_key))
    resp=re.get(url, stream=True)
    if 'Wolfram|Alpha did not understand your input' in resp.text:
        raise Exception(resp.text)
    return resp.content


def get_tellme(question: str):
    url=(url_tellme.format(urllib.parse.quote(question), API_key))
    resp=re.get(url)
    return resp.text
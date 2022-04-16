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
    if 'Wolfram|Alpha did not understand your input' in resp.text:
        raise Exception(resp.text)
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
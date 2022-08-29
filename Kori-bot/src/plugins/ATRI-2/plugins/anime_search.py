from random import choice

from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls, Cooldown

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request, Translate
from ATRI.exceptions import RequestError

URL = "https://api.trace.moe/search?anilistInfo=true&url="
_anime_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])

__doc__ = """
通过一张图片搜索你需要的番！据说里*也可以
"""


class Anime(Service):
    def __init__(self):
        Service.__init__(self, "以图搜番", __doc__, rule=is_in_service("以图搜番"))

    @staticmethod
    async def _request(url: str) -> dict:
        aim = URL + url
        try:
            res = await request.get(aim)
        except RequestError:
            raise RequestError("Request failed!")
        return res.json()

    @classmethod
    async def search(cls, url: str) -> str:
        data = await cls._request(url)
        try:
            data = data["result"]
        except:
            return "没有相似的结果呢..."

        d = {}
        for i in range(3):
            if data[i]["anilist"]["title"]["native"] in d:
                d[data[i]["anilist"]["title"]["native"]][0] += data[i]["similarity"]
            else:
                from_m = data[i]["from"] / 60
                from_s = data[i]["from"] % 60

                to_m = data[i]["to"] / 60
                to_s = data[i]["to"] % 60

                n = data[i]["episode"] or 1
                d[Translate(data[i]["anilist"]["title"]["native"]).to_simple()] = [
                    data[i]["similarity"],
                    f"第{n}集",
                    f"约{int(from_m)}min{int(from_s)}s至{int(to_m)}min{int(to_s)}s处",
                ]

        result = sorted(d.items(), key=lambda x: x[1], reverse=True)
        msg0 = str()
        for t, i in enumerate(result, start=1):
            s = "%.2f%%" % (i[1][0] * 100)
            msg0 = msg0 + (
                "\n——————————\n"
                f"({t}) Similarity: {s}\n"
                f"Name: {i[0]}\n"
                f"Time: {i[1][1]} {i[1][2]}"
            )

        return msg0


anime_search = Anime().on_command("以图搜番", "发送一张图以搜索可能的番剧")


@anime_search.got("anime_pic", "图呢？", [Cooldown(5, prompt=_anime_flmt_notice)])
async def _deal_sear(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    img = extract_image_urls(event.message)
    if not img:
        await anime_search.finish("请发送图片而不是其它东西！！")

    await bot.send(event, "别急，在找了")
    a = await Anime().search(img[0])
    result = f"> {MessageSegment.at(user_id)}\n{a}"
    await anime_search.finish(Message(result))

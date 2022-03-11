import re

from ATRI.service import Service
from ATRI.utils import request
from ATRI.rule import is_in_service


URL = "https://api.kyomotoi.moe/api/bilibili/v3/video_info?aid="

table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
tr = dict()
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608

__doc__ = "啥b腾讯小程序给👴爪巴\n目前只整了b站的"


class Applet(Service):
    def __init__(self):
        Service.__init__(self, "小程序处理", __doc__, rule=is_in_service("小程序处理"))

    @staticmethod
    def _bv_dec(x) -> str:
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return str((r - add) ^ xor)

    @staticmethod
    def _bv_enc(x) -> str:
        x = (x ^ xor) + add
        r = list("BV1  4 1 7  ")
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return "".join(r)

    @staticmethod
    async def bili_request(url: str) -> str:
        req = await request.get(url)
        return req.headers.get("location")

    @staticmethod
    def bili_video_code_catcher(text: str) -> str:
        pattern = re.compile(r"BV[0-9A-Za-z]{10}")
        result = pattern.findall(text)
        return result[0] if result else ""

    @classmethod
    async def msg_builder(cls, text: str) -> tuple:
        bv = cls.bili_video_code_catcher(text)
        if not bv:
            pattern = r"https://b23.tv/[a-z0-9A-z]{6,7}"
            burl = re.findall(pattern, text)
            u = burl[0] if burl else str()
            if not u:
                return None, False

            rep = await cls.bili_request(u)
            bv = cls.bili_video_code_catcher(rep)
            av = cls._bv_dec(bv)

        else:
            av = cls._bv_dec(bv)

        url = URL + av
        req = await request.get(url)
        res_data = req.json()
        data = res_data["data"]

        result = (
            f"{data['bvid']} INFO:\n"
            f"Title: {data['title']}\n"
            f"Link: {data['short_link']}"
        )
        return result, True

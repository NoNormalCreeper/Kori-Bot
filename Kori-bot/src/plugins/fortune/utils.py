import nonebot
import os
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .data_source import FORTUNE_PATH

'''
    各主题抽签开关，仅在random抽签中生效
    请确保不全是False
'''
ARKNIGHTS_FLAG = bool(nonebot.get_driver().config.arknights_flag)
ASOUL_FLAG = bool(nonebot.get_driver().config.asoul_flag)
AZURE_FLAG = bool(nonebot.get_driver().config.azure_flag)
GENSHIN_FLAG = bool(nonebot.get_driver().config.genshin_flag)
ONMYOJI_FLAG = bool(nonebot.get_driver().config.onmyoji_flag)
PCR_FLAG = bool(nonebot.get_driver().config.pcr_flag)
TOUHOU_FLAG = bool(nonebot.get_driver().config.touhou_flag)
TOUHOU_OLD_FLAG = bool(nonebot.get_driver().config.touhou_old_flag)
VTUBER_FLAG = bool(nonebot.get_driver().config.vtuber_flag)
GRANBLUE_FANTASY_FLAG = bool(nonebot.get_driver().config.granblue_fantasy_flag)
PUNISHING_FLAG = bool(nonebot.get_driver().config.punishing_flag)
PRETTY_DERBY_FLAG = bool(nonebot.get_driver().config.pretty_derby_flag)
DC4_FLAG = bool(nonebot.get_driver().config.dc4_flag)
EINSTEIN_FLAG = bool(nonebot.get_driver().config.einstein_flag)
SWEET_ILLUSION_FLAG = bool(nonebot.get_driver().config.sweet_illusion_flag)
LIQINGGE_FLAG = bool(nonebot.get_driver().config.liqingge_flag)
HOSHIZORA_FLAG = bool(nonebot.get_driver().config.hoshizora_flag)
SAKURA_FLAG = bool(nonebot.get_driver().config.sakura_flag)

'''
    抽签主题开关，当随机抽签时判断某主题是否开启
'''
MainThemeEnable = {
    "pcr":              PCR_FLAG,
    "genshin":          GENSHIN_FLAG,
    "vtuber":           VTUBER_FLAG,
    "touhou":           TOUHOU_FLAG,
    "touhou_old":       TOUHOU_OLD_FLAG,
    "onmyoji":          ONMYOJI_FLAG,
    "azure":            AZURE_FLAG,
    "asoul":            ASOUL_FLAG,
    "arknights":        ARKNIGHTS_FLAG,
    "granblue_fantasy": GRANBLUE_FANTASY_FLAG,
    "punishing":        PUNISHING_FLAG,
    "pretty_derby":     PRETTY_DERBY_FLAG,
    "dc4":              DC4_FLAG,
    "einstein":         EINSTEIN_FLAG,
    "sweet_illusion":   SWEET_ILLUSION_FLAG,
    "liqingge":         LIQINGGE_FLAG,
    "hoshizora":        HOSHIZORA_FLAG,
    "sakura":           SAKURA_FLAG
}

'''
    抽签主题对应表，第一键值为“抽签设置”或“主题列表”展示的主题名称
    Key-Value: 主题资源文件夹名-设置主题别名
'''
MainThemeList = {
    "random":   ["随机"],
    "pcr":      ["PCR", "公主链接", "公主连接", "Pcr", "pcr"],
    "genshin":  ["原神", "Genshin Impact", "genshin", "Genshin"],
    "vtuber":   ["Vtuber", "VTB", "Vtb", "vtb", "管人", "holo", "猴楼"],
    "touhou":   ["东方", "touhou", "Touhou", "车万"],
    "touhou_old": 
                ["旧东方", "旧版东方", "老东方", "老版东方", "经典东方"],
    "onmyoji":  ["阴阳师", "yys", "Yys", "痒痒鼠"],
    "azure":    ["碧蓝航线", "碧蓝", "azure", "Azure"],
    "asoul":    ["asoul", "a手", "A手", "as", "As"],
    "arknights":["明日方舟", "方舟", "arknights", "鹰角", "Arknights", "舟游"],
    "granblue_fantasy":
                ["碧蓝幻想", "Granblue Fantasy", "granblue fantasy", "幻想", "fantasy", "Fantasy"],
    "punishing":["战双", "战双帕弥什"],
    "pretty_derby":
                ["赛马娘", "马", "马娘", "赛马"],
    "dc4":      ["dc4", "DC4", "Dc4", "初音岛", "初音岛4"],
    "einstein": ["爱因斯坦携爱敬上", "爱因斯坦", "einstein", "Einstein"],
    "sweet_illusion":
                ["灵感满溢的甜蜜创想", "甜蜜一家人", "富婆妹"],
    "liqingge": ["李清歌", "清歌"],
    "hoshizora":["星空列车与白的旅行", "星空列车"],
    "sakura":   ["樱色之云绯色之恋", "樱云之恋", "樱云绯恋", "樱云"]
}

def copywriting() -> str:
    p = f"{FORTUNE_PATH}/fortune/copywriting.json"
    if not os.path.exists(p):
        return False

    with open(p, "r", encoding="utf-8") as f:
        content = json.load(f)

    return random.choice(content["copywriting"])

def getTitle(structure):
    p = f"{FORTUNE_PATH}/fortune/goodLuck.json"
    if not os.path.exists(p):
        return False

    with open(p, "r", encoding="utf-8") as f:
        content = json.load(f)

    for i in content["types_of"]:
        if i["good-luck"] == structure["good-luck"]:
            return i["name"]
    raise Exception("Configuration file error")

def randomBasemap(theme: str, spec_path: Optional[str]) -> str:
    try_time = 0
    if spec_path:
        _p = f"{FORTUNE_PATH}/img"
        return os.path.join(_p, spec_path)
    else:
        if theme == "random":
            __p = f"{FORTUNE_PATH}/img"
            while True:
                picked_theme = random.choice(os.listdir(__p))
                if MainThemeEnable[picked_theme] == True:
                    break
                else:
                    try_time = try_time+1

                if try_time == len(MainThemeEnable):
                    break

            _p = os.path.join(__p, picked_theme)
        else:
            _p = os.path.join(f"{FORTUNE_PATH}/img", theme)
        return os.path.join(_p, random.choice(os.listdir(_p)))

def drawing(theme: str, spec_path: Optional[str], user_id: str, group_id: str) -> Path:
    fontPath = {
        "title": f"{FORTUNE_PATH}/font/Mamelon.otf",
        "text": f"{FORTUNE_PATH}/font/sakura.ttf",
    }
    imgPath = randomBasemap(theme, spec_path)
    img = Image.open(imgPath)
    # Draw title
    draw = ImageDraw.Draw(img)
    text = copywriting()
    title = getTitle(text)
    text = text["content"]
    font_size = 45
    color = "#F5F5F5"
    image_font_center = (140, 99)
    ttfront = ImageFont.truetype(fontPath["title"], font_size)
    font_length = ttfront.getsize(title)
    draw.text(
        (
            image_font_center[0] - font_length[0] / 2,
            image_font_center[1] - font_length[1] / 2,
        ),
        title,
        fill=color,
        font=ttfront,
    )
    # Text rendering
    font_size = 25
    color = "#323232"
    image_font_center = [140, 297]
    ttfront = ImageFont.truetype(fontPath["text"], font_size)
    result = decrement(text)
    if not result[0]:
        return
    textVertical = []
    for i in range(result[0]):
        font_height = len(result[i + 1]) * (font_size + 4)
        textVertical = vertical(result[i + 1])
        x = int(
            image_font_center[0]
            + (result[0] - 2) * font_size / 2
            + (result[0] - 1) * 4
            - i * (font_size + 4)
        )
        y = int(image_font_center[1] - font_height / 2)
        draw.text((x, y), textVertical, fill=color, font=ttfront)
    # Save
    outPath = exportFilePath(imgPath, user_id, group_id)
    img.save(outPath)
    return outPath

def exportFilePath(originalFilePath: str, user_id: str, group_id: str) -> Path:
    dirPath = f"{FORTUNE_PATH}/out"
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    return (
        Path(originalFilePath).parent.parent.parent
        / "out"
        / f"{user_id}_{group_id}.png"
    )

def decrement(text):
    length = len(text)
    cardinality = 9
    if length > 4 * cardinality:
        return [False]
    numberOfSlices = 1
    while length > cardinality:
        numberOfSlices += 1
        length -= cardinality
    result = [numberOfSlices]
    length = len(text)
    if numberOfSlices == 2:
        # Optimize for two columns
        space = " "
        if length % 2 == 0:
            # even
            fillIn = space * int(9 - length / 2)
            return [
                numberOfSlices,
                text[: length // 2] + fillIn,
                fillIn + text[length // 2 :],
            ]

        else:
            # odd number
            fillIn = space * int(9 - (length + 1) / 2)
            return [
                numberOfSlices,
                text[: int((length + 1) / 2)] + fillIn,
                fillIn + space + text[int((length + 1) / 2) :],
            ]
    for i in range(numberOfSlices):
        if i == numberOfSlices - 1 or numberOfSlices == 1:
            result.append(text[i * cardinality :])
        else:
            result.append(text[i * cardinality : (i + 1) * cardinality])
    return result


def vertical(str):
    list = list(str)
    return "\n".join(list)

# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw

import random
from io import BytesIO

from .utils import getAvatar, checkFolder

# 爬的概率 越大越容易爬 取值区间 [0, 100]
creep_limit = 80

_avatar_size = 139
_center_pos = (17, 180)

# _toppest = 164
# _downest = 504

base_path = './creep'


async def throw(qq):
    throwed_who = qq

    avatar_img_url = 'http://q1.qlogo.cn/g?b=qq&nk={QQ}&s=640'.format(QQ=throwed_who)

    res = await getAvatar(avatar_img_url)
    avatar = Image.open(BytesIO(res)).convert('RGBA')
    avatar = await get_circle_avatar(avatar, _avatar_size)

    rotate_angel = random.randrange(0, 360)

    throw_img = Image.open(base_path + '/image/throw.jpg').convert('RGBA')
    throw_img.paste(avatar.rotate(rotate_angel), _center_pos, avatar.rotate(rotate_angel))
    await checkFolder(base_path + '/image/avatar')
    throw_img.save(f'{base_path}/image/avatar/{throwed_who}.png')

    return base_path + f'/image/avatar/{throwed_who}.png'



async def creep(qq):
    creeped_who = qq
    id = random.randint(0, 53)

    whetherToClimb = await randomClimb()

    if not whetherToClimb:
        return base_path + '/image/不爬.jpg'

    avatar_img_url = 'http://q1.qlogo.cn/g?b=qq&nk={QQ}&s=640'.format(QQ=creeped_who)
    res = await getAvatar(avatar_img_url)
    avatar = Image.open(BytesIO(res)).convert('RGBA')
    avatar = await get_circle_avatar(avatar, 100)

    creep_img = Image.open(f'{base_path}/image/pa/爬{id}.jpg').convert('RGBA')
    creep_img = creep_img.resize((500, 500), Image.ANTIALIAS)
    creep_img.paste(avatar, (0, 400, 100, 500), avatar)
    await checkFolder(base_path + '/image/avatar')
    creep_img.save(f'{base_path}/image/avatar/{creeped_who}_creeped.png')

    return base_path + f'/image/avatar/{creeped_who}_creeped.png'


async def get_circle_avatar(avatar, size):
    avatar.thumbnail((size, size))

    scale = 5
    mask = Image.new('L', (size*scale, size*scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask.resize((size, size), Image.ANTIALIAS)

    ret_img = avatar.copy()
    ret_img.putalpha(mask)

    return ret_img


async def randomClimb():
    randomNumber = random.randint(1, 100)
    if randomNumber < creep_limit:
        return True
    return False






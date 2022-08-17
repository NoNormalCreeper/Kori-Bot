import requests
import aiohttp
import json

url = "https://api.imlazy.ink/mcapi/"


def generate_result(data: dict) -> str:
    if data is None:
        return "获取信息失败..."
    host = data["host"]
    status = data["status"]
    players_max = data["players_max"]
    players_online = data["players_online"]
    version = data["version"]
    if status == "离线":
        return f"地址: {host}\n状态: {status}"
    return (
        f"地址: {host}\n状态: {status}\n玩家: {players_online} / {players_max}\n游戏版本: {version}"
    )


async def get_server_status(ip: str) -> str:
    params = {
        "host": ip,
        "type": 'json'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                data = await response.text()
                return generate_result(json.loads(data))
    except:
        return None


async def get_status_image(ip: str) -> str:
    params = {
        "host": ip,
        "type": 'image',
        "getbg" : '8.jpg'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                return await response.read()
    except:
        return None

# print(get_server_status("play.hypixel.net"))
# print(get_status_image("play.hypixel.net"))

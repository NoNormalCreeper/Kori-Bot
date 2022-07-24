import requests
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


def get_server_status(ip: str) -> str:
    params = {
        "host": ip,
        "type": 'json'
    }
    try:
        response = requests.get(url=url, params=params, timeout=10)
        data = json.loads(response.text)
        return generate_result(data)
    except:
        return None


def get_status_image(ip: str) -> str:
    params = {
        "host": ip,
        "type": 'image',
        "getbg" : '8.jpg'
    }
    try:
        response = requests.get(url=url, params=params, stream=True, timeout=10)
        return response.content
    except:
        return None

# print(get_server_status("play.hypixel.net"))
# print(get_status_image("play.hypixel.net"))

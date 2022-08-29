import requests
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class DownloadError(Exception):
    pass

def get_preset(file_path: Path, file_type: str) -> None:
    if file_type == "GREATING":
        url = "https://cdn.jsdelivr.net/gh/KafCoppelia/nonebot_plugin_what2eat@beta.1/nonebot_plugin_what2eat/resource/greating.json"


    elif file_type == "MENU":
        url = "https://cdn.jsdelivr.net/gh/KafCoppelia/nonebot_plugin_what2eat@beta.1/nonebot_plugin_what2eat/resource/data.json"

    if data := requests.get(url).json():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({}))
            f.close()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    if not file_path.exists():
        raise DownloadError
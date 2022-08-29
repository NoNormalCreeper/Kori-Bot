import os
import json
from pathlib import Path
from datetime import datetime

from ATRI.service import Service, ServiceTools
from ATRI.exceptions import ReadFileError, load_error

MANAGE_DIR = Path(".") / "data" / "database" / "manege"
ESSENTIAL_DIR = Path(".") / "data" / "database" / "essential"
os.makedirs(MANAGE_DIR, exist_ok=True)
os.makedirs(ESSENTIAL_DIR, exist_ok=True)

TRACK_BACK_FORMAT = """Track ID：{track_id}
Prompt: {prompt}
Time: {time}
{content}
""".strip()

__doc__ = """控制bot的各项服务"""


class Manage(Service):
    def __init__(self):
        Service.__init__(self, "管理", __doc__, True)

    @staticmethod
    def _load_block_user_list() -> dict:
        """
        文件结构：
        {
            "Block user ID": {
                "time": "Block time"
            }
        }
        """
        file_name = "block_user.json"
        path = MANAGE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            return {}
        try:
            data = json.loads(path.read_bytes())
        except BaseException:
            data = {}
        return data

    @staticmethod
    def _save_block_user_list(data: dict) -> None:
        file_name = "block_user.json"
        path = MANAGE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))

    @staticmethod
    def _load_block_group_list() -> dict:
        """
        文件结构：
        {
            "Block group ID": {
                "time": "Block time"
            }
        }
        """
        file_name = "block_group.json"
        path = MANAGE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            return {}

        try:
            data = json.loads(path.read_bytes())
        except BaseException:
            data = {}
        return data

    @staticmethod
    def _save_block_group_list(data: dict) -> None:
        file_name = "block_group.json"
        path = MANAGE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))

    @classmethod
    def block_user(cls, user_id: str) -> bool:
        data = cls._load_block_user_list()
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[user_id] = {"time": now_time}
        try:
            cls._save_block_user_list(data)
            return True
        except BaseException:
            return False

    @classmethod
    def unblock_user(cls, user_id: str) -> bool:
        data: dict = cls._load_block_user_list()
        if user_id not in data:
            return False

        try:
            data.pop(user_id)
            cls._save_block_user_list(data)
            return True
        except BaseException:
            return False

    @classmethod
    def block_group(cls, group_id: str) -> bool:
        data = cls._load_block_group_list()
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[group_id] = {"time": now_time}
        try:
            cls._save_block_group_list(data)
            return True
        except BaseException:
            return False

    @classmethod
    def unblock_group(cls, group_id: str) -> bool:
        data: dict = cls._load_block_group_list()
        if group_id not in data:
            return False

        try:
            data.pop(group_id)
            cls._save_block_group_list(data)
            return True
        except BaseException:
            return False

    @staticmethod
    def control_global_service(service: str, is_enabled: bool) -> bool:
        """
        Only SUPERUSER.
        """
        try:
            data = ServiceTools().load_service(service)
        except BaseException:
            return False
        data["enabled"] = is_enabled
        ServiceTools().save_service(data, service)
        return True

    @staticmethod
    def control_user_service(service: str, user_id: str, is_enabled: bool) -> bool:
        """
        Only SUPERUSER.
        """
        try:
            data = ServiceTools().load_service(service)
        except BaseException:
            return False
        temp_list: list = data.get("disable_user", [])

        if is_enabled:
            try:
                temp_list.remove(user_id)
            except BaseException:
                return False
        elif user_id in temp_list:
            return True

        else:
            temp_list.append(user_id)

        data["disable_user"] = temp_list
        ServiceTools().save_service(data, service)
        return True

    @staticmethod
    def control_group_service(service: str, group_id: str, is_enabled: bool) -> bool:
        """
        SUPERUSER and GROUPADMIN or GROUPOWNER.
        Only current group.
        """
        try:
            data = ServiceTools().load_service(service)
        except:
            return False
        temp_list: list = data.get("disable_group", [])

        if is_enabled:
            try:
                temp_list.remove(group_id)
            except:
                return False
        elif group_id in temp_list:
            return True

        else:
            temp_list.append(group_id)

        data["disable_group"] = temp_list
        ServiceTools().save_service(data, service)
        return True

    @staticmethod
    def load_friend_apply_list() -> dict:
        file_name = "friend_add.json"
        path = ESSENTIAL_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            return {}

        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        return data

    @staticmethod
    def save_friend_apply_list(data: dict) -> None:
        file_name = "friend_add.json"
        path = ESSENTIAL_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))

    @staticmethod
    def load_invite_apply_list() -> dict:
        file_name = "group_invite.json"
        path = ESSENTIAL_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            return {}

        try:
            data = json.loads(path.read_bytes())
        except BaseException:
            data = {}
        return data

    @staticmethod
    def save_invite_apply_list(data: dict) -> None:
        file_name = "group_invite.json"
        path = ESSENTIAL_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))

    @staticmethod
    async def track_error(track_id: str) -> str:
        try:
            data = load_error(track_id)
        except ReadFileError:
            return "请检查ID是否正确..."

        prompt = data.get("prompt", "ignore")
        time = data.get("time", "ignore")
        content = data.get("content", "ignore")

        return TRACK_BACK_FORMAT.format(
            track_id=track_id, prompt=prompt, time=time, content=content
        )

import os
import json
import shutil
import asyncio
from datetime import datetime
from pydantic.main import BaseModel
from random import choice, randint
from pathlib import Path

import nonebot
from nonebot.permission import SUPERUSER
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    FriendRequestEvent,
    GroupRequestEvent,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupAdminNoticeEvent,
    GroupBanNoticeEvent,
    GroupRecallNoticeEvent,
    FriendRecallNoticeEvent,
    MessageSegment,
    Message,
)

import ATRI
from ATRI.service import Service
from ATRI.log import logger as log
from ATRI.config import BotSelfConfig
from ATRI.utils import MessageChecker
from ATRI.utils.apscheduler import scheduler


driver = ATRI.driver()
bots = nonebot.get_bots()


ESSENTIAL_DIR = Path(".") / "data" / "database" / "essential"
MANEGE_DIR = Path(".") / "data" / "database" / "manege"
TEMP_PATH = Path(".") / "data" / "temp"
os.makedirs(ESSENTIAL_DIR, exist_ok=True)
os.makedirs(MANEGE_DIR, exist_ok=True)
os.makedirs(TEMP_PATH, exist_ok=True)


@driver.on_startup
async def startup():
    log.info(f"Now running: {ATRI.__version__}")
    log.info("アトリは、高性能ですから！")


@driver.on_shutdown
async def shutdown():
    log.info("Thanks for using.")


@run_preprocessor
async def _check_block(event: MessageEvent):
    user_file = "block_user.json"
    path = MANEGE_DIR / user_file
    if not path.is_file():
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps({}))

    try:
        data = json.loads(path.read_bytes())
    except BaseException:
        data = {}

    user_id = event.get_user_id()
    if user_id in data:
        raise IgnoredException(f"Block user: {user_id}")

    if isinstance(event, GroupMessageEvent):
        group_file = "block_group.json"
        path = MANEGE_DIR / group_file
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        try:
            data = json.loads(path.read_bytes())
        except BaseException:
            data = {}

        group_id = str(event.group_id)
        if group_id in data:
            raise IgnoredException(f"Block group: {user_id}")


class FriendRequestInfo(BaseModel):
    user_id: str
    comment: str
    time: str
    is_approve: bool


class GroupRequestInfo(BaseModel):
    user_id: str
    comment: str
    time: str
    is_approve: bool


__doc__ = """
对bot基础/必须请求进行处理
"""


class Essential(Service):
    def __init__(self):
        Service.__init__(self, "基础部件", __doc__)


friend_add_event = Essential().on_request("好友添加", "好友添加检测")


@friend_add_event.handle()
async def _friend_add(bot: Bot, event: FriendRequestEvent):
    """
    存储文件结构：
    {
        "Apply code": {
            "user_id": "User ID",
            "comment": "Comment content"
            "time": "Time",
            "is_approve": bool  # Default: False
        }
    }
    """
    file_name = "friend_add.json"
    path = ESSENTIAL_DIR / file_name
    if not path.is_file():
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps({}))
        data = {}

    apply_code = event.flag
    apply_comment = event.comment
    user_id = event.get_user_id()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = json.loads(path.read_bytes())
    data[apply_code] = FriendRequestInfo(
        user_id=user_id, comment=apply_comment, time=now_time, is_approve=False
    ).dict()
    with open(path, "w", encoding="utf-8") as w:
        w.write(json.dumps(data, indent=4))

    repo = (
        "咱收到一条好友请求...\n"
        f"请求人：{user_id}\n"
        f"申请信息：{apply_comment}\n"
        f"申请码：{apply_code}\n"
        "Tip：好友申请 帮助"
    )
    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=superuser, message=repo)


group_invite_event = Essential().on_request("邀请入群", "被邀请入群检测")


@group_invite_event.handle()
async def _group_invite(bot: Bot, event: GroupRequestEvent):
    """
    存储文件结构：
    {
        "Apply code": {
            "user_id": "User ID",
            "comment": "Comment content"
            "time": "Time",
            "is_approve": bool  # Default: False
        }
    }
    """
    file_name = "group_invite.json"
    path = ESSENTIAL_DIR / file_name
    if not path.is_file():
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps({}))
        data = {}

    apply_code = event.flag
    apply_comment = event.comment
    user_id = event.get_user_id()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = json.loads(path.read_bytes())
    data[apply_code] = GroupRequestInfo(
        user_id=user_id, comment=apply_comment, time=now_time, is_approve=False
    ).dict()
    with open(path, "w", encoding="utf-8") as w:
        w.write(json.dumps(data, indent=4))

    repo = (
        "咱收到一条群聊邀请请求...\n"
        f"请求人：{user_id}\n"
        f"申请信息：{apply_comment}\n"
        f"申请码：{apply_code}\n"
        "Tip：群聊邀请 帮助"
    )
    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=superuser, message=repo)


group_member_event = Essential().on_notice("群成员变动", "群成员变动检测")


@group_member_event.handle()
async def _group_member_join(bot: Bot, event: GroupIncreaseNoticeEvent):
    await asyncio.sleep(randint(1, 6))
    msg = "好欸！事新人！\n" f"在下 {choice(list(BotSelfConfig.nickname))} 哒!w!"
    await group_member_event.finish(msg)


@group_member_event.handle()
async def _group_member_left(bot: Bot, event: GroupDecreaseNoticeEvent):
    await asyncio.sleep(randint(1, 6))
    await group_member_event.finish("呜——有人跑了...")


group_admin_event = Essential().on_notice("群管理变动", "群管理变动检测")


@group_admin_event.handle()
async def _group_admin_event(bot: Bot, event: GroupAdminNoticeEvent):
    if not event.is_tome():
        return

    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(
            user_id=int(superuser), message=f"好欸！主人！我在群 {event.group_id} 成为了管理！！"
        )


group_ban_event = Essential().on_notice("群禁言变动", "群禁言变动检测")


@group_ban_event.handle()
async def _group_ban_event(bot: Bot, event: GroupBanNoticeEvent):
    if not event.is_tome():
        return

    if event.duration:
        msg = (
            "那个..。，主人\n"
            f"咱在群 {event.group_id} 被 {event.operator_id} 塞上了口球...\n"
            f"时长...是 {event.duration} 秒"
        )
    else:
        msg = "好欸！主人\n" f"咱在群 {event.group_id} 的口球被 {event.operator_id} 解除了！"
    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=int(superuser), message=msg)


_acc_recall = True


recall_event = Essential().on_notice("撤回事件", "撤回事件检测")


@recall_event.handle()
async def _recall_group_event(bot: Bot, event: GroupRecallNoticeEvent):
    if event.is_tome():
        return

    if not _acc_recall:
        return

    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except BaseException:
        return

    user = event.user_id
    group = event.group_id
    repo = repo["message"]

    try:
        m = recall_msg_dealer(repo)
    except:
        if check := MessageChecker(repo).check_cq_code:
            return

        else:
            m = repo
    msg = f"主人，咱拿到了一条撤回信息！\n{user}@[群:{group}]\n撤回了\n{m}"
    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=int(superuser), message=Message(msg))


@recall_event.handle()
async def _recall_private_event(bot: Bot, event: FriendRecallNoticeEvent):
    if event.is_tome():
        return

    if not _acc_recall:
        return

    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except BaseException:
        return

    user = event.user_id
    repo = repo["message"]

    try:
        m = recall_msg_dealer(repo)
    except:
        if check := MessageChecker(repo).check_cq_code:
            return

        else:
            m = repo
    msg = f"主人，咱拿到了一条撤回信息！\n{user}@[私聊]撤回了\n{m}"
    for superuser in BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=int(superuser), message=Message(msg))


rej_recall = Essential().on_command("拒绝撤回", "拒绝撤回信息", permission=SUPERUSER)


@rej_recall.handle()
async def _():
    global _acc_recall
    _acc_recall = False
    await rej_recall.finish("已拒绝撤回信息...")


acc_recall = Essential().on_command("接受撤回", "接受撤回信息", permission=SUPERUSER)


@acc_recall.handle()
async def _():
    global _acc_recall
    _acc_recall = True
    await acc_recall.finish("现在可以接受撤回信息啦！")


@scheduler.scheduled_job("interval", name="清除缓存", minutes=30, misfire_grace_time=5)
async def _clear_cache():
    try:
        shutil.rmtree(TEMP_PATH)
        os.makedirs(TEMP_PATH, exist_ok=True)
    except Exception:
        log.warning("清除缓存失败，请手动清除：data/temp")


def recall_msg_dealer(msg: dict) -> str:
    temp_m = []

    for i in msg:
        _type = i.get("type", "idk")
        _data = i.get("data", "idk")
        if _type == "text":
            temp_m.append(_data["text"])
        elif _type == "image":
            url = _data["url"]
            if check := MessageChecker(url).check_image_url:
                temp_m.append(MessageSegment.image(url))
            else:
                temp_m.append(f"[该图片可能包含非法内容，源url：{url}]")
        elif _type == "face":
            temp_m.append(MessageSegment.face(_data["id"]))
        else:
            temp_m.append(f"[未知类型信息：{_data}]")

    return str().join(map(str, temp_m))

from datetime import datetime
from sqlmodel import select, or_
from typing_extensions import Literal
from typing import Iterable, List, Optional, Union, overload

from nonebot.adapters.onebot.v11 import Message
from nonebot_plugin_datastore import create_session

from .model import MessageRecord
from .message import deserialize_message


@overload
async def get_message_records(
    plain_text: Literal[True],
    user_ids: Optional[Iterable[str]] = None,
    group_ids: Optional[Iterable[str]] = None,
    exclude_user_ids: Optional[Iterable[str]] = None,
    exclude_group_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Literal['private', 'group']] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> List[str]:
    ...


@overload
async def get_message_records(
    plain_text: Literal[False] = ...,
    user_ids: Optional[Iterable[str]] = None,
    group_ids: Optional[Iterable[str]] = None,
    exclude_user_ids: Optional[Iterable[str]] = None,
    exclude_group_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Literal['private', 'group']] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> List[Message]:
    ...


async def get_message_records(
    plain_text: bool = False,
    user_ids: Optional[Iterable[str]] = None,
    group_ids: Optional[Iterable[str]] = None,
    exclude_user_ids: Optional[Iterable[str]] = None,
    exclude_group_ids: Optional[Iterable[str]] = None,
    message_type: Optional[Literal['private', 'group']] = None,
    time_start: Optional[datetime] = None,
    time_stop: Optional[datetime] = None,
) -> Union[List[str], List[Message]]:
    """
    :说明:

      获取消息记录

    :参数:

      * ``plain_text: bool = False``: 为真则返回字符串数组，否则返回 Message 数组
      * ``user_ids: Optional[Iterable[str]]``: 用户列表，为空表示所有用户
      * ``group_ids: Optional[Iterable[str]]``: 群组列表，为空表示所有群组
      * ``exclude_user_ids: Optional[Iterable[str]]``: 不包含的用户列表，为空表示不限制
      * ``exclude_group_ids: Optional[Iterable[str]]``: 不包含的群组列表，为空表示不限制
      * ``message_type: Optional[Literal['private', 'group']]``: 消息类型，可选值：'private' 和 'group'，为空表示所有类型
      * ``time_start: Optional[datetime]``: 起始时间，UTC 时间，为空表示不限制起始时间
      * ``time_stop: Optional[datetime]``: 结束时间，UTC 时间，为空表示不限制结束时间

    :返回值:

      * ``Union[List[str], List[Message]]``: 消息列表
    """

    whereclause = []
    if user_ids:
        whereclause.append(
            or_(*[MessageRecord.user_id == user_id for user_id in user_ids])
        )
    if group_ids:
        whereclause.append(
            or_(*[MessageRecord.group_id == group_id for group_id in group_ids])
        )
    if exclude_user_ids:
        whereclause.extend(
            MessageRecord.user_id != user_id for user_id in exclude_user_ids
        )

    if exclude_group_ids:
        whereclause.extend(
            MessageRecord.group_id != group_id
            for group_id in exclude_group_ids
        )

    if message_type:
        whereclause.append(MessageRecord.detail_type == message_type)
    if time_start:
        whereclause.append(MessageRecord.time >= time_start)
    if time_stop:
        whereclause.append(MessageRecord.time <= time_stop)

    statement = select(MessageRecord).where(*whereclause)
    async with create_session() as session:
        records: List[MessageRecord] = (await session.exec(statement)).all()

    if plain_text:
        return [record.alt_message for record in records]
    else:
        return [deserialize_message(record.message) for record in records]

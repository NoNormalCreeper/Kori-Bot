from nonebot.rule import Rule
from nonebot.typing import T_State


def validate_status(database) -> Rule:
    """
    :说明:

      通过数据库查询判断事件处于交互环境

    :数据库:

      ``status``
        Columns: [message_type: TEXT, session_id: INT PIRMARY KEY, command_active: INT]

      若用户不在数据库 -> 直接返回 False
      若用户存在数据库 -> 以 ``command_active`` 作为规则过滤依据
    """

    async def _validate_status(bot: "Bot", event: "Event", state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        await database.connect()
        if status := await database.fetch_val(f"SELECT command_active FROM status WHERE session_id = {event.get_session_id()}"):
            await database.disconnect()
            return bool(status)
        await database.disconnect()
        return False

    return Rule(_validate_status)
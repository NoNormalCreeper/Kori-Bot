import re
import traceback
from nonebot.rule import Rule, to_me
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_message
from nonebot.params import CommandArg, EventMessage, EventPlainText, State
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    Message,
    MessageSegment,
)

from .shindan_list import add_shindan, del_shindan, set_shindan, get_shindan_list
from .shindanmaker import make_shindan, get_shindan_title


__help__plugin_name__ = 'shindan'
__des__ = 'shindanmaker趣味占卜'
__cmd__ = '''
发送“占卜列表”查看可用占卜
发送“{占卜名} {名字}”使用占卜
'''.strip()
__example__ = '''
人设生成 小Q
'''.strip()
__usage__ = f'{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}'


add_usage = """Usage:
添加占卜 {id} {指令}
如：添加占卜 917962 人设生成"""

del_usage = """Usage:
删除占卜 {id}
如：删除占卜 917962"""

set_usage = """Usage:
设置占卜 {id} {mode}
设置占卜输出模式：'text' 或 'image'(默认)
如：设置占卜 360578 text"""

cmd_sd = on_command(
    '占卜', aliases={'shindan', 'shindanmaker'}, rule=to_me(), block=True, priority=8
)
cmd_ls = on_command('占卜列表', aliases={'可用占卜'}, block=True, priority=8)
cmd_add = on_command('添加占卜', permission=SUPERUSER, block=True, priority=8)
cmd_del = on_command('删除占卜', permission=SUPERUSER, block=True, priority=8)
cmd_set = on_command('设置占卜', permission=SUPERUSER, block=True, priority=8)


@cmd_sd.handle()
async def _():
    await cmd_sd.finish(__usage__)


@cmd_ls.handle()
async def _():
    sd_list = get_shindan_list()

    if not sd_list:
        await cmd_ls.finish('尚未添加任何占卜')

    await cmd_ls.finish(
        f'可用占卜：\n'
        + '\n'.join([f"{s['command']}（{s['title']}）" for s in sd_list.values()])
    )


@cmd_add.handle()
async def _(msg: Message = CommandArg()):
    arg = msg.extract_plain_text().strip()
    if not arg:
        await cmd_add.finish(add_usage)

    args = arg.split()
    if len(args) != 2 or not args[0].isdigit():
        await cmd_add.finish(add_usage)

    id = args[0]
    command = args[1]
    title = await get_shindan_title(id)
    if not title:
        await cmd_add.finish('找不到该占卜，请检查id')

    sd_list = get_shindan_list()
    if id in sd_list:
        await cmd_add.finish('该占卜已存在')
    if command in sd_list.values():
        await cmd_add.finish('该指令已存在')

    if add_shindan(id, command, title):
        await cmd_add.finish(f'成功添加占卜“{title}”，可通过“{command} 名字”使用')


@cmd_del.handle()
async def _(msg: Message = CommandArg()):
    arg = msg.extract_plain_text().strip()
    if not arg:
        await cmd_del.finish(del_usage)

    if not arg.isdigit():
        await cmd_del.finish(del_usage)

    id = arg
    sd_list = get_shindan_list()
    if id not in sd_list:
        await cmd_del.finish('不存在该占卜')

    if del_shindan(id):
        await cmd_del.finish('成功删除该占卜')


@cmd_set.handle()
async def _(msg: Message = CommandArg()):
    arg = msg.extract_plain_text().strip()
    if not arg:
        await cmd_set.finish(set_usage)

    args = arg.split()
    if len(args) != 2 or not args[0].isdigit() or args[1] not in ['text', 'image']:
        await cmd_set.finish(set_usage)

    id = args[0]
    mode = args[1]
    sd_list = get_shindan_list()
    if id not in sd_list:
        await cmd_set.finish('不存在该占卜')

    if set_shindan(id, mode):
        await cmd_set.finish('设置成功')


def sd_handler() -> Rule:
    async def handle(
        bot: Bot,
        event: MessageEvent,
        msg: Message = EventMessage(),
        msg_text: str = EventPlainText(),
        state: T_State = State(),
    ) -> bool:
        async def get_name(command: str) -> str:
            name = ''
            for msg_seg in msg:
                if msg_seg.type == 'at':
                    assert isinstance(event, GroupMessageEvent)
                    info = await bot.get_group_member_info(
                        group_id=event.group_id, user_id=msg_seg.data['qq']
                    )
                    name = info.get('card', '') or info.get('nickname', '')
                    break
            if not name:
                name = msg_text[len(command) :].strip()
            if not name:
                name = event.sender.card or event.sender.nickname
            return name

        sd_list = get_shindan_list()
        sd_list = sorted(
            sd_list.items(), reverse=True, key=lambda items: items[1]['command']
        )
        for id, s in sd_list:
            command = s['command']
            if msg_text.startswith(command):
                name = await get_name(command)
                state['id'] = id
                state['name'] = name
                state['mode'] = s.get('mode', 'image')
                return True
        return False

    return Rule(handle)


sd_matcher = on_message(sd_handler(), priority=9)


@sd_matcher.handle()
async def _(state: T_State = State()):
    id = state.get('id')
    name = state.get('name')
    mode = state.get('mode')
    try:
        res = await make_shindan(id, name, mode)
    except:
        logger.warning(traceback.format_exc())
        await sd_matcher.finish('出错了，请稍后再试')

    if isinstance(res, str):
        img_pattern = r'((?:http|https)://\S+\.(?:jpg|jpeg|png|gif|bmp|webp))'
        message = Message()
        msgs = re.split(img_pattern, res)
        for msg in msgs:
            message.append(
                MessageSegment.image(msg) if re.match(img_pattern, msg) else msg
            )
        await sd_matcher.finish(message)
    elif isinstance(res, bytes):
        await sd_matcher.finish(MessageSegment.image(res))

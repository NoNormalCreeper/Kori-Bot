import re
import random
from nonebot.log import logger
from nonebot import on_command
from nonebot.params import State, CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GROUP, Message, GroupMessageEvent

roll = on_command("rd", aliases={"Roll", "掷骰子", "掷骰"}, permission=GROUP, priority=10, block=True)

@roll.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg(), state: T_State=State()):
    args = args.extract_plain_text().strip().split()
    # logger.info(args)
    if not args:
        pass
    elif args and len(args) == 1:
        state['rd'] = args[0]
    else:
        await roll.finish('参数错误QAQ')

@roll.got('rd', prompt='请掷骰子: [x]d[y]')
async def handle_roll(bot: Bot, event: GroupMessageEvent, state: T_State=State()):
    _roll = state['rd']
    if re.match(r'^\d+[d]\d+$', _roll):
        # <x>d<y>
        dice_info = _roll.split('d')
        dice_num = int(dice_info[0])
        dice_side = int(dice_info[1])
    elif re.match(r'^[d]\d+$', _roll):
        # d<x>
        dice_num = 1
        dice_side = int(_roll[1:])
    elif re.match(r'^\d+$', _roll):
        # Any number
        dice_num = 1
        dice_side = int(_roll)
    else:
        await roll.finish(f'格式不对呢, 请重新输入: /rd <x>d<y>:')

    # 加入一个趣味的机制
    if random.randint(1, 100) == 99:
        await roll.finish(f'【彩蛋】骰子之神似乎不看好你, 你掷出的骰子全部消失了😥')
    if dice_num > 1024 or dice_side > 1024:
        await roll.finish(f'【错误】谁没事干扔那么多骰子啊😅')
    if dice_num <= 0 or dice_side <= 0:
        await roll.finish(f'【错误】你掷出了不存在的骰子, 只有上帝知道结果是多少🤔')
    dice_result = 0
    for i in range(dice_num):
        this_dice_result = random.choice(range(dice_side)) + 1
        dice_result += this_dice_result
    await roll.finish(f'你掷出了{dice_num}个{dice_side}面骰子, 点数为【{dice_result}】')

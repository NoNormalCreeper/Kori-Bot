from urllib import response
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    MessageSegment,
    Message,
    Event
)
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.params import Depends, CommandArg, State, Arg, ArgPlainText
from quart import got_websocket_exception
from .utils import is_number, get_message_at
from nonebot.log import logger
from .data_source import (
    russian_manager, max_bet_gold, 
    number_estimated_format, number_format, resolve_formated_number
)
from .fx import f
from .poem import check, getQuestion
# from .lottery import *
import random
from .math_question import *
from .words import *


__zx_plugin_name__ = "俄罗斯轮盘"

__plugin_usage__ = """俄罗斯轮盘帮助：
    开启游戏：装弹 [子弹数] ?[金额](默认200金币) ?[at](指定决斗对象，为空则所有群友都可接受决斗)
        示例：装弹 1 10
    接受对决：接受对决/拒绝决斗
    开始对决：开枪 ?[子弹数](默认1)（轮流开枪，根据子弹数量连开N枪械，30秒未开枪另一方可使用‘结算’命令结束对决并胜利）
    结算：结算（当某一方30秒未开枪，可使用该命令强行结束对决并胜利）
    我的战绩：我的战绩
    排行榜：金币排行/胜场排行/败场排行/欧洲人排行/慈善家排行
    【注：同一时间群内只能有一场对决】
"""

scheduler = require("nonebot_plugin_apscheduler").scheduler


sign = on_command("轮盘签到", permission=GROUP, priority=5, block=True)

russian = on_command(
    "俄罗斯轮盘", aliases={"装弹", "俄罗斯转盘"}, permission=GROUP, priority=5, block=True
)

accept = on_command(
    "接受对决", aliases={"接受决斗", "接受挑战"}, permission=GROUP, priority=5, block=True
)

refuse = on_command(
    "拒绝对决", aliases={"拒绝决斗", "拒绝挑战"}, permission=GROUP, priority=5, block=True
)

shot = on_command(
    "开枪", aliases={"咔", "嘭", "嘣"}, permission=GROUP, priority=5, block=True
)

settlement = on_command("结算", permission=GROUP, priority=5, block=True)

record = on_command("我的战绩", permission=GROUP, priority=5, block=True)

lottery = on_command("lottery", aliases={}, permission=GROUP, priority=5, block=True)

addmoney = on_command("addmoney", aliases={}, priority=5, block=True)

fx = on_command("fx", aliases={}, permission=GROUP, priority=5, block=True)

stock = on_command("stock", aliases={}, permission=GROUP, priority=5, block=True)

math = on_command("math", aliases={"口算"}, permission=GROUP, priority=5, block=True)

word = on_command("word", aliases={}, permission=GROUP, priority=5, block=True)

russian_rank = on_command(
    "胜场排行",
    aliases={"金币排行", "胜利排行", "败场排行", "失败排行", "欧洲人排行", "慈善家排行"},
    permission=GROUP,
    priority=5,
    block=True,
)

my_gold = on_command("我的金币", aliases={"mycoin"}, permission=GROUP, priority=5, block=True)

dap = on_command("dap", aliases={}, permission=GROUP, priority=5, block=True)

lottery = on_command("lottery", aliases={}, permission=GROUP, priority=5, block=True)

pay = on_command("pay", aliases={}, permission=GROUP, priority=5, block=True)

poem = on_command("poem", aliases={}, permission=GROUP, priority=5, block=True)

# answer = on_regex("[0-4]+", permission=GROUP, priority=5)

@sign.handle()
async def _(event: GroupMessageEvent):
    msg, gold = russian_manager.sign(event)
    await sign.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金币")


@accept.handle()
async def _(event: GroupMessageEvent):
    msg = russian_manager.accept(event)
    await accept.send(msg, at_sender=True)


@refuse.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = await russian_manager.refuse(bot, event)
    await refuse.send(msg, at_sender=True)


@settlement.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = russian_manager.settlement(event)
    await settlement.send(msg, at_sender=True)
    await russian_manager.end_game(bot, event)


async def get_bullet_num(
    event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()
):
    msg = arg.extract_plain_text().strip()
    if state["bullet_num"]:
        return state
    if msg in ["取消", "算了"]:
        await russian.finish("已取消操作...")
    try:
        if russian_manager.check_game_is_start(event.group_id):
            await russian.finish("决斗已开始...", at_sender=True)
    except KeyError:
        pass
    if not is_number(msg):
        await russian.reject("输入子弹数量必须是数字啊喂！")
    if int(msg) < 1 or int(msg) > 6:
        await russian.reject("子弹数量必须大于0小于7！")
    return {**state, "bullet_num": int(msg)}


@russian.handle()
async def _(
    bot: Bot,
    event: GroupMessageEvent,
    state: T_State = State(),
    arg: Message = CommandArg(),
):
    msg = arg.extract_plain_text().strip()
    if msg == "帮助":
        await russian.finish(__plugin_usage__)
    try:
        _msg = await russian_manager.check_current_game(bot, event)
    except KeyError:
        pass
    if msg:
        msg = msg.split()
        if len(msg) == 1:
            msg = msg[0]
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state["bullet_num"] = int(msg)
        else:
            money = msg[1].strip()
            msg = msg[0].strip()
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state["bullet_num"] = int(msg)
            if is_number(money) and 0 < int(money) <= max_bet_gold:
                state["money"] = int(money)
    state["at"] = get_message_at(event.json())


@russian.got("bullet_num", prompt="请输入装填子弹的数量！(最多6颗)")
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State = Depends(get_bullet_num)
):
    bullet_num = state["bullet_num"]
    at_ = state["at"]
    money = state["money"] if state.get("money") else 200
    user_money = russian_manager.get_user_data(event)["gold"]
    if bullet_num < 0 or bullet_num > 6:
        await russian.reject("子弹数量必须大于0小于7！速速重新装弹！")
    if money > max_bet_gold:
        await russian.finish(f"太多了！单次金额不能超过{max_bet_gold}！", at_sender=True)
    if money > user_money:
        await russian.finish("你没有足够的钱支撑起这场挑战", at_sender=True)

    player1_name = event.sender.card or event.sender.nickname

    if at_:
        at_ = at_[0]
        at_player_name = await bot.get_group_member_info(
            group_id=event.group_id, user_id=int(at_)
        )
        at_player_name = (
            at_player_name["card"]
            if at_player_name["card"]
            else at_player_name["nickname"]
        )
        msg = (
            f"{player1_name} 向 {MessageSegment.at(at_)} 发起了决斗！请 {at_player_name} 在30秒内回"
            f"复‘接受对决’ or ‘拒绝对决’，超时此次决斗作废！"
        )
    else:
        at_ = 0
        msg = "若30秒内无人接受挑战则此次对决作废【首次游玩请发送 ’俄罗斯轮盘帮助‘ 来查看命令】"

    _msg = russian_manager.ready_game(event, msg, player1_name, at_, money, bullet_num)
    await russian.send(_msg)


@shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    count = arg.extract_plain_text().strip()
    if is_number(count):
        count = int(count)
        if count > 7 - russian_manager.get_current_bullet_index(event):
            await shot.finish(
                f"你不能开{count}枪，大于剩余的子弹数量，"
                f"剩余子弹数量：{7 - russian_manager.get_current_bullet_index(event)}"
            )
    else:
        count = 1
    await russian_manager.shot(bot, event, count)


@record.handle()
async def _(event: GroupMessageEvent):
    user = russian_manager.get_user_data(event)
    await record.send(
        f"俄罗斯轮盘\n"
        f'胜利场次：{user["win_count"]}\n'
        f'失败场次：{user["lose_count"]}\n'
        f'赚取金币：{user["make_gold"]}\n'
        f'输掉金币：{user["lose_gold"]}',
        at_sender=True,
    )


@russian_rank.handle()
async def _(event: GroupMessageEvent, state: T_State = State()):
    msg = await russian_manager.rank(state["_prefix"]["raw_command"], event.group_id)
    await russian_rank.send(msg)


@my_gold.handle()
async def _(event: GroupMessageEvent):
    gold = russian_manager.get_user_data(event)["gold"]
    if "rough" in event.raw_message:
        gold = number_estimated_format(gold)
    else:
        gold = number_format(gold)
    await my_gold.send(f"你还有 {gold} 枚金币", at_sender=True)


# @lottery.handle()
# async def lottery_handle(event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
#     possibility = 0.1
#     user_money = russian_manager.get_user_data(event)["gold"]
#     arg = arg.extract_plain_text()
#     if arg:
#         arg = int(arg)
#     else:
#         arg = 1
#     spent_money = arg*20

#     if spent_money <= user_money:

#         await lottery.send("Successfully bought {0} pieces of lottery ticket by {1} coins!".format(arg,spent_money), 
#         at_sender=True)

def calc_distance(times: int):
    dist = 0
    for i in range(times+1):
        dist += random.randint(300, 1500) / 1000
    return round(dist, 2)

@dap.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    gold = russian_manager.get_user_data(event)["gold"]
    if gold > 0:
        russian_manager._waste_data_handle(event.user_id, event.group_id, 1)
        p_list = [0, 1, 3, 4, 7, 11, 14, 16, 17, 17.5]
        rand = random.randint(0, 175)
        times = -1
        msg = "你扔出了一个硬币，"
        for i in range(1, 9):
            if (p_list[i-1]*10 <= rand) and (rand < p_list[i]*10):
                times = i-1
                # break
        if times == -1:
            times = random.randint(8, 80)
            dist = calc_distance(times)
            msg += "它居然弹了 {0} 次！！在距离你 {1} 米处才沉了下去！！！".format(times,dist)
        else:
            dist = calc_distance(times)
            if times == 0:
                msg += f"它在你面前 {dist} 米处直接沉下去了"
            else:
                msg += f"它弹了 {times} 次，在你距离你 {dist} 米处沉了下去"
    else:
        msg = "你没有金币，不能扔金币！"
    await dap.send(message=('\n'+msg), at_sender=True)


@lottery.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
    ban_groups = ["277620613"]
    if str(event.group_id) in ban_groups:
        await lottery.finish("😓 此功能已被管理员禁用")
    
    possibility = 0.03
    msg = ""
    gold_per_ticket = 50
    user_gold = russian_manager.get_user_data(event)["gold"]
    arg = arg.extract_plain_text()
    award_path = data_source.russian_path / "data" / "russian" / "award.txt"
    if arg:
        arg = int(arg)
    else:
        arg = 1
    spent_gold = arg*gold_per_ticket
    if arg > 8:
        await lottery.finish("\n买那么多干嘛 >_<", at_sender=True)
    if user_gold >= spent_gold:
        msg += "\n💸 你花 {1} 金币购买了 {0} 张彩票 \n".format(arg, spent_gold)
        with open(award_path) as f:
            # award_sheet = json.load(f)
            try:
                award_gold = int(f.read().strip())
            except:
                award_gold = 0
        with open(award_path, 'w') as f:
            russian_manager._waste_data_handle(event.user_id, event.group_id, spent_gold)
            if random.randint(0, 100) < (1-((1-possibility)**arg))*100:
                won_gold = (award_gold+spent_gold)*0.9
                russian_manager._earn_data_handle(event.user_id, event.group_id, round(won_gold))
                msg += f"🎉 噫！好！你中了！！！你赢得了 {number_format(won_gold)} 金币！"
                logger.info("{0} won {1} coins from lottery tickets.".format(event.user_id, won_gold))
                f.write("0")
            else:
                msg += f"😐 很可惜，没有中奖呢...\n💰 当前奖池： {number_format(award_gold+spent_gold)} 金币"
                f.write(str(award_gold+spent_gold))
    else:
        msg = "你买不起彩票！"
    await lottery.send(message=msg, at_sender=True)

@pay.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
    sender = event.user_id
    group_id = event.group_id
    arg = arg.extract_plain_text().split(' ')
    transfer_money = arg[1]
    if arg[0]:
        receiver = arg.data["qq"]
    else:
        pay.finish("Pay to who? Air?")
    at_ = state["at"][0]
    at_player_name = await bot.get_group_member_info(
            group_id=event.group_id, user_id=int(at_)
        )
    at_player_name = (
            at_player_name["card"]
            if at_player_name["card"]
            else at_player_name["nickname"]
        )
    if russian_manager.get_user_data(event)["gold"] > transfer_money:
        russian_manager._waste_data_handle(sender, group_id, transfer_money)
        russian_manager._earn_data_handle(receiver, group_id, transfer_money)
        await pay.send(" successfully paid {0} coins to {1} !".format(transfer_money, at_player_name), at_sender=True)
    else:
        await pay.send(" You don't have enough money!", at_sender=True)

@addmoney.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
    if str(event.user_id) in ["2560359315"]:
        args = arg.extract_plain_text().split(' ')
        russian_manager._earn_data_handle(int(args[0]), event.group_id, int(args[1]))
        await addmoney.send(f"成功向用户 {args[1]} 添加了 {args[0]} 金币")
    else:
        await addmoney.send("😅 你不是超级管理员哦")


@fx.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
    await fx.finish("😓 该功能已被管理员禁用")
    arg = arg.extract_plain_text().strip()
    x = int(arg) if arg else 50
    if x > 0 and x <= 500:
        tmp = f(x)
        y = tmp[0]
        msg = '\n'+tmp[1]
        msg += '\n💰 Your {0} coins have become {1} coins!'.format(x,y)
        russian_manager._waste_data_handle(event.user_id, event.group_id, x)
        russian_manager._earn_data_handle(event.user_id, event.group_id, y)
        if russian_manager.get_user_data(event)["gold"] < 0:
            msg += '\n⚠ You have less than 0 coin now!'
        logger.info("{0}'s {1} -> {2} ".format(event.user_id, x, y))
        await fx.send(msg, at_sender=True)
    else:
        await fx.send("Range error!")


@poem.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    question = getQuestion(event.user_id)
    msg = '\n'+question
    args = args.extract_plain_text()
    if args:    
        matcher.set_arg("answer", args)     # never run
    await poem.send(msg, at_sender=True)

# @answer.handle()
# async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
#     user_answer = event.raw_message
#     user_answer = user_answer.strip()
#     if check(user_answer):
#         award = random.randint(5,15)
#         russian_manager._earn_data_handle(event.user_id, event.group_id, award)


@poem.got("ans", prompt="请回答...")
async def _(bot: Bot, event: Event, matcher: Matcher, ans: Message = Arg(), answer: str = ArgPlainText("ans")):
    answer = answer.strip()
    # answer = state["answer"]
    award = random.randint(2,30)
    if check(answer, event.user_id):
        russian_manager._earn_data_handle(event.user_id, event.group_id, award)
        msg = f"\n✔ 你赢得了 {award} 金币！"
    else:
        russian_manager._waste_data_handle(event.user_id, event.group_id, award)
        msg = f"\n❌ 扣掉你 {award} 金币"
    await poem.send(msg, at_sender=True)


@math.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    question = getMathQuestion(event.user_id)
    msg = '\n'+question
    args = args.extract_plain_text()
    if args:    
        matcher.set_arg("answer", args)     # never run
    await math.send(msg, at_sender=True)

@math.got("ans", prompt="请回答...")
async def _(bot: Bot, event: Event, matcher: Matcher, ans: Message = Arg(), answer: str = ArgPlainText("ans")):
    answer = answer.strip().replace(' ', '')
    # answer = state["answer"]
    try:
        answer = int(answer)
        answer = str(answer)
    except:
        await math.reject("请输入一个数字而不是其他东西！")
    award = random.randint(2,60)
    responce = checkMathAnswer(event.user_id, answer)
    if not responce:
        russian_manager._earn_data_handle(event.user_id, event.group_id, award)
        msg = f"\n✔ 你赢得了 {award} 金币！"
    else:
        russian_manager._waste_data_handle(event.user_id, event.group_id, award)
        msg = f"\n❌ 扣掉你 {award} 金币，正确答案是 {response}"
    await math.send(msg, at_sender=True)

@word.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    question = getWordQuestion(event.user_id)
    msg = '\n'+question
    args = args.extract_plain_text()
    if args:    
        matcher.set_arg("answer", args)     # never run
    await word.send(msg, at_sender=True)

@word.got("ans", prompt="请回答...")
async def _(bot: Bot, event: Event, matcher: Matcher, ans: Message = Arg(), answer: str = ArgPlainText("ans")):
    answer = answer.strip().replace(' ', '')
    # answer = state["answer"]
    if answer.upper() not in ['A','B','C','D']:
        await word.reject("Please input a right letter!")
    award = random.randint(2,20)
    responce = checkWordAnswer(event.user_id, answer)
    if not responce:
        russian_manager._earn_data_handle(event.user_id, event.group_id, award)
        msg = f"\n✔ 你赢得了 {award} 金币！"
    else:
        russian_manager._waste_data_handle(event.user_id, event.group_id, award)
        msg = f"\n❌ 扣掉你 {award} 金币，正确答案是 {response}"
    await word.send(msg, at_sender=True)


@stock.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text()
    args = args.strip().split()
    user_id = event.user_id
    group_id = event.group_id
    money_per_stock = russian_manager._check_stock_handle()["money_per_stock"]
    percent = russian_manager._check_stock_handle()["percent"]
    color_block = '🟥' if ('-' not in percent) else '🟩'
    if args:
        if args[0] == "buy":
            try:
                number = args[1]
            except:
                number = 1
            number = resolve_formated_number(number)
            if number*money_per_stock <= russian_manager.get_user_data(event)["gold"]:
                russian_manager._buy_stock_handle(user_id, group_id, number)
                await stock.finish(
                    "\n🧾 成功买入 {0} 股！花费：{3} 金币\n你现在有 {4} 股\n{5}当前行情： {1} 金币, {2}".format(
                        number_format(number), money_per_stock, percent, 
                        number_format(number*money_per_stock), 
                        number_format(russian_manager.get_user_data(event)["stock"]), 
                        color_block
                    ),at_sender=True
                )
            else:
                await stock.finish("\n😦 你买不起这么多！", at_sender=True)
        elif args[0] == "sell":
            try:
                number = args[1]
            except:
                number = 1
            number = resolve_formated_number(number)
            if number <= russian_manager.get_user_data(event)["stock"]:
                russian_manager._sell_stock_handle(user_id, group_id, number)
                await stock.finish(
                    "\n🧾 成功售出 {0} 股！获得：{3} 金币\n你现在还剩 {4} 股\n{5} 当前行情：{1} 金币, {2}".format(
                        number_format(number), money_per_stock, percent, 
                        number_format(number*money_per_stock), 
                        number_format(russian_manager.get_user_data(event)["stock"]), 
                        color_block
                    ),at_sender=True
                )
            else:
                await stock.finish("\n😦 你没有那么多股！", at_sender=True)
        elif args[0] == "me":
            await stock.finish("\n你现在持有 {0} 股".format(
                number_format(russian_manager.get_user_data(event)["stock"])), 
                at_sender=True)
        elif args[0] == "price":
            await stock.finish("{2} 当前行情： {0} 金币, {1}".format(
                    money_per_stock, percent, color_block),
                    )
    else:
        await stock.finish("{2} 当前行情： {0} 金币, {1}".format(
                    money_per_stock, percent, color_block),
                    )

@scheduler.scheduled_job(
    "cron",
    hour="8-21",    # 08:00:00 - 21:59:30
    minute="*",
    second="*/30"
)
async def change_price():
    russian_manager._price_change_handle()

@scheduler.scheduled_job(
    "cron",
    hour=7,
    minute=59,
)
async def start_stock():
    russian_manager._start_stock_handle()


# 重置每日签到
@scheduler.scheduled_job(
    "cron", 
    hour="*/4",
    minute=0,
)
async def _():
    russian_manager.reset_gold()
    logger.info("每日轮盘签到重置成功...")

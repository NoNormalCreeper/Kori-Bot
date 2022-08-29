from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot import logger, on_command
import requests, json
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

# sv = Service('小鸡词典')
help_txt = """
小鸡词典使用指北
xxx是什么梗 查询xxx的含义
""".strip()
host = 'https://api.jikipedia.com/go/search_entities'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'content-type': 'application/json',
    'referer': 'https://jikipedia.com/',
    'Client': 'web',
    'Client-Version': '2.6.10r'
}
# freq = FreqLimiter(60)


# @sv.on_fullmatch(('小鸡词典', '小鸡字典'))
# async def help(bot, event: CQEvent):
#     await bot.send(event, help_txt)

sv = on_command("梗")

@sv.handle()
async def query(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    # keyword = event.message.replace("梗", "")
    # for i in ['!','/','！',' ', '\n', '\r', '\t']:
    #    keyword = keyword.replace(i, '')
    keyword = args.extract_plain_text()
    if not keyword:
        return
    request_data = {'page': 1, 'phrase': keyword, 'size': 60}
    gid = event.group_id
    try:
        resp = requests.post(host, headers=header, json=request_data, timeout=10)
        res = json.loads(resp.text)
    except Exception as ex:
        logger.exception(ex)
        await sv.finish('查询错误，请重试')

    if 'data' not in res:
        msg = res['message']
        content = msg['content']
        await sv.finish(content)

    # freq.start_cd(gid)

    data = res['data']
    if len(data) == 0:
        await sv.finish(f'没有查询到关于{keyword}的结果')

    definitions = {}
    for el in data:
        if el['category'] != 'definition':
            continue
        if len(el['definitions']) == 0:
            continue
        definitions |= el['definitions'][0]
        break

    if not definitions:
        await sv.finish(f'没有查询到关于{keyword}的结果')

    term = definitions['term']
    title = term['title']
    result_txt = f'没有找到{keyword}，我猜你可能在找{title}\n' if title != keyword else ''
    result_txt += definitions['plaintext']
    await sv.finish(result_txt)

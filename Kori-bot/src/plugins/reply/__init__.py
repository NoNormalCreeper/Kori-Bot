from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command, on_keyword
import time

help=on_command("help")
ping=on_command("ping")
morning=on_keyword("早")
bing=on_command("bing")
baidu=on_command("baidu")
bd=on_command("bd")
goo=on_command("google")

help_content='''====Kori Bot指令列表====
可输入'/help [指令编号]'获取详细帮助
（输入指令请加上前缀'/'）
(1)色图/涩图/setu/无内鬼： 获取涩图
(2)sx： 查询缩写可能代表的含义
(3)点歌： 点歌
(4)saying： 一言
(5)mcs： 查询Minecraft服务器状态
(6)喜报: 生成喜报
(7)ping: 检查积气人是否正在运行
(8)tih: 历史上的今天
'''
help_dict={'1':'/setu  获取涩图\n/下载涩图  下载涩图','2':'/sx <缩写内容>','3':'/点歌 [歌曲名称]',
           '4':'/saying  获取一言','5':'/mcs [服务器IP]  查询mc服务器运行状态','6':'/喜报 [内容]  生成指定内容的喜报','7':'/ping  如果正常，她会回复\'pong!\'','8':'/tih [条数]  查看“历史上的今天”'}

@help.handle()
async def help_handle(bot: Bot, event: Event, state: T_State):
    # await help.send(help_content)
    #获取把命令头部分去除后的消息内容，也就是命令的具体内容。
    cmd = str(event.get_message()).strip()
    #如果命令的具体内容不为空，就将cmd存入state。
    if cmd:
        state['cmd'] = cmd 
        print(state['cmd'])
        await help.send(help_dict[state['cmd']])
    else:
        await help.send(help_content)
        # time.sleep(30)
        # await help.delete_msg()


@ping.handle()
async def ping_handle(bot: Bot, event: Event, state: T_State):
    await help.send("pong!")

@morning.handle()
async def morning_handle(bot: Bot, event: Event, state: T_State):
    await morning.send("早！")

@bing.handle()
async def bing_handle(bot: Bot, event: Event, state: T_State):
    word = str(event.get_message()).strip()
    if word:
        await bing.send("https://cn.bing.com/search?q="+word)
    else:
        await bing.send("https://cn.bing.com/")

@baidu.handle()
async def baidu_handle(bot: Bot, event: Event, state: T_State):
    word = str(event.get_message()).strip()
    if word:
        await baidu.send("https://www.baidu.com/s?wd="+word)
    else:
        await baidu.send("https://www.baidu.com/")

@bd.handle()
async def bd_handle(bot: Bot, event: Event, state: T_State):
    word = str(event.get_message()).strip()
    if word:
        await bd.send("https://www.baidu.com/s?wd="+word)
    else:
        await bd.send("https://www.baidu.com/")

@goo.handle()
async def goo_handle(bot: Bot, event: Event, state: T_State):
    word = str(event.get_message()).strip()
    if word:
        await goo.send("https://www.google.com/search?q="+word)
    else:
        await goo.send("https://www.google.com/")

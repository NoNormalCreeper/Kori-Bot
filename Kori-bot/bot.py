#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from os import path

#初始化nb
nonebot.init()
app = nonebot.get_asgi()
#连接驱动
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
#加载插件(除此处其他配置不建议更改)
nonebot.load_builtin_plugins()
nonebot.load_plugins('src/plugins')
# nonebot.load_plugin("nonebot_plugin_setu")
# nonebot.load_plugins(
#         'D:\\Files\\coding\\Kori-bot\\Kori-bot\\repeater'
#     )
# nonebot.load_plugins(
#         'D:\\Files\\coding\\Kori-bot\\Kori-bot\\GoodMorning'
#     )
# nonebot.load_plugins(
#         'D:\\Files\\coding\\Kori-bot\\Kori-bot'
#     )


#启动bot
if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")

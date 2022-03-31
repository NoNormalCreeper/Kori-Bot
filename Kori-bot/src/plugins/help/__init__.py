#{"author":"HornCopper","version":"v1.0","name":"help","admin":"主命令(0)$部分子命令(1~10)","aliases":"帮助","desc":"获取帮助的插件。$+help <command/keyword>"}!
from pathlib import Path
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event
from nonebot.params import Arg, CommandArg, ArgPlainText
from tabulate import tabulate
from aiocqhttp import MessageSegment as ms 
from .picture import main as pic
import os
import re
import json
import sys
sys.path.append("/root/Kori-Bot/Kori-bot/src/tools")
from tools.permission import checker, error

help = on_command("help", aliases={"帮助"}, priority=1)
css="""
<style>
            ::-webkit-scrollbar 
            {
            display: none;
                
            }
            table { 
            border-collapse: collapse; 
                } 
              table, th, td { 
                border: 1px solid rgba(0,0,0,0.05); 
                font-size: 0.8125rem; 
                font-weight: 500; 
              } 
              th, td { 
              padding: 15px; 
              text-align: left; 
              }
              @font-face
              {
                  font-family: Minecraft;
                  src: url("file:///root/nb/src/plugins/help/unifont.ttf");
              }
            </style>"""
path = "./src/plugins/"
final_plugin_information_file_path = {}
name = {}
version = {}
author = {}
json_ = {}
desc = {}
admin = {}
aliases = {}
table = []
html_path = "./src/plugins/help/help.html"
imgPath = "./src/plugins/help/help.png"

@help.handle()
async def help_(matcher: Matcher, event: Event, args: Message = CommandArg()):
    try:
        cmd = args.extract_plain_text()
        if cmd != True:
            pass
        else:
            os.system(f"rm -rf {html_path}")
            all_cmd = os.listdir(path)
            for plugin in all_cmd:
                final_plugin_information_file_path[plugin] = path + plugin + "/info.json"
                file = open(final_plugin_information_file_path[plugin],mode="r")
                cache = file.read()
                file.close()
                json_[plugin] = cache
                json_[plugin] = json.loads(json_[plugin])
                cache = json_[plugin]
                name[plugin] = cache["name"]
                version[plugin] = cache["version"]
                author[plugin] = cache["author"]
                desc[plugin] = cache["desc"]
                admin[plugin] = cache["admin"]
                aliases[plugin] = cache["aliases"]
            table.append(["插件名称","插件版本","插件介绍","插件作者","权限等级","别名"])
            for i in all_cmd:
                table.append([name[i],version[i],desc[i],author[i],admin[i],aliases[i]])
            if os.path.exists(html_path) == False:
                msg = str(tabulate(table,headers="firstrow",tablefmt="html"))
                table.clear()
                html = "<div style=\"font-family:Minecraft\">" + msg.replace("$", "<br>") + "</div>"+css
                file0 = open(html_path,mode="w")
                file0.write(html)
                file0.close()
            if os.path.exists(imgPath) == False:
                pic_status = pic()
                if pic_status == "200 OK":
                    now_path = os.getcwd()
                    help_path = Path("./src/plugins/help/help.png").as_uri()
                    pic_msg = ms.image(help_path)
                    msg = "帮助信息出来了喵~\n以下为帮助信息：" + pic_msg
                else:
                    msg = f"啊咧，帮助图片生成失败了，请联系管理员尝试清除缓存。\n错误信息如下：{pic_status}"
            else:
                now_path = os.getcwd()
                help_path = Path("./src/plugins/help/help.png").as_uri()
                pic_msg = ms.image(help_path)
                msg = "帮助信息出来了喵~\n以下为帮助信息：" + pic_msg
            await help.finish(msg)
            return
    except:
        await help.finish("在线命令手册: \nhttp://u6.gg/kpxbr")



# import socket
# import codecs
# class mcstatus:
#     def __init__(self,hostname,port,timeout = 0.6):
#         self.hostname = hostname
#         self.timeout = timeout
#         self.port = port
#     def getserverinfo(self):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         ip = socket.gethostbyname(self.hostname)
#         try:
#             s.settimeout(self.timeout)
#             s.connect((ip,self.port))
#             s.send(bytearray([0xFE, 0x01]))
#             data_raw = s.recv(1024)
#             s.close()
#             #这个编码太神秘了
#             data = data_raw.decode('cp437').split('\x00\x00\x00')
#             #print codecs.utf_16_be_decode(data_raw[1:])[0] #(utf-16)这个可以看到MOTD和其他信息
#             info = {}
#             info['version'] = data[2].replace("\x00","")
#             info['online_players'] = data[4].replace("\x00","")
#             info['max_players'] = data[5].replace("\x00","")
#             return (True,info)
#         except socket.error:
#             return (False)

# if __name__ == '__main__':
#     app = mcstatus('mc.hypixel.net',25565)
#     print(app.getserverinfo())

from json import encoder
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command
import requests
import json
import time
import math

mcs=on_command("mcs")

@mcs.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    result,url="",""
    url="https://mcapi.us/server/status?ip="
    ip = str(event.get_message()).strip()
    ts = time.time()

    if ip:
        if ':' in ip:
            # url=ip
            x=ip.split(':')
            url+=x[0]
            url+="&port="
            url+=x[1]
        else:
            url+=ip
            url+="&port=25565"
        url+="&encode=json"

        req=requests.get(url)
        # print(str(requests.get(url)))
        # print(requests.get(url))
        # req.encoding="utf-8"
        # res=requests.get(url)
        js_=req.text
        js=json.loads(js_)
        # js=json.loads(js_)

        result+=(js["status"]+"!\n")
        result+=(js["motd"])
        if js["motd"]!="":
            result+="\n"
        result+=ip
        result+=("\n在线状态: "+str(js["online"]))
        result+=("\n在线玩家: "+str((js["players"])["now"])+"/"+str((js["players"])["max"]))
        result+=(("\n版本: ")+(js["server"])["name"])
        diff=str(format(((ts-int(js["last_updated"]))/60), '.2f'))
        result+=(("\n(更新于"+diff+"min前)"))

        await mcs.send(result)

    else:
        await mcs.send("缺少参数'IP'，请检查后重新输入指令！")

# {"status":"success","online":true,"motd":"","favicon":"data:image/png;base64,略","error":null,"players":{"max":2021,"now":553,"sample":[]},"server":{"name":"Waterfall 1.8.x, 1.9.x, 1.10.x, 1.11.x, 1.12.x, 1.13.x, 1.14.x, 1.15.x, 1.16.x, 1.17.x","protocol":756},"last_updated":"1629699780","last_online":"1629699780","duration":2493701595}

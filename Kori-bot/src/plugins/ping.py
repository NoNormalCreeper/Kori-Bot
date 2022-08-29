from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event, Message
import random

ping = on_command("ping", priority=1)
pong = on_command("pong", priority=1)

pong_words = ["Sorry but I can't \"Ping!\"","Do you think I will \"Ping!\" ?","PONG!!!!!!","You are not allowed to \"Pong!\""]

@ping.handle()
async def ping_handle(bot: Bot, event: Event, matcher: Matcher):
	delay=random.randint(10,800)
	result = f"Pong!   ({delay} ms)"
	await ping.send(result)

@pong.handle()
async def pong_handle(bot: Bot, event: Event, matcher: Matcher):
	await pong.send(pong_words[random.randint(0,len(pong_words)-1)])

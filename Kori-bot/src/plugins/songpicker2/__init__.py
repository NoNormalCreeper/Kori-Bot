# import nonebot
from .data_source import dataGet, dataProcess
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Bot, Event, Message
from nonebot.params import State, Arg, CommandArg, ArgPlainText
from nonebot import on_command
from nonebot.matcher import Matcher


def removeprefix(string, prefix):
    if not isinstance(string, str) or not isinstance(prefix, str):
        raise TypeError('Param value type error')
    return string[len(prefix):] if string.startswith(prefix) else string

def removesuffix(string, suffix):
    if not isinstance(string, str) or not isinstance(suffix, str):
        raise TypeError('Param value type error')
    return string[:-len(suffix)] if string.endswith(suffix) else string


dataget = dataGet()

songpicker = on_command("点歌",aliases={'song'})


@songpicker.handle()
async def handle_first_receive( matcher: Matcher, bot: Bot, event: Event, args: Message = CommandArg()):
    if args := args.extract_plain_text():
        matcher.set_arg("songName", args)  # 如果用户发送了参数则直接赋值


@songpicker.got("songName", prompt="歌名是？")
async def handle_songName(bot: Bot, event: Event, args: Message = CommandArg()):
    songName = state["songName"]
    songIdList = await dataget.songIds(songName=songName)
    if songIdList is None:
        await songpicker.reject("没有找到这首歌，请发送其它歌名！")
    songInfoList = []
    for songId in songIdList:
        songInfoDict = await dataget.songInfo(songId)
        songInfoList.append(songInfoDict)
    songInfoMessage = await dataProcess.mergeSongInfo(songInfoList)
    await songpicker.send(songInfoMessage)
    state["songIdList"] = songIdList


@songpicker.got("songNum")
async def handle_songNum(bot: Bot, event: Event):
    songIdList = state["songIdList"]
    songNum = int(str((state["songNum"])))

    if songNum >= len(songIdList):
        await songpicker.reject("数字序号错误，请重选")

    selectedSongId = songIdList[songNum]

    await songpicker.send(MessageSegment.music("163", int(selectedSongId)))

    songCommentsDict = await dataget.songComments(songId=selectedSongId)
    state["songCommentsDict"] = songCommentsDict
    songCommentsMessage = await dataProcess.mergeSongComments(songCommentsDict)
    commentContent = "下面为您播送热评：\n" + songCommentsMessage
    await songpicker.send(commentContent)



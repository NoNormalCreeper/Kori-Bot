import os
import docker
import base64
import random
from databases import Database

import nonebot
from nonebot import on_command, on_message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.rule import Rule

from .exceptions import NoMatchContainerError, ContainerRunTimeError
from .models import validate_status


config = nonebot.get_driver().config

client = docker.from_env()
image_name = config.plugin_ipypreter_image or 'python:latest'
current_path = os.path.dirname(os.path.realpath(__file__))
db_name = 'store.db'
db_path = os.path.join(current_path, db_name)
database = Database(f"sqlite:///{db_path}")


# 检查 Docker 是否存在 `image_name`
for container in client.images.list():
    if image_name in container.tags:
        break
    if container == client.images.list()[-1]:
        raise NoMatchContainerError('There is no python image in docker, please check your setting or go to document: https://github.com')

async def call_docker(cmd_b64encoded: str):
    command = f'import base64;cmd=base64.b64decode("{cmd_b64encoded}".encode()).decode();exec(cmd)'
    return client.containers.run('python', auto_remove=True,
                                 command=['python', '-c', command])



ipypreter = on_command('python', aliases={'python3'}, block=True)

@ipypreter.handle()
async def _handle_init(bot: Bot, event: Event, state: T_State):

    await database.connect()
    user_status = await database.fetch_val(f"SELECT command_active FROM status WHERE session_id = {event.get_session_id()}")

    # 用户不存在
    if user_status == None:
        await database.execute("INSERT INTO status (message_type, session_id, command_active) VALUES (:mgt,:sid,:cat)",
                                {'mgt': str(event.get_event_name()),
                                'sid': int(event.get_session_id()),
                                'cat': 1})
        await database.execute("INSERT INTO commands (session_id) VALUES (:sid)",
                                {'sid': int(event.get_session_id())})
        await bot.send(message='* 进入交互环境，输入 exit 退出', event=event)

    # 用户存在，判断状态
    if user_status == 0: 
        await database.execute(f"UPDATE status SET command_active = 1 WHERE session_id = {event.get_session_id()}")
        await bot.send(message='进入交互环境，输入 exit 退出', event=event)
    elif user_status == 1:
        await bot.send(message='已处于交互环境，输入 exit 退出', event=event)

    await database.disconnect()



filtr = on_message(rule=validate_status(database), priority=100)

@filtr.handle()
async def _handle_filtr(bot: Bot, event: Event):
    """
    ``store.db`` Tables 说明

      ``status`` 储存用户状态
        Columns: [message_type: TEXT, session_id: INT PRIMARY KEY, command_active: INT]

      ``commands`` 储存会话的所有命令
        Columns: [session_id: INT PRIMARY KEY, commands: TEXT]
    """

    def text_encode(f: str) -> str:
        return base64.b64encode(f.encode()).decode()

    def text_decode(f: str) -> str:
        return base64.b64decode(f.encode()).decode()

    next_cmd = event.get_plaintext().strip().strip('\n')

    await database.connect()

    if next_cmd in ['exit', 'exit()', 'quit']:
        await database.execute(f"UPDATE commands SET commands = NULL WHERE session_id = {event.get_session_id()}")
        await database.execute(f"UPDATE status SET command_active = 0 WHERE session_id = {event.get_session_id()}")
        await database.disconnect()
        await filtr.finish('Stopped')

    if next_cmd == 'history':
        if msg := await database.fetch_val(f"SELECT commands FROM commands WHERE session_id = {event.get_session_id()}"):
            await bot.send(message=f'{text_decode(msg)}', event=event)
        else:
            await bot.send(message='无历史输入', event=event)
        await database.disconnect()
        await filtr.finish()

    db_query_cmds = await database.fetch_val(f"SELECT commands FROM commands WHERE session_id = {event.get_session_id()}")

    hsh = random.getrandbits(128)
    splitor = f'{hsh:032x}'
    split_cmd = f"print('{splitor}')"

    if db_query_cmds:
        db_query_cmds = text_decode(db_query_cmds)
        store_cmds = text_encode('\n'.join([db_query_cmds, next_cmd]))
        exec_cmds = '\n'.join([db_query_cmds, split_cmd, next_cmd])
    else:
        store_cmds = text_encode(next_cmd)
        exec_cmds = next_cmd

    try:
        stdout = await call_docker(text_encode(exec_cmds))
    except docker.errors.ContainerError:
        stdout = None
        await database.disconnect()
        await filtr.finish('\n'.join(['容器执行错误', f'命令：{next_cmd} 执行错误']))
    else:
        await database.execute(f"UPDATE commands SET commands = '{store_cmds}' WHERE session_id = {event.get_session_id()}")

    await database.disconnect()

    # 把输出分割，取最后一条作为结果发送出去
    msg = stdout.decode().split(splitor)[-1].strip('\n') if stdout else None

    if msg:
        await bot.send(message=f"{msg}", event=event)
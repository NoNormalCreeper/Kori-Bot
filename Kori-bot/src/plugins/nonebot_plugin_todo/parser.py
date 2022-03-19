from nonebot.rule import ArgumentParser

from .handle import *

todo_parser = ArgumentParser("todo")

npm_subparsers = todo_parser.add_subparsers()

list_parser = npm_subparsers.add_parser("list", help="show todo list")
list_parser.set_defaults(handle=handle_list)

add_parser = npm_subparsers.add_parser("add", help="add todo")
add_parser.add_argument("job")
add_parser.add_argument("cron")
add_parser.add_argument("message")
add_parser.set_defaults(handle=handle_add)

remove_parser = npm_subparsers.add_parser("remove", help="remove todo")
remove_parser.add_argument("job")
remove_parser.set_defaults(handle=handle_remove)

pause_parser = npm_subparsers.add_parser("pause", help="pause todo")
pause_parser.add_argument("job")
pause_parser.set_defaults(handle=handle_pause)

resume_parser = npm_subparsers.add_parser("resume", help="resume todo")
resume_parser.add_argument("job")
resume_parser.set_defaults(handle=handle_resume)

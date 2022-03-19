import time
from argparse import Namespace

from .data import *


def handle_list(args: Namespace) -> Namespace:

    todo_list = get_todo_list(args.user_id, args.group_id)

    if todo_list == {}:
        args.message = "当前会话暂无待办事项列表!"
    else:
        args.message = "\n".join(
            f"[{'o' if todo_list[job]['enable'] else 'x'}] {job}" for job in todo_list
        )

    return args


def handle_add(args: Namespace) -> Namespace:

    if args.group_id and not args.is_admin:
        args.message = "管理待办事项列表需要群管理员权限！"
    else:
        add_todo_list({args.job: {"cron": args.cron, "message": args.message, "enable": True}}, args.user_id, args.group_id)

        args.message = f"待办事项 {args.job} 添加成功！"

    return args


def handle_remove(args: Namespace) -> Namespace:

    if args.group_id and not args.is_admin:
        args.message = "管理待办事项列表需要群管理员权限！"
    else:
        remove_todo_list(args.job, args.user_id, args.group_id)
        args.message = f"待办事项 {args.job} 删除成功！"

    return args


def handle_pause(args: Namespace) -> Namespace:

    if args.group_id and not args.is_admin:
        args.message = "管理待办事项列表需要群管理员权限！"
    else:
        pause_todo_list(args.job, args.user_id, args.group_id)
        args.message = f"待办事项 {args.job} 暂停成功！"

    return args


def handle_resume(args: Namespace) -> Namespace:

    if args.group_id and not args.is_admin:
        args.message = "管理待办事项列表需要群管理员权限！"
    else:
        resume_todo_list(args.job, args.user_id, args.group_id)
        args.message = f"待办事项 {args.job} 恢复成功！"

    return args


def handle_scheduler(args: Namespace = Namespace()) -> Namespace:
    def format_crontab(crontab: str, default: List[int]) -> List[int]:
        if crontab == "*":
            return default
        elif "," in crontab:
            return list(int(i) for i in crontab.split(","))
        elif "-" in crontab:
            return list(
                range(int(crontab.split("-")[0]), int(crontab.split("-")[0]) + 1)
            )
        elif "/" in crontab:
            return list(filter(lambda x: x % int(crontab[3:]) == 0, default))
        else:
            return [int(crontab)]

    def check_time(job: Dict[str, Any]) -> bool:

        localtime = time.localtime(time.time())

        cron = job["cron"].split()
        minute = format_crontab(cron[0], list(range(60)))
        hour = format_crontab(cron[1], list(range(24)))
        day = format_crontab(cron[2], list(range(1, 31)))
        month = format_crontab(cron[3], list(range(1, 13)))
        day_of_week = format_crontab(cron[4], list(range(7)))

        if (
            job["enable"]
            and localtime.tm_min in minute
            and localtime.tm_hour in hour
            and localtime.tm_mday in day
            and localtime.tm_mon in month
            and localtime.tm_wday in day_of_week
        ):
            return True
        else:
            return False

    todo_list = get_todo_list()

    args.jobs = []

    for group_id in todo_list["group"]:
        for job in todo_list["group"][group_id]:
            if check_time(todo_list["group"][group_id][job]):
                args.jobs.append(
                    {
                        "user_id": None,
                        "group_id": group_id,
                        "message": todo_list["group"][group_id][job]["message"],
                    }
                )

    for user_id in todo_list["user"]:
        for job in todo_list["user"][user_id]:
            if check_time(todo_list["user"][user_id][job]):
                args.jobs.append(
                    {
                        "user_id": user_id,
                        "group_id": None,
                        "message": todo_list["user"][user_id][job]["message"],
                    }
                )

    return args

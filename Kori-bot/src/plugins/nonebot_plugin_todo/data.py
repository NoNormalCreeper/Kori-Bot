import yaml
from pathlib import Path
from typing import Optional, Union, Any, List, Dict

_DATA_PATH = Path() / "data" / "todo" / "todo_list.yml"


def get_todo_list(
    user_id: Optional[int] = None, group_id: Optional[int] = None
) -> Optional[Dict[str, Any]]:

    todo_list = __load_todo_list()

    if user_id:
        if user_id not in todo_list["user"]:
            todo_list["user"][user_id] = {}
        tmp_todo_list = todo_list["user"][user_id]
    elif group_id:
        if group_id not in todo_list["group"]:
            todo_list["group"][group_id] = {}
        tmp_todo_list = todo_list["group"][group_id]
    else:
        tmp_todo_list = todo_list

    return tmp_todo_list


def add_todo_list(
    job: Dict[str, Any],
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    __update_todo_list("add", job, user_id, group_id)


def remove_todo_list(
    job: str,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    __update_todo_list("remove", job, user_id, group_id)


def pause_todo_list(
    job: str,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    __update_todo_list("pause", job, user_id, group_id)


def resume_todo_list(
    job: str,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    __update_todo_list("resume", job, user_id, group_id)


# 更新待办事项列表
def __update_todo_list(
    type: str,
    job: Union[str, Dict[str, Any]],
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):

    todo_list = get_todo_list()
    tmp_todo_list = get_todo_list(user_id, group_id)

    if type == "add":
        tmp_todo_list.update(job)
    elif type == "remove":
        tmp_todo_list.pop(job)
    elif type == "pause":
        tmp_todo_list[job]["enable"] = False
    elif type == "resume":
        tmp_todo_list[job]["enable"] = True

    if user_id:
        todo_list["user"][user_id] = tmp_todo_list
        if tmp_todo_list == {}:
            todo_list["user"].pop(user_id)
    elif group_id:
        todo_list["group"][group_id] = tmp_todo_list
        if tmp_todo_list == {}:
            todo_list["group"].pop(group_id)

    __dump_todo_list(todo_list)


# 保存待办事项列表
def __load_todo_list() -> Dict[str, Any]:
    try:
        return yaml.safe_load(_DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {"user": {}, "group": {}}


# 保存待办事项列表
def __dump_todo_list(todo_list: Dict[str, Any]):
    _DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(
        todo_list,
        _DATA_PATH.open("w", encoding="utf-8"),
        allow_unicode=True,
    )

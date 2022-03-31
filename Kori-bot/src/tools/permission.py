import json
import os
def judge(qqnumber):
    file = open("/root/Kori-Bot/Kori-bot/src/tools/permission.json", mode = "r")
    json_ = json.loads(file.read())
    if qqnumber not in json_:
        return False
    else:
        return True
    file.close()

def checker(qqnumber:str,score:int):
    file = open("/root/Kori-Bot/Kori-bot/src/tools/permission.json", mode = "r")
    json_ = json.loads(file.read())
    if qqnumber not in json_:
        return False
    else:
        if (int(json_[qqnumber]) >= score) == False:
            return False
        else:
            return True
    file.close()
def error(score):
    return f"唔，权限不够哦，你需要至少{score}的权限等级才行呢。"

import json

def already_married(obj):
    cache = open("./src/tools/marry.json",mode="r")
    marrylist = json.loads(cache.read())
    cache.close()
    for i in marrylist:
        if i["wife"] == obj or i["husband"] == obj:
            return True
        else:
            continue
    return False
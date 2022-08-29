import requests as re

# id = "2560359315"
url = "https://api.iyk0.com/tzgsc/?msg={0}&id={1}"

right_response = "恭喜你，回答正确"

def check(answer: str, id):
    resp = re.get(url.format(answer, id))
    resp_text = resp.text
    return right_response in resp_text

def getQuestion(id):
    resp = re.get(url.format("下一题", id))
    resp_text = resp.text
    return resp_text or "Failed to get data!"
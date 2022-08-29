import ujson as json
import aiohttp
from random import randint
from pathlib import Path
from requests import get
from .sentence_similarity_calc import calculate_similarity

api_url = "http://api.kekc.cn/api/yien"


answer_path = Path() / "data" / "russian" / "dictation_answer.json"

def saveAnswer(answer, cn, id) -> None:
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf8") as f:
        data = json.loads(f.read())
    data[id] = {"en": answer}
    data[id]["cn"] = cn
    with open(answer_path, 'w', encoding="utf8") as f:
        f.write(json.dumps(data))

def checkAnswer(id, answer) -> dict:
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf-8") as f:
        answers = json.loads(f.read())
    return {
        "en": answers[id]["en"],
        "cn": answers[id]["cn"],
        "similarity": calculate_similarity(answers[id]["en"], answer)
    }


async def getAudio(id):
    id = str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            content = await response.text()
            content = json.loads(content)
            saveAnswer(content["en"], content["cn"], id)
            async with session.get(content["audio"]) as audio:
                return await audio.content.read()
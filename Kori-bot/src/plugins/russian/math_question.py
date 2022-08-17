import ujson as json
from random import randint
from pathlib import Path
# from .data_source import russian_path

# answer_path = "/root/Projects/Kori-Bot/Kori-bot/data/russian/math_answer.json"
answer_path = Path() / "data" / "russian" / "math_answer.json"
range1 = 10
range2 = 3000
# max_gold = 60


def saveMathAnswer(answer, id):
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf8") as f:
        data = json.loads(f.read())
    data[id] = answer
    with open(answer_path, 'w', encoding="utf8") as f:
        f.write(json.dumps(data))

def checkMathAnswer(id, answer):    # Answer is right -> return False
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf-8") as f:
        answers = json.loads(f.read())
    if answer == answers[id]:
        return False
    else:
        return answers[id]

def getMathQuestion(id):
    question_type = randint(0, 1)
    if question_type == 0:
        a = randint(range1, range2)
        b = randint(range1, range2)
        opp = randint(0, 1)
        question = str(a) + ('+' if opp else '-') + str(b)
    elif question_type == 1:
        a = randint(2, 100)
        b = randint(2, 100)
        question = str(a) + '*' + str(b)
    answer = eval(question)
    saveMathAnswer(answer, id)
    return (question+"=?").replace('*','×')
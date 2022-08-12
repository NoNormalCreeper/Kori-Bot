import ujson as json
from random import randint, sample, shuffle
from pathlib import Path


answer_path = "/root/Projects/Kori-Bot/Kori-bot/data/russian/word_answer.json"
wordlist_path = "/root/Projects/Kori-Bot/Kori-bot/src/plugin/russian/wordlist_CE.json"


def saveWordAnswer(answer, id):
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf8") as f:
        data = json.loads(f.read())
    data[id] = answer
    with open(answer_path, 'w', encoding="utf8") as f:
        f.write(json.dumps(data))

def checkWordAnswer(id, answer):    # Answer is right -> return False
    answer = str(answer)
    answer = answer.upper()
    id = str(id)
    with open(answer_path, "r", encoding="utf-8") as f:
        answers = json.loads(f.read())
    if answer == answers[id]:
        return False
    else:
        return answers[id]

def getWordQuestion(id):
    id = str(id)
    question = ""
    choice = []
    with open(wordlist_path, 'r') as f:
        wordlist = f.read()
    wordlist = json.loads(wordlist)

    length = len(wordlist)
    question_id = randint(0, length-1)
    chinese = list(wordlist.keys())[question_id]
    english = list(wordlist.values())[question_id]

    choice.append(english)
    for i in range(3):
        choice.append(list(wordlist.values())[randint(0, length-1)])
    shuffle(choice)
    answer = choice.index(english)

    letter = ['A','B','C','D']
    question += chinese
    for i in range(4):
        question += "\n[{0}] {1}".format(letter[i], choice[i])
    
    saveWordAnswer(letter[answer], id)
    return question

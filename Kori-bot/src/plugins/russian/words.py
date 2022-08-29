import ujson as json
from random import randint, sample, shuffle
from pathlib import Path


answer_path = "/root/Projects/Kori-Bot/Kori-bot/data/russian/word_answer.json"
#wordlist_path = "/root/Projects/Kori-Bot/Kori-bot/src/plugin/russian/CET4.json"
wordlist_path = Path(__file__).parent / "CET6.json"

def saveWordAnswer(answer, id):
    answer = str(answer)
    id = str(id)
    with open(answer_path, "r", encoding="utf8") as f:
        data = json.loads(f.read())
    data[id] = answer
    with open(answer_path, 'w', encoding="utf8") as f:
        f.write(json.dumps(data))

def checkWordAnswer(id, answer):# Answer is right -> return False
    answer = str(answer)
    answer = answer.upper()
    id = str(id)
    with open(answer_path, "r", encoding="utf-8") as f:
        answers = json.loads(f.read())
    return False if answer == answers[id] else answers[id]

def getWordQuestion(id):
    id = str(id)
    question = ""
    with open(wordlist_path, 'r') as f:
        wordlist = f.read()
    wordlist = json.loads(wordlist)

    length = len(wordlist)
    question_id = randint(0, length-1)
    #chinese = list(wordlist.keys())[question_id]
    #english = list(wordlist.values())[question_id]
    english = list(wordlist.keys())[question_id]
    chinese = wordlist[english]["中释"]

    choice = [english]
    choice.extend(list(wordlist.keys())[randint(0, length-1)] for _ in range(3))
    shuffle(choice)
    answer = choice.index(english)

    letter = ['A','B','C','D']
    question += chinese
    for i in range(4):
        question += "\n[{0}] {1}".format(letter[i], choice[i])

    saveWordAnswer(letter[answer], id)
    return question

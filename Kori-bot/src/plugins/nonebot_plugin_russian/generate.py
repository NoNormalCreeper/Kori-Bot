import re
import json

path = "wordlist2.txt"


type_rule = "[a-z]+ *\."


with open(path, 'r') as f:
    text = f.read()
wordlist_list = re.split('\n', text)
result = {}

for i in wordlist_list:
    # print(i)
    try:
        chinese_pos = re.search(type_rule, i).start()
        chinese = i[chinese_pos:].strip()
        english = i[0:chinese_pos].strip()
        result[english] = chinese
    except:  # 还是匹配不上
        print("Ignored:", i)
print(len(result))

result = json.dumps(result)
with open("output.json", 'w') as f:
    f.write(result)

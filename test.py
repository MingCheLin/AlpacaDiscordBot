file = open('./token.txt', 'r', encoding='UTF-8')
data = list()
with file as f:
    for line in f.read().splitlines():
        s = line.split(' ')
        data.append(s[1])
f.close()
token = data[0]
AI_name = data[1]
user_name = data[2]

print(data)
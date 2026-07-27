import json

with open("./data/data.mvpref", "r", encoding='utf-8') as file:
    data = json.load(file)

print(data["recent"][0]["name"])
import re
import json as JSON
import codecs

filename = "episodes/season_1/a_golden_crown.txt"

with open(filename, "r") as f:
    data = f.read()

json = [{}]

res = re.findall(r'"(.*?)"', data)

json[0]["title"] = res[0]

res = re.findall(r'Season (.*?)\n', data)

json[0]["season"] = res[0]

res = re.findall(r'Episode (.*?)\n', data)

json[0]["episode"] = res[0]

res = re.findall(r'Air date\n(.*?)\n', data)

json[0]["air_date"] = res[0]

res = re.findall(r'Written by\n(.*?)\n', data)

json[0]["authors"] = re.split(r'[,&]', res[0])

res = re.findall(r'Directed by\n(.*?)\n', data)

json[0]["director"] = re.split(r'[,&]', res[0])

res = re.findall(r'\n\n(.*?)\n\nContent', data)

json[0]["info"] = res[0]

dataSemEnter = data.replace("\n", "")

res = re.findall(r'Plot(.*?)Summary', dataSemEnter)

json[0]["plot"] = res[0].replace("Edit", "")

# res = re.findall(r'SummaryEdit\n(.*?)\nRecapEdit', dataSemEnter)
res = re.findall(r'Summary(.*?)Recap', dataSemEnter)
res = re.sub(" +", " ", res[0])
res.replace("\xa0", " ")
print(res)

json[0]["summary"] = res.replace("Edit", " ")

# print(json)

outputFilename = "teste2.json"

with codecs.open(outputFilename, "w", encoding="utf-8") as fp:
    JSON.dump(json, fp, ensure_ascii=False, indent=4, separators=(",", ": "))
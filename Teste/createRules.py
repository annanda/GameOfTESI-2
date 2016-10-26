import json
import nltk

with open("a_golden_crownTAGS.json", "r") as f:
    data = f.read()
    
with open("a_golden_crown.json", "r") as f:
    text = f.read()
    
data = json.loads(data)
text = json.loads(text)
text = text["summary"][0]["content"]

#Training:
sizeWindow = 3
rules = []
sep_sent = nltk.sent_tokenize(text)
# text = nltk.word_tokenize(text)
# text = nltk.pos_tag(text)

def findSurroundings(sent_index, word_index, length, type):
    sentence = sep_sent[sent_index]
    sentence = nltk.word_tokenize(sentence)
    sentence = nltk.pos_tag(sentence)
    surroundings = []
    for i in range(2 * sizeWindow + 1):
        nextNeighbour = word_index - sizeWindow + i
        if(nextNeighbour == word_index):
            word_index += length - 1
            surroundings.append(type)
        elif(nextNeighbour < 0 or nextNeighbour >= len(sentence)):
            surroundings.append("")
        else:
            surroundings.append(sentence[word_index - sizeWindow + i][1])
    return surroundings

def createRules(obj):
    tagged_elements = obj["tags"]
    for element in tagged_elements:
        rules.append(findSurroundings(element[0], element[1], element[2], element[3]))

# print(text[0])
# print(data)
# test = findSurroundings(0, 0, 3, "PERSON")
# test2 = findSurroundings(0, 20, 2, "PERSON")
# test3 = findSurroundings(1, 7, 2, "PERSON")
# print(sep_sent[0])
# print(test)
# print(test2)
# print(test3)
createRules(data)
print(rules)
    
    

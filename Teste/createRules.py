import json
import nltk

with open("a_golden_crownTAGS.json", "r") as f:
    data = f.read()
    
with open("a_golden_crown.json", "r") as f:
    text = f.read()
    
data = json.loads(data)
text = json.loads(text)
text = text["summary"][0]["content"]
sep_sent = nltk.sent_tokenize(text)



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
        elif(nextNeighbour < 0 or nextNeighbour >= len(sentence) or sentence[word_index - sizeWindow + i][1] == "."):
            surroundings.append("")
        else:
            surroundings.append(sentence[word_index - sizeWindow + i][1])
    return surroundings

def createRules(obj):
    rules = []
    tagged_elements = obj["tags"]
    for element in tagged_elements:
        rules.append(findSurroundings(element[0], element[1], element[2], element[3]))
    # print(rules)
    return optimizeRules(rules)

def separate_by_type(rules):
    sep_rules = {}
    for r in rules:
        if(r[sizeWindow] not in sep_rules.keys()):
            sep_rules[r[sizeWindow]] = []
        sep_rules[r[sizeWindow]].append(r)
    return sep_rules

def merge(_rule1, _rule2):
    rule1 = list(_rule1)
    rule2 = list(_rule2)
    for i in range(len(rule1)):
        # if(rule2[i] in rule1[i]):
        if(not(rule2[i] in rule1[i]) and len(rule1[i]) < variety and rule1[i] != ["?"]):
            rule1[i].append(rule2[i])
        else:
            rule1[i] = ["?"]
    return rule1

def convertToArray(rule):
    arr = []
    for tag in rule:
        arr.append([tag])
    return arr

def h_dist(rule1, rule2):
    dist = 0
    for i in range(len(rule1)):
        if(rule2[i] not in rule1[i]):
            dist+=1
    return dist

def optimizeRules(rules):
    sep_rules = separate_by_type(rules)
    print(sep_rules)
    op_rules = {}
    for t in sep_rules:
        for rule in sep_rules[t]:
            if(t not in op_rules.keys()):
                op_rules[t] = [convertToArray(rule)]
            else:
                added = False
                size = len(op_rules[t])
                for i in range(size):
                    current_rule = op_rules[t][i]
                    print(h_dist(current_rule, rule))
                    if(h_dist(current_rule, rule) > sensitivity and added == False):
                        print("ifDIST")
                        op_rules[t].append(convertToArray(rule))
                        added = True
                    elif(added == False):
                        print("elseDIST")
                        op_rules[t][i] = (merge(current_rule, rule))
    return op_rules

#Hyperparameters    
sizeWindow = 3
variety = 3
sensitivity = 2

print(createRules(data))

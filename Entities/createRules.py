import json
import nltk
from collections import OrderedDict


# with open("a_golden_crownTAGS.json", "r") as f:
#     data = f.read()
    
# with open("a_golden_crown.json", "r") as f:
#     text = f.read()
    
# data = json.loads(data)
# text = json.loads(text)
# text = text["summary"][0]["content"]
# sep_sent = nltk.sent_tokenize(text)

past_entities = {}


def findSurroundings(sentence, word_index, length, type):
    # sentence = sep_sent[sent_index]
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

def createRules(tagged_elements):
    rules = []
    i = 0
    # print(tagged_elements, end="\n\n\n\n")
    for section in tagged_elements:
        past_entities = {}
        sep_sent = main_text[i][1]
        i+=1
        # print(section)
        for entity in tagged_elements[section]:
            # print("Chamando find word index")
            # print("sep_sent: " + str(sep_sent))
            initial_word_index, length = findWordIndex(sep_sent[entity[0]], entity[0], entity[1], entity[4])
            # final_word_index = findWordIndex(sep_sent[entity[0]], entity[0], entity[2], entity[4])
            # length = final_word_index - initial_word_index + 1
            rules.append(findSurroundings(sep_sent[entity[0]], initial_word_index, length, entity[3]))
    # print(rules)
    return optimizeRules(rules)

def addPastEntity(sent_index, entity_string):
    tup = (sent_index, entity_string)
    if(tup in past_entities):
        past_entities[tup] += 1
    else:
        past_entities[tup] = 1
    return past_entities[tup]-1


def findWordIndex(sentence, sent_index, char_index, entity_string):
    # print("Looking for " + entity_string)
    prev_occurences = addPastEntity(sent_index, entity_string)
    # print("sentence: " + str(sentence))
    words = nltk.word_tokenize(sentence)
    decomposed_entity = nltk.word_tokenize(entity_string)
    index_candidate = -1
    candidates_found = 0
    for i in range(len(words)):
        # print("loopao")
        if(words[i] == decomposed_entity[0]):
            # print("Something matched")
            index_candidate = i
            for d in range(len(decomposed_entity)):
                if(words[i+d] != decomposed_entity[d]):
                    index_candidate = -1
                    break
            if(index_candidate == -1):
                continue
            elif(candidates_found == prev_occurences):
                # print("Found it")
                return (index_candidate, len(decomposed_entity))
            else:
                candidates_found += 1
                continue

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
            if(rule1[i] == "PERSON" or rule1[i] == "LOCATION" or rule1[i] == "ORGANIZATION" or rule1[i] == "OTHER" or rule1[i] == "DATE"):
                print("Well shit")
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
    # print(sep_rules)
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
                    if(h_dist(current_rule, rule) > sensitivity and added == False):
                        op_rules[t].append(convertToArray(rule))
                        added = True
                    elif(added == False):
                        op_rules[t][i] = (merge(current_rule, rule))
    return op_rules

def readFiles(input):
    with open(input, "r") as f:
        ext = input.split(".")[1]
        if(ext == "json"):
            temp = f.read()
            return json.loads(temp, object_pairs_hook=OrderedDict)
        elif(ext == "txt"):
            temp = f.readlines()
            return createSections(temp)
        else:
            return temp

def createSections(text):
    allIndexes = []
    index = []
    for i, item in enumerate(text):
        if (item[0] == "<") and (item[-2] == ">"):  
            index.append(i+1)
        if (item == "\n"):
            index.append(i-1)
            allIndexes.append(index)
            index = []

    dataTXT = []
    for i in range(len(allIndexes)):
        dataI = []
        dataI.append(text[allIndexes[i][0]-1][1:-2])      
        selectedSent = text[allIndexes[i][0]:allIndexes[i][1]+1]
        selectedSent = [item.rstrip("\n") for item in selectedSent]
        dataI.append(selectedSent)
        dataTXT.append(dataI)
             
    return (dataTXT, allIndexes)



#Hyperparameters    
sizeWindow = 3
variety = 3
sensitivity = 5

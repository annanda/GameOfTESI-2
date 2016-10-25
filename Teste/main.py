import json
import nltk

with open("a_golden_crownTAGS.json", "r") as f:
    data = f.read()
    
with open("a_golden_crown.json", "r") as f:
    text = f.read()
    
data = json.loads(data)
text = json.loads(text)
text = text["summary"][0]["content"]


def findMe(string, text):
    string = string.split(" ")
    
    sizeText = len(text)
    sizeString = len(string)
    for i in range(sizeText - sizeString):
        for j in range(sizeString):
            if (j == sizeString - 1) and (string[j] != text[i+j]):
            
            if string[j] != text[i+j]:
                break
            
#Training:
sizeWindow = 2

rules = []

text = nltk.word_tokenize(text)
text = nltk.pos_tag(text)

print(text)

#textWithPOS_TAGGER = TEXTO

#Varrer exemplos no treinamento:
    
    

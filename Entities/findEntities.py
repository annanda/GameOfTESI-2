import createRules
import re
import nltk

def findEntities(rules):
	entities = {}
	for length in range(4):
		print("Entity Length: " + str(length))
		for entity_type in rules:
			entities[entity_type] = findAllFromType(rules[entity_type], length)
	return entities

def findAllFromType(type_rules, entity_length):
	entities = []
	for rule in type_rules:
		entities.append(matchAllFromRule(rule, entity_length))
	entities = flatten(entities)
	return entities

def matchAllFromRule(rule, entity_length):
	print("matching")
	entities = []
	for section in createRules.main_text:
		for sentence in section[1]:
			words = nltk.word_tokenize(sentence)
			pos_tags = nltk.pos_tag(words)
			for i in range(len(pos_tags)):
				if(pos_tags[i][1] == rule[0][0]):
					length = 0
					for j in range(len(rule)):
						next_rule_tag = rule[j][0]
						if(next_rule_tag == ''):
							continue
							
						if(isNamedEntityType(next_rule_tag)):
							length += entity_length-1 
							continue
						pos_index = i+j+length
						if(pos_index >= len(pos_tags)):
							break
						if(j == len(rule)-1):
							print("Found an Entity!")
							ent = ""
							for k in range(entity_length):
								ent += pos_tags[i+k][0]
								if(k != entity_length -1 and pos_tags[i+k] != "'"):
									ent += " "
							entities.append(ent)
								
						if(rule[j][0] != pos_tags[pos_index][1]):
							break

					
	print(entities)
	return entities

def isNamedEntityType(tag):
	if(tag == "PERSON" or tag == "LOCATION" or tag == "DATE" or tag == "ORGANIZATION" or tag == "OTHER"):
		return True
	else:
		return False


def flatten(array):
	flat_array = []
	for subarray in array:
		for item in subarray:
			flat_array.append(item)
	return flat_array

def getFullText(file):
	with open(file, "r") as f:
		text =  f.read()
		tags = re.findall(r'<(.*?)>', text)
		for tag in tags:
			text = text.replace("<" + tag + ">", "")
		print(text)

#Create rules to find entities
tags = createRules.readFiles("a_golden_crown_entities.json")
createRules.main_text, createRules.indexes = createRules.readFiles("a_golden_crown.txt")
createRules.sep_sent = []
rules = createRules.createRules(tags)
# getFullText("a_golden_crown.txt")
entities = findEntities(rules)
print(entities)
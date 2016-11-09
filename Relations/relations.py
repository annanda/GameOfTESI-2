import json
from nltk import word_tokenize
from nltk import sent_tokenize

class RelationExtracter():
	def __init__(self, input=None):
		self.input = input
		if(input):
			self.parseFile()
		else:
			print("Done")

	def parseFile(self):
		with open(self.input, "r") as f:
			text = f.read()
			self.fullJSON = json.loads(text)
			self.summary = self.fullJSON["summary"]

		with open(self.input.split(".")[0] + "_tags.json", "r") as f:
			text = f.read()
			self.tags = json.loads(text)

	# Temporary
	def findEntities(self):
		self.entities = {}
		locations = self.tags["summary"]
		i = 0
		for loc in locations:
			print(loc)
			self.entities[loc["location"]] = []
			currentText = self.summary[i]["content"]
			sentences = sent_tokenize(currentText)
			words = []
			for sent in sentences:
				words.append(word_tokenize(sent))
			lastSent = 0
			for entity in loc["entities"]:
				print(lastSent)
				print(entity[0])
				bug = False if entity[1]<len(words[entity[0]]) and entity[0]>=lastSent else True
				lastSent = entity[0]
				if(bug):
					break
				fullEntity = ""
				print(entity)
				print("Max len: " + str(len(words[entity[0]])))
				for j in range(entity[2]):
					apostrophe = False
					nextFragment = words[entity[0]][entity[1] + j]
					if(nextFragment == "'"):
						apostrophe = True
					if (j != 0 and not apostrophe):
						fullEntity += " "

					fullEntity += nextFragment
				self.entities[loc["location"]].append(fullEntity)
			i+=1


rel = RelationExtracter("a_golden_crown.json")
rel.findEntities()
print(rel.entities)
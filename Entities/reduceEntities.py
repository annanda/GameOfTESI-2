import json
from collections import OrderedDict

def readFiles(input):
    with open(input, "r") as f:
        ext = input.split(".")[1]
        if(ext == "json"):
            temp = f.read()
            return json.loads(temp, object_pairs_hook=OrderedDict)
        else:
            return temp

def discardCopies(l):
 	return set(list(l))

def createGraph(ne_list):
 	graph = {}
 	for ne in ne_list:
 		graph[ne] = []
 	return graph

def addSubStringEdges(graph, ne_list):
 	for main_ne in ne_list:
 		for ne in ne_list:
 			if(ne == main_ne):
 				continue
 			if(ne in main_ne):
 				if(ne not in graph[main_ne]):
 					graph[main_ne].append((ne, 1.0))
 				if(main_ne not in graph[ne]):
 					graph[ne].append((main_ne, 1.0))
 	return graph

def printCSV(graph):
	for node in graph:
		print(node + ",", end=" ")
		for connections in graph[node]:
			print(connections[0] + ",", end=" ")
		print("")


entities_list = readFiles("entities_list.json")
entities_list = discardCopies(entities_list["entities"])
print("Initial List")
print(entities_list, end="\n\n")
print("Graph")
graph = createGraph(entities_list)
graph = addSubStringEdges(graph, entities_list)
print(graph)
printCSV(graph)
print
import os
import re
import json
from nltk import sent_tokenize
from tkinter import filedialog

current_path = os.getcwd()
dir_path = filedialog.askdirectory()

#Create folders:
os.makedirs(current_path + "/episodesTXT", exist_ok=True)
for i in range(6):
    os.makedirs(current_path + "/episodesTXT" + "/season_" + str(i+1), exist_ok=True)

#Raw to txt:
for i in range(6):    
    seasonFolder = dir_path + "/season_" + (str(i + 1))
    for filename in os.listdir(seasonFolder):
        with open(seasonFolder + "/" + filename, "r") as f:
            jsonFile = f.read()
            jsonFile = json.loads(jsonFile) 
            
            #os.makedirs(os.path.dirname(current_path
            textFile = open(current_path + "/episodesTXT" + "/season_" + str(i+1) + "/" + filename[:-5] + ".txt", "w+")
            
            #Write info and plot:
            info = jsonFile["info"]
            sentInfo = sent_tokenize(info)
            plot = jsonFile["plot"]
            sentPlot = sent_tokenize(plot)
            
            textFile.write("<info>\n")
            for sent in sentInfo:
                textFile.write(sent + "\n")
            textFile.write("\n")
            textFile.write("<plot>\n")
            for sent in sentPlot:
                textFile.write(sent + "\n")
            textFile.write("\n")
            
            #Write summary:
            summary = jsonFile["summary"]
            for item in summary:
                location = item["location"]
                content = item["content"]    
                textFile.write("<summary/" + location + ">\n")   
                sentContent = sent_tokenize(content)
                for sent in sentContent:
                    textFile.write(sent + "\n")
                textFile.write("\n")
            

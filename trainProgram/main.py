from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from nltk import word_tokenize
from nltk import sent_tokenize
import json

class Window(Frame):
    
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        
        self.master = master
        self.configure()
        
        #Init Variables:
        self.init_variables()

        self.init_firstScene()
        self.init_secondScene()
        
            
    def configure(self):
        self.master.title("Game of Annotation")
        for i in range(60):
            Grid.columnconfigure(self.master, i, weight=1)
        for i in range(30):
            Grid.rowconfigure(self.master, i, weight=1)
        
        # self.dataBOX = Listbox(master, selectmode=EXTENDED, height=25, width=20)
        # self.wordBOX = Listbox(master, selectmode=EXTENDED, height=25, width=30)
        # self.addButton = Button(master, text="Add NE", command=self.addNE, height=1, width=7)
        # self.removeButton = Button(master, text="Remove NE", command=self.removeNE, height=1, width=7)                
        # self.loadButton = Button(master, text="Load File", command=self.addNE, height=1, width=7)
        # self.saveButton = Button(master, text="Save File", command=self.addNE, height=1, width=7)
    
    def init_firstScene(self):
        self.background_image = ImageTk.PhotoImage(file="game-of-tesi.jpg")
        self.panel = Canvas(width = self.background_image.width(), height = self.background_image.height())
        self.panel.grid()
        self.panel.create_image(self.background_image.width()/2.0, self.background_image.height()/2.0, image = self.background_image)
        self.startButton = Button(self.master, text="Choose File", command=self.openFile, height=3, width=15)
        self.aboutButton = Button(self.master, text="About", command=self.infoAbout, height=3, width=15)
        self.panel.create_window(350, 450, window=self.startButton)
        self.panel.create_window(650, 450, window=self.aboutButton)
        
    def init_secondScene(self):
        # self.scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.dataBOX = Listbox(self.master, selectmode=EXTENDED, height=30, width=20)
        self.wordBOX = Listbox(self.master, selectmode=EXTENDED, height=25, width=30)
        self.taggedText = Text(self.master, height=25, width=50)
        self.addButton = Button(self.master, text="Add NE", command=self.addNE, height=1, width=7)
        self.removeButton = Button(self.master, text="Remove NE", command=self.removeNE, height=1, width=7)                
        self.loadButton = Button(self.master, text="Load File", command=self.loadFile, height=1, width=7)
        self.saveButton = Button(self.master, text="Save File", command=self.saveFile, height=1, width=7)
        self.neTypeDropdown = OptionMenu(self.master, self.currentNEType, "PERSON", "LOCATION", "ORGANIZATION", "OTHER")
        self.taggedText.tag_config("PERSON", background=self.colors["PERSON"])
        self.taggedText.tag_config("LOCATION", background=self.colors["LOCATION"])
        self.taggedText.tag_config("ORGANIZATION", background=self.colors["ORGANIZATION"])
        self.taggedText.tag_config("OTHER", background=self.colors["OTHER"])
        self.taggedText.tag_config("BLANK", background="white")
        
    def init_variables(self):
        self.allSaved = True
        self.listTokens = []
        self.sizeOfSents = []
        self.taggedTupples = {}                
        self.currentLocation = IntVar()
        self.currentNEType = StringVar()
        self.currentLocation.set(0)
        self.currentNEType.set("PERSON")
        self.colors = {"PERSON": "#90D491", "LOCATION": "#90AAD4", "ORGANIZATION": "#D46B5F", "OTHER": "#AC81D4"}
        self.highlightTerms = {}
        
    def infoAbout(self):    
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Guilherme Freire e Hugo Gomes criaram esse programa", height=20, width=40)
        label1.pack()
        
    def openFile(self):
        file_path = tk.filedialog.askopenfilename()
        with open(file_path, "r") as f:
            text = f.read()
        text = json.loads(text)
        self.mainScreen(text)

    def discardChanges(self):
        self.err.destroy()
        self.loadFile(True)

    def loadFile(self, loadAnyway=False):
        #Check for unsaved material
        if(not self.allSaved and not loadAnyway):
            self.err = Toplevel()
            self.err.title("File not saved!")

            msg = Message(self.err, text="Você ainda não salvou suas mudanças.\nAo carregar outro arquivo, mudanças não salvas serão perdidas.\nDeseja continuar?", width=300, justify="center")
            msg.grid(row=0, column=0, columnspan=2)

            buttonYes = Button(self.err, text="Yes", command=self.discardChanges)
            buttonYes.grid(row=1, column=0)

            buttonNo = Button(self.err, text="No", command=self.err.destroy)
            buttonNo.grid(row=1, column=1)
            center(self.err)
            return

        file_path = tk.filedialog.askopenfilename()
        with open(file_path, "r") as f:
            text = f.read()
        text = json.loads(text)

        self.dataBOX.delete(0,END)
        self.wordBOX.delete(0, END)
        for radio in self.locations:
            radio.grid_forget()

        self.summary = text["summary"]
        summary = self.summary
        self.locations = []
        for location in range(len(summary)):
            self.locations.append(Radiobutton(self.master, height=1, width=20, text=summary[location]["location"], variable=self.currentLocation, value=location, command=self.changeLocation))
            self.locations[location].grid(row=location + 1, column=1, sticky=W+N+S)

        text = text["summary"][0]["content"]
        sents = sent_tokenize(text)
        self.listTokens = []
        self.sizeOfSents = []
        for sent in sents:
            self.listTokens.append(word_tokenize(sent))
        for item in self.listTokens:
            self.sizeOfSents.append(len(item))
        
        # Add box of words
        for sents in self.listTokens:
            for token in sents:
                self.dataBOX.insert(END, token)

    def saveFile(self):
        file_path = tk.filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if(file_path is None):
            return
        file_path.write(self.toJSON(self.taggedTupples))
        file_path.close()
        self.allSaved = True

    def toJSON(self, dict):
    	i = 0
    	jsonString = "{\"summary\": ["
    	for location in self.taggedTupples:
    		jsonString += "{\"location\": \"" + location + "\","
    		jsonString += "\"entities\": " + str(self.tuppleArrayToArrayArray(self.taggedTupples[location])).replace("'", "\"")
    		if(i != len(self.taggedTupples) -1):
    			jsonString += "},"
    		else:
    			jsonString += "}]"
    		i+=1
    	jsonString += "}"
    	return jsonString

    def tuppleArrayToArrayArray(self, tupArr):
    	array = []
    	for tup in range(len(tupArr)):
    		array.append([])
    		for item in tupArr[tup]:
    			array[tup].append(item)
    	return array


        
    def mainScreen(self, text):

        if("summary" not in text):
            err = Toplevel()
            err.title("Invalid JSON")

            msg = Message(err, text="Arquivo não possui a estrutura esperada.", width=300)
            msg.pack()

            button = Button(err, text="Dismiss", command=err.destroy)
            button.pack()
            center(err)
            return

        self.panel.grid_forget()
        self.startButton.grid_forget()

        self.summary = text["summary"]
        summary = self.summary
        self.locations = []
        for location in range(len(summary)):
            self.locations.append(Radiobutton(self.master, height=1, width=20, text=summary[location]["location"], variable=self.currentLocation, value=location, command=self.changeLocation))
            self.locations[location].grid(row=location + 1, column=1, sticky=W+N+S)

        self.neTypeDropdown.grid(row=2 + len(summary), column=1, sticky=E+W)
        self.addButton.grid(row=3 + len(summary), column=1, sticky=N+S+E+W)
        self.removeButton.grid(row=4 + len(summary), column=1, sticky=N+S+E+W)
        self.loadButton.grid(row=0, column=0, sticky=N+S+E+W)
        self.saveButton.grid(row=0, column=2, sticky=N+S+E+W)
        # self.scrollbar.config(command=self.dataBOX.yview)
        # self.scrollbar.pack(side=RIGHT, fill=Y)
        self.dataBOX.grid(row=1, column=0, rowspan=10, sticky=N+S+E+W)
        self.wordBOX.grid(row=1, column=2, rowspan=10, sticky=N+S+E+W)
        self.taggedText.grid(row=1, column=3, rowspan=10, sticky=N+S+E+W)
        
        text = text["summary"][0]["content"]
        sents = sent_tokenize(text)
        for sent in sents:
            self.listTokens.append(word_tokenize(sent))
        for item in self.listTokens:
            self.sizeOfSents.append(len(item))
        
        
        # Add box of words
        for sents in self.listTokens:
            for token in sents:
                self.dataBOX.insert(END, token)

        self.taggedText.insert(END, self.summary[0]["content"])

    def changeLocation(self):
        self.dataBOX.delete(0,END)
        self.wordBOX.delete(0, END)
        self.taggedText.delete(1.0, END)
        text = self.summary[self.currentLocation.get()]["content"]
        sents = sent_tokenize(text)
        self.listTokens = []
        self.sizeOfSents = []
        for sent in sents:
            self.listTokens.append(word_tokenize(sent))
        for item in self.listTokens:
            self.sizeOfSents.append(len(item))

        # Add box of words
        for sents in self.listTokens:
            for token in sents:
                self.dataBOX.insert(END, token)
        locTag = self.summary[self.currentLocation.get()]["location"]
        if(locTag in self.taggedTupples):
            for item in self.taggedTupples[locTag]:
                self.wordBOX.insert(END, str(item) + "\n")

        self.taggedText.insert(END, self.summary[self.currentLocation.get()]["content"])
        self.showHighlight()
        
    def addNE(self):
        wordIndexes = list(self.dataBOX.curselection())
        if(not wordIndexes):
            return

        self.allSaved = False

        #Find sent_index:
        sumTotal = 0
        sent_index = 0
        for i, item in enumerate(self.sizeOfSents):
            if wordIndexes[0] < sumTotal:
                sent_index = i-1
                break
            sumTotal += item
        
        word_index = -sum(self.sizeOfSents[0:sent_index])+wordIndexes[0]
        length = len(wordIndexes)
        typeNE = self.currentNEType.get()
        writeItem = "(" + str(sent_index) + ", " + str(word_index) + ", " + str(length) + ", " + typeNE + ")"
        self.wordBOX.insert(END, writeItem + "\n")
        locTag = self.summary[self.currentLocation.get()]["location"]
        if(locTag not in self.taggedTupples):
            self.taggedTupples[locTag] = []
        self.taggedTupples[locTag].append((sent_index, word_index, length, typeNE))

        #Color selected cells
        for sel in wordIndexes:
            self.dataBOX.itemconfig(sel, bg=self.colors[typeNE])

        #Highlight tagged entities in the full text
        self.addHighlight(wordIndexes, typeNE)
        self.showHighlight()

    def addHighlight(self, wordIndexes, type):
        highlightTerm = ""
        counter = 0
        for index in wordIndexes:
            apostrophe = False
            nextFragment = self.dataBOX.get(index)
            if(nextFragment[0] == "'"):
                apostrophe = True
            if(counter != 0 and not apostrophe):
                 highlightTerm += " "
            highlightTerm += nextFragment
            counter+=1 

        locTag = self.summary[self.currentLocation.get()]["location"]
        if(locTag not in self.highlightTerms):
            self.highlightTerms[locTag] = []
        self.highlightTerms[locTag].append((highlightTerm, type))

        # self.highlightTerms.append((highlightTerm, type))

    def showHighlight(self):
        locTag = self.summary[self.currentLocation.get()]["location"]
        for h in self.highlightTerms[locTag]:
            self.highlightText(self.taggedText, h[0], h[1])
        
    def removeNE(self):
        wordIndexes = list(self.wordBOX.curselection())
        if(not wordIndexes):
            return
        for i in wordIndexes:
            locTag = self.summary[self.currentLocation.get()]["location"]
            del self.taggedTupples[locTag][i]
            pop = self.highlightTerms[locTag][i]
            del self.highlightTerms[locTag][i]
            self.highlightText(self.taggedText, pop[0], "BLANK")
            self.wordBOX.delete(i)
        self.showHighlight()

    def highlightText(self, text_widget, keyword, tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, pos)

def create_window():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (1000/2)        
    y = (screen_height/2) - (600/2)
    root.geometry("%dx%d+%d+%d" % (1000, 600, x, y))
    
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

root = Tk()
create_window()
app = Window(root)
root.mainloop()

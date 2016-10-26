from tkinter import *
import tkinter as tk
from nltk import word_tokenize
from nltk import sent_tokenize
import json

class Window(Frame):
    
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        
        self.master = master
        self.init_window()
        
        self.dataBOX = Listbox(master, selectmode=EXTENDED, height=25, width=20)
        self.wordBOX = Text(master, height=26, width=30)
        self.addButton = Button(master, text="Add NE", command=self.addNE, height=1, width=7)
        self.removeButton = Button(master, text="Remove NE", command=self.addNE, height=1, width=7)                
        self.loadButton = Button(master, text="Load File", command=self.addNE, height=1, width=7)
        self.saveButton = Button(master, text="Save File", command=self.addNE, height=1, width=7)
                        
        self.listTokens = []
        self.sizeOfSents = []                
                        
    def init_window(self):
        
        self.master.title("Game of Annotation")
        
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open File", command=self.openFile)
        menu.add_cascade(label="File", menu=fileMenu)
        
        editMenu = Menu(menu)
        editMenu.add_command(label="About", command=self.infoAbout)
        menu.add_cascade(label="About", menu=editMenu)
        
    def infoAbout(self):    
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Guilherme Freire e Hugo Gomes criaram esse programa", height=20, width=40)
        label1.pack()
        
    def openFile(self):
        file_path = tk.filedialog.askopenfilename()
        with open(file_path, "r") as f:
            text = f.read()
        text = json.loads(text)
        
        #option = OptionMenu(self.master, "one", "two", "three", "four")
        #option.pack()
        
        text = text["summary"][0]["content"]
        sents = sent_tokenize(text)
        for sent in sents:
            self.listTokens.append(word_tokenize(sent))
        for item in self.listTokens:
            self.sizeOfSents.append(len(item))
        
        self.addButton.grid(row=2, column=1)
        self.removeButton.grid(row=3, column=1)
        self.loadButton.grid(row=0, column=0)
        self.saveButton.grid(row=0, column=2)
        
        #Add box of words
        for sents in self.listTokens:
            for token in sents:
                self.dataBOX.insert(END, token)
        self.dataBOX.grid(row=1, column=0, rowspan=3)
        
        self.wordBOX.grid(row=1, column=2, rowspan=3)
        
        
    def addNE(self):
        wordIndexes = list(self.dataBOX.curselection())
        
        #Find sent_index:
        sumTotal = 0
        sent_index = 0
        for i, item in enumerate(self.sizeOfSents):
            if wordIndexes[0] < sumTotal:
                sent_index = i-1
                break
            sumTotal += item
        
        word_index = -sum(self.sizeOfSents[0:sent_index])+wordIndexes[0]
        lenght = len(wordIndexes)
        typeNE = "PERSON"
        writeItem = "(" + str(sent_index) + ", " + str(word_index) + ", " + str(lenght) + ", " + typeNE + ")"
        self.wordBOX.insert(END, writeItem + "\n")
        
def create_window():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (500/2)        
    y = (screen_height/2) - (480/2)
    root.geometry("%dx%d+%d+%d" % (500, 480, x, y))
    
root = Tk()
create_window()
app = Window(root)
root.mainloop()

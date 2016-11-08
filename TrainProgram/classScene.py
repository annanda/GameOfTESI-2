from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from nltk import word_tokenize
import pickScene
import json

class Window(Frame):
    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        
        self.master = master
        self.master.title("Game of Annotation")
        
        #Init Variables:
        self.init_variables()

        #menuScene:
        self.init_menuScene()
        
        #pickScene:
        
        #mainScene:
        self.init_mainScene()   
    
    #Block of Inits:
    def init_variables(self):
        self.outputFILE = {}
        self.allSaved = True
        self.listTokens = []
        self.sizeOfSents = []
        self.taggedTupples = {}                
        self.currentFormKey = IntVar()
        self.currentFormKey.set(0)
        self.currentNEType = StringVar()
        self.currentNEType.set("PERSON")
        self.colors = {"PERSON": "#90D491", "LOCATION": "#90AAD4", "ORGANIZATION": "#D46B5F", "OTHER": "#AC81D4"}
        
    def init_menuScene(self):
        self.background_image = ImageTk.PhotoImage(file="game-of-tesi.jpg")
        self.panel = Canvas(width = self.background_image.width(), height = self.background_image.height())
        self.panel.grid()
        self.panel.create_image(self.background_image.width()/2.0, self.background_image.height()/2.0, image = self.background_image)
        self.startButton = Button(self.master, text="Choose File", command=self.openFile, height=3, width=15)
        self.aboutButton = Button(self.master, text="About", command=self.infoAbout, height=3, width=15)
        self.panel.create_window(350, 450, window=self.startButton)
        self.panel.create_window(650, 450, window=self.aboutButton)
        
    def init_mainScene(self):
        self.wordsBOX = Listbox(self.master, selectmode=EXTENDED, height=30, width=20)
        self.outputBOX = Text(self.master, height=25, width=50)
        self.colorTextBOX = Listbox(self.master, selectmode=EXTENDED, height=25, width=30)
        self.addButton = Button(self.master, text="Add NE", command=self.addNE, height=1, width=7)
        self.removeButton = Button(self.master, text="Remove NE", command=self.removeNE, height=1, width=7)                
        self.neTypeDropdown = OptionMenu(self.master, self.currentNEType, "PERSON", "LOCATION", "ORGANIZATION", "OTHER")
        
        #Menu
        self.menubar = Menu(self.master)
        
        #Add File
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.hello)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        #Add Help
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=self.hello)
        helpmenu.add_separator()
        helpmenu.add_command(label="About", command=self.hello)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
                
    #Functions of menuScene:
    def infoAbout(self):    
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Guilherme Freire e Hugo Gomes criaram esse programa", height=10, width=60)
        label1.pack()
        
    def openFile(self):
        file_path = tk.filedialog.askopenfilename()
        with open(file_path, "r") as f:
            text = f.readlines()
            
        #pickScene:    
        self.choices, self.indexesChoices, self.indexesTXT, self.dataTXT = pickScene.listBoxDialogWindow(self, text).returnAnswer()

        #Prepare tokensTXT:
        self.tokensTXT = []
        for item in self.dataTXT:
            sentTXT = []
            for sent in item[1]:
                sentTXT.append(word_tokenize(sent))
            self.tokensTXT.append(sentTXT)

        self.mainScreen()
        
    #Functions for mainScene:
    def mainScreen(self):

        #Delete First Scene:
        self.panel.grid_forget()
        self.startButton.grid_forget()

        self.formKeys = []
        for i in range(len(self.choices)):
            self.formKeys.append(Radiobutton(self.master, height=1, width=20, text=self.choices[i], variable=self.currentFormKey, value=i, command=self.changeFormKey))
            self.formKeys[i].grid(row=i + 1, column=1, sticky=W+N+S)
            
        self.neTypeDropdown.grid(row=2 + 10, column=1, sticky=E+W)
        self.addButton.grid(row=3 + 10, column=1, sticky=N+S+E+W)
        self.removeButton.grid(row=4 + 10, column=1, sticky=N+S+E+W)
        self.wordsBOX.grid(row=1, column=0, rowspan=10, sticky=N+S+E+W)
        self.outputBOX.grid(row=1, column=2, rowspan=10, sticky=N+S+E+W)
        self.colorTextBOX.grid(row=1, column=3, rowspan=10, sticky=N+S+E+W)
        self.master.config(menu=self.menubar)
        
        #First iteration        
        for item in self.choices:
            self.outputFILE[item] = []
        self.actual_block = self.indexesChoices[0]
        for sent in self.tokensTXT[self.actual_block]:
            for token in sent:
                self.wordsBOX.insert(END, token)
        self.update_outputBOX()
####    self.outputBOX.insert(END, self.summary[0]["content"])

    def changeFormKey(self):
        self.wordsBOX.delete(0,END)
        self.actual_block = self.indexesChoices[self.currentFormKey.get()]
        for sent in self.tokensTXT[self.actual_block]:
            for token in sent:
                self.wordsBOX.insert(END, token)
        
    def addNE(self):
        wordIndexes = list(self.wordsBOX.curselection())
        if(not wordIndexes):
            return
        #self.allSaved = False
        
        #Find sent_index:
        sumTotal = 0
        sent_index = 0
        notBreak = 1
        for i, item in enumerate(self.tokensTXT[self.actual_block]):
            if wordIndexes[0] < sumTotal:
                sent_index = i-1
                prev = self.tokensTXT[self.actual_block][i-1]
                wordInSentIndex = wordIndexes[0] - (sumTotal - len(prev))
                notBreak = 0
                break
            sumTotal += len(item)
        if notBreak == 1:
            sent_index = len(self.tokensTXT[self.actual_block]) - 1
        
        sumTotal = 0
        for i, item in enumerate(self.tokensTXT[self.actual_block]):
            if wordIndexes[-1] < sumTotal:
                prev = self.tokensTXT[self.actual_block][i-1]
                LastwordInSentIndex = wordIndexes[-1] - (sumTotal - len(prev))
                break
            sumTotal += len(item)
        
        
        #Find begin_index:
        sentence = self.dataTXT[self.actual_block][1][sent_index]
        word = self.tokensTXT[self.actual_block][sent_index][wordInSentIndex]
        begin_index = sentence.find(word)
                   
        #Find last_index =
        word = self.tokensTXT[self.actual_block][sent_index][LastwordInSentIndex]
        last_index = sentence.find(word) + len(word)
        
        
        typeNE = self.currentNEType.get()
        
        stringNE = self.dataTXT[self.actual_block][1][sent_index][begin_index:last_index]
        
        
        writeItem = []
        writeItem.append(sent_index)
        writeItem.append(begin_index)
        writeItem.append(last_index)
        writeItem.append(typeNE)
        writeItem.append(stringNE)
        
        self.outputFILE[self.dataTXT[self.actual_block][0]].append(writeItem)
        self.update_outputBOX()    
        
        #Color selected cells
        for sel in wordIndexes:
            self.wordsBOX.itemconfig(sel, bg=self.colors[typeNE])
    
    def update_outputBOX(self):
        self.outputBOX.delete('1.0',END)        
        string = json.dumps(self.outputFILE, sort_keys=True, indent=4, separators=[",", ":"])
        self.outputBOX.insert(END, string)
        
    def removeNE(self):
        if len(self.outputFILE[self.dataTXT[self.actual_block][0]]):    
            del self.outputFILE[self.dataTXT[self.actual_block][0]][-1]
        
        self.update_outputBOX()
            
    def saveFile(self):
        file_path = tk.filedialog.asksaveasfile(mode="w", defaultextension=".json")
        if(file_path is None):
            return
        with open("outputFILE.json", "w") as f:
            json.dump(self.outputFILE, f, ensure_ascii=False)
    
    def hello(self):
        print("ae")
    
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

        self.wordsBOX.delete(0,END)
        self.colorTextBOX.delete(0, END)
        for radio in self.locations:
            radio.grid_forget()

        self.summary = text["summary"]
        summary = self.summary
        self.locations = []
        for location in range(len(summary)):
            self.locations.append(Radiobutton(self.master, height=1, width=20, text=summary[location]["location"], variable=self.currentFormKey, value=location, command=self.changeLocation))
            self.locations[location].grid(row=location + 1, column=1, sticky=W+N+S)

        text = text["summary"][0]["content"]
        #sents = sent_tokenize(text)
        sents = None
        self.listTokens = []
        self.sizeOfSents = []
        for sent in sents:
            self.listTokens.append(word_tokenize(sent))
        for item in self.listTokens:
            self.sizeOfSents.append(len(item))
        
        # Add box of words
        for sents in self.listTokens:
            for token in sents:
                self.wordsBOX.insert(END, token)


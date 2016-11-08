from tkinter import *

class listBoxDialogWindow(object):
    
    def __init__(self, parent, text):
        
        self.toplevel = Toplevel(parent)
        
        self.set_data(text)
        
        choices = self.getChoices()
        names = StringVar(value=choices)
        
        label = Label(self.toplevel, text="Pick something:")
        self.listbox = Listbox(self.toplevel, listvariable=names, selectmode=EXTENDED, height=len(choices), width=len(max(choices, key=len)), exportselection=0)
        button = Button(self.toplevel, text="OK", command=self.toplevel.destroy)
        
        label.pack()
        self.listbox.pack()
        button.pack()
        
        self.listbox.bind("<<ListboxSelect>>", self.getSelection)
    
    def set_data(self, text):
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
                 
        self.dataTXT = dataTXT
        self.indexesTXT = allIndexes
        
    def getChoices(self):
        listChoices = []
        for item in self.dataTXT:
            listChoices.append(item[0])
        return listChoices
        
    def getSelection(self, event):
        widget = event.widget
        indexes = widget.curselection()
        self.selection = []
        for i in indexes:
            self.selection.append(widget.get(i))
        
        self.indexesChoices = []
        for item in self.selection:
            for i, data in enumerate(self.dataTXT):
                if data[0] == item:
                    self.indexesChoices.append(i)
        
    def returnAnswer(self):
        self.toplevel.wait_window()
        
        return self.selection, self.indexesChoices, self.indexesTXT, self.dataTXT

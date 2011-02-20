from Tkinter import *

class myApp:
    def __init__(self, myParent):
        self.myCont = Frame(myParent)
        self.myCont.pack()
        
        self.button1 = Button(self.myCont)
        self.button1["text"] = "Ok"
        self.button1["background"] = "green"
        self.button1.bind("<Return>", self.button1Click())
        self.button1.pack()
        
    def button1Click(self):
        if self.button1["text"] == "OK":
            self.button1["text"] = "Moo"
        else:
            self.button1["text"] = "OK"
        
root = Tk()
frame = myApp(root)
root.mainloop()
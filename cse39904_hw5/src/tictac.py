from Tkinter import *

class myTTT:
    def __init__(self, myParent):
        self.myCont = Frame(myParent)
        self.myCont.pack()
        self.mainOut = Label(self.myCont)
        self.setupGame()
        
    def setupGame(self):
        self.mainOut["text"] = "player 1, it is your turn"
        self.mainOut.pack()
        self.buttons = []
        self.clicks = 0
        self.vals = []
        self.buttonsVals = [[(1, ""), (2, ""), (3, "")],
                  [(4, ""), (5, ""), (6, "")],
                  [(7, ""), (8, ""), (9, "")]]
        for i in range(len(self.buttonsVals)):
            myFrame = Frame(self.myCont)
            #myFrame.pack()
            for j in range(len(self.buttonsVals[i])):
                pos, disp = self.buttonsVals[i][j]
                self.vals.insert(pos,0)
                myButton = Button(myFrame)
                myButton.grid(column=i,row=j)
                self.buttons.insert(i*3+j,myButton)
                #print len(self.buttons), self.buttons.index(myButton)
                self.buttons[i*3+j]["text"] = ""
                self.buttons[i*3+j]["height"] = 4
                self.buttons[i*3+j]["width"] = 4
                self.buttons[i*3+j]["command"]=lambda ind=i*3+j: self.buttonClick(ind)
                #self.buttons[i*3+j].bind("<Button-1>", self.callback(i*3+j))
                self.buttons[i*3+j].pack(side=LEFT)
                #self.myCont[symbol] = Button((4+36*j,30+36*i,32,32))
                #.bind(char, w[symbol].push)
            myFrame.pack()
        
    def callback(self,sm):
        self.buttons[sm]["background"] = "green"
        
    def buttonClick(self, sm):  ### (3)
        #print "button1Click event handler", sm
        self.clicks += 1
        player = "1"
        if self.clicks%2 == 1:
            player = "2"
        self.mainOut["text"] = "player "+player+", it is your turn"
        if player == "1":
            self.buttons[sm]["background"] = "yellow"
            self.buttons[sm]["text"] = "O"
            self.vals[sm] = -1
        else:
            self.buttons[sm]["background"] = "green"
            self.buttons[sm]["text"] = "X"
            self.vals[sm] = 1
        self.buttons[sm]['state'] = DISABLED
        self.check()
        
    def check(self):
        flag = -3
        while flag<4:
            if flag < 0:
               pl = "2" 
            else:
                pl = "1"
            for i in range(flag):
                sumr = self.vals[i*3]+self.vals[i*3+1]+self.vals[i*3+2]
                sumc = self.vals[i]+self.vals[i+3]+self.vals[i+6]
                if (sumr == flag or sumc == flag):
                    self.mainOut["text"] = "player "+pl+", WON!"
                    self.endGame()
            sumd1 = self.vals[0]+self.vals[4]+self.vals[8]
            sumd2 = self.vals[2]+self.vals[4]+self.vals[6]
            if (sumd1 == flag or sumd2 == flag):
                    self.mainOut["text"] = "player "+pl+", WON!"
                    self.endGame()
            flag +=6
        zr = 0
        if zr not in self.vals:
            self.mainOut["text"] = "it is a TIE!"
            self.endGame()
        
    def endGame(self):
        for j in range(len(self.buttons)):
            self.buttons[j]['state'] = DISABLED
        
root = Tk()
root.resizable(0,0)
frame = myTTT(root)
root.mainloop()
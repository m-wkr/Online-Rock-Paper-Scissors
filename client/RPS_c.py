#= Rock Paper Scissors Client script =#


# Import required modules #
import socket
import tkinter as tk 
from tkinter import font as tkf
from tkinter.ttk import *

### Establish client side socket attributes + related functions, and server socket information ###
selfSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
selfSocket.setblocking(True)
serverIp, serverPort = "127.0.0.1",5500  # {ALTER IP as required} #

def sendMsg(msg):
    selfSocket.send(msg.encode("ascii"))

def receiveMsg():
    return selfSocket.recv(1024).decode("ascii")

### Image based button class ###
class button:
    def __init__(self,root,imagePath,text,func,side,padx):
        self.text = text
        if imagePath != "":
            self.image = tk.PhotoImage(file=imagePath)
            self.button = tk.Button(root,text=self.text,image=self.image,compound=tk.TOP,command=func,bg="#d9d9d9",fg="#454045")
        else:
            self.image = imagePath
            self.button = tk.Button(root,text=self.text,command=func,bg="#d9d9d9",fg="#454045")

        self.button["font"] = FONT
        self.button.pack(side=side,padx=padx,pady=40)

    def getButton(self):
        return self.button

### Tkinter based GUI class ###
class GUI:
    def __init__(self):
        # Main window #
        self.root = tk.Tk()
        self.root.geometry(("640x400"))
        self.root.configure(bg="#454045")
        self.textFrame = tk.Frame(self.root,height=100,width=400,bg="#d9d9d9")
        self.textFrame.pack(side=tk.TOP)
        # Main variable text display #
        self.title = self.root.title("Online Rock Paper Scissors")
        self.varText = tk.StringVar(self.textFrame,"                                      Welcome to online Rock Paper Scissors                                       ")
        self.boardText = tk.Label(self.textFrame,textvariable=self.varText,bg="#d9d9d9",fg="#454045")
        self.boardText.pack(pady=20)
        # Menu buttons #
        self.buttons = []
        # Records server socket response #
        self.serverResponse = ""

    # Set button font
    def setFont(self,FONT):
        self.boardText["font"] = FONT

    # Update server response if the value is new and valid (not empty)
    def updateResponse(self,val):
        if val != "" and val != self.serverResponse:
            self.serverResponse = val

    # Remove tkinter buttons
    def clearButtons(self):
        for button in self.buttons:
            button.getButton().destroy()
        self.buttons = []

    ### Main GUI functionality methods ###
    # Connect to server button screen #
    def connectStatus(self):
        self.buttons.append(button(self.root,"","Connect to server",lambda:self.connect(),tk.TOP,0))


    # Attempt to connect to server #
    def connect(self):
        try:
            selfSocket.connect_ex((serverIp,serverPort))
            self.varText.set("                                                Connected to server, waiting for matching                                                ")
        except:
            self.varText.set("                                                The server is currently unreachable,                                                \n please try again later.")
        self.root.after(0,self.stageManagement)

    # Receives any/all messages provided by server script and delegates to relevant method as required #
    def stageManagement(self):
        self.clearButtons()
        self.updateResponse(receiveMsg())
        if self.serverResponse == "TERM" or self.serverResponse == "":
            self.connectStatus()
        else:
            if self.serverResponse[0] == "0":
                self.connected()
            elif self.serverResponse[0] == "1":
                self.displayOutcome()
            
    # Send a method's passed in value to server, and terminates window if the value indicates end#
    def roundInformation(self,val):
        sendMsg(val)
        if val != "no":
            self.root.after(0,self.stageManagement)
        else:
            self.root.destroy()

    # Rock paper scissors choice screen #
    def connected(self):
        self.varText.set(self.serverResponse[2:])
        self.buttons.append(button(self.root,".\\imgs\\rock.png","Rock",lambda: self.roundInformation("1"),tk.LEFT,62))
        self.buttons.append(button(self.root,".\\imgs\\paper.png","Paper",lambda: self.roundInformation("2"),tk.LEFT,62))
        self.buttons.append(button(self.root,".\\imgs\\scissors.png","Scissors",lambda: self.roundInformation("3"),tk.LEFT,62))

    # Play again/Exit choice screen #
    def displayOutcome(self):
        self.varText.set(self.serverResponse[2:])
        self.buttons.append(button(self.root,"","Play Again",lambda: self.roundInformation("yes"),tk.LEFT,112))
        self.buttons.append(button(self.root,"","Exit",lambda: self.roundInformation("no"),tk.LEFT,112))

### Instantiate GUI object and run mainloop ###
g = GUI()
FONT = tkf.Font(family="Arial",size=14,weight="bold")
g.setFont(FONT)
g.connectStatus()
g.root.mainloop()
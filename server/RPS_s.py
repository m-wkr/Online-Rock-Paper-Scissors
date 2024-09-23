#= Rock Paper Scissors Server script =#

# Import required modules #
import socket
import threading

# Establish server socket information #
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host, port = '',5500
serverSocket.bind((host,port))
serverSocket.listen(2)

# Contain any established socket connection objects #
clients = []

### Socket specific client class ###
class client:

    def __init__(self,identifier,socket,address):
        # Assigned player ID #
        self.identifier = identifier
        # Socket object and IP #
        self.socket = socket
        self.address = address
        # Client sent choice, determined outcome, and disconnection status #
        self.choice = ""
        self.outcome = ""
        self.disconnected = False
        
    # Encapsulated attribute methods #
    def getIdentifier(self):
        return self.identifier
    
    def setIdentifier(self,val):
        self.identifier = val

    def getSocket(self):
        return self.socket

    def getAddress(self):
        return self.address
    
    def getChoice(self):
        return self.choice
    
    def setChoice(self,val):
        self.choice = val

    def getDisconnected(self):
        return self.disconnected
    
    def setDisconnected(self,val):
        self.disconnected = val

    # Sending and receiving socket data methods #
    def sendMsg(self,msg):
        self.socket.send(msg.encode("ascii"))

    def receiveMsg(self):
        return self.socket.recv(1024).decode("ascii")
    
### Add successful socket connection to clients array ###
def addClientConnection(clients):
    try:
        clientSocket, clientAddr = serverSocket.accept()
        clients.append(client(str(len(clients)),clientSocket,clientAddr))
        print(f"A player has connected to the server from the IP: {clientAddr[0]}")
    except: 
        print("A connection error had occurred")

### Create threads and assign the argument function to each ###
def threadDispersal(clients,func):
    threads = []
    for i in range(len(clients)):
        threads.append(threading.Thread(target=func,args=(clients[i],)))
        threads[i].daemon = True
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

### Checks if the client response is empty or indicates disconnection ###
def emptyConnection(client):
    if client.getChoice() != "" and client.getChoice() != "no":
        return False
    client.setDisconnected(True)
    return True
    
### Predicate for checking if a function (indicating invalid input) has been met or not ###
def validateConnection(clients,func):
    for i in range(len(clients)):
        if func(clients[i]):
            return False

    return True

    
### (PHASE 0) Set clients identifier ID, relay phase 0 info to clients, and await for user response ###
def setID(clients):
    for i in range(len(clients)):
        clients[i].setIdentifier(str(i))

def roundStart(client):
    client.sendMsg("0                                                             There are sufficient players for the round to begin                                                            \nYou are player "+ client.getIdentifier())
    client.setChoice(client.receiveMsg())



### Validates client move is an expected value ###
def validatedMove(client):
    for i in range(1,4):
        if client.getChoice() == str(i):
            return False
    return True

### Compares two client moves to determine victor via modular arithmetic ###
def determineVictor(m1,m2):
    if m1%3 < m2%3:
        return m2
    elif m1%3 > m2%3:
        return m1
    else:
        return None

### Calculate which player won and return result to clients ###
def relayWinner(clients):
    result = determineVictor(int(clients[0].getChoice()),int(clients[1].getChoice()))
    if result is None:
        response = "It was a draw."
    elif result ==  int(clients[0].getChoice()):
        response = "Player " + clients[0].getIdentifier() + " won"
    else:
        response = "Player " + clients[1].getIdentifier() + " won"

    
    for i in range(len(clients)):
        clients[i].response = "1                                                                            " + response + "                                                                           "

### (1) Ask and retain clients' next round participation response ###
def nextRoundConsent(client):
    client.sendMsg(client.response)
    client.setChoice(client.receiveMsg())

### Reset client choices to default ###
def nextRoundPrep(clients):
    for client in clients:
        client.setChoice("")
    
### Send round termination signal ###
def disconnectedSignal(clients):
    for client in clients:
        client.sendMsg("TERM")

### Close and delete disconnected sockets ###
def deleteDeadClients(clients):
    for i in range(len(clients)-1,-1,-1):
        if clients[i].getDisconnected():
            clients[i].getSocket().close()
            del clients[i]
        else:
            clients[i].setChoice("")


while True:
    if len(clients) < 2:
        addClientConnection(clients)
    else:
        setID(clients)
        threadDispersal(clients,roundStart)
        if validateConnection(clients,emptyConnection) and validateConnection(clients,validatedMove):
            relayWinner(clients) 
            threadDispersal(clients,nextRoundConsent)
            if validateConnection(clients,emptyConnection):
                nextRoundPrep(clients)
            else:
                disconnectedSignal(clients)
        elif not validateConnection(clients,emptyConnection):
            disconnectedSignal(clients)

        deleteDeadClients(clients)
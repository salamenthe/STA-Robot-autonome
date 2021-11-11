import socket
from time import sleep
import threading


class cls_ServerTCP (threading.Thread) :
    def __init__(self, ipServerToConnect, portServerToConnect) :
        threading.Thread.__init__(self)
        self.ipServer = ipServerToConnect
        self.portServer = portServerToConnect
        self.lMessageToClient = []
        self.lIpClients = []
        self.lIndexClients = []

    def newClientSocket(self, clientNewSocket, addr, index) :

        clientNewSocket.settimeout(20)
        
        while True :
        # now our endpoint knows about the OTHER endpoint.
        
            msg = clientNewSocket.recv(10)
            msg = msg.decode("utf-8")

            if (msg == "%") :
                if (len(self.lMessageToClient[index]) > 0) :
                    auxMessage = self.lMessageToClient[index].pop()
                    clientNewSocket.send(bytes(auxMessage,"utf-8"))

                    while (self.lMessageToClient[index].len() > 3) :
                        self.lMessageToClient[index].pop()
                else :
                    clientNewSocket.send(bytes("%","utf-8"))

            sleep(0.01)
    
    def run(self) :

        index = 0

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ipServer, self.portServer))
        s.listen(5)

        while True :
            clientsocket, address = s.accept()
            clientsocket.settimeout(20)
            
            clientsocket.send(bytes("%","utf-8"))
            print("Client Connected...")

            msg = clientsocket.recv(20)
            msg = msg.decode("utf-8")

            print("Client: ", msg, " connected")

            self.lMessageToClient.append([])
            self.lIpClients.append(msg)
            self.lIndexClients.append(index)

            clientsocket.send(bytes("%","utf-8"))
            sleep(0.02)
            
            threading.Thread(target=lambda : self.newClientSocket(clientsocket, address, index)).start()
            index += 1
            
        
    

        
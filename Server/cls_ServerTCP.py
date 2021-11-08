import socket
from time import sleep
import threading


class cls_ServerTCP (threading.Thread) :
    def __init__(self, ipServerToConnect, portServerToConnect) :
        threading.Thread.__init__(self)
        self.ipServer = ipServerToConnect
        self.portServer = portServerToConnect
        self.lMessageToClient = []
        self.nClient = 0

    def newClientSocket(self, clientNewSocket, addr, index) :
        while True :
        # now our endpoint knows about the OTHER endpoint.

            msg = clientNewSocket.recv(10)
            msg = msg.decode("utf-8")
            clientNewSocket.settimeout(20)

            if (msg == "%") :
                if (len(self.lMessageToClient[index]) > 0) :
                    clientNewSocket.send(bytes("#","utf-8"))
                else :
                    clientNewSocket.send(bytes("%","utf-8"))
            elif (msg == "#") :
                clientNewSocket.send(bytes("$","utf-8"))
            elif (msg == "$") :
                while (len(self.lMessageToClient[index]) > 0) :
                    auxMessage = self.lMessageToClient[index].pop(0)
                    clientNewSocket.send(bytes(auxMessage,"utf-8"))
                    msg = clientNewSocket.recv(10)
                
                clientNewSocket.send(bytes("%","utf-8"))

            sleep(0.01)
    
    def run(self) :

        index = 0

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ipServer, self.portServer))
        s.listen(5)

        while True :
            clientsocket, address = s.accept()
            
            clientsocket.send(bytes("%","utf-8"))
            print("Client Connected...")
            self.lMessageToClient.append([])
            threading.Thread(target=lambda : self.newClientSocket(clientsocket, address, index)).start()
            index += 1
            
        
    

        
import socket
import threading

class cls_ClientTCP (threading.Thread) :
    def __init__(self, ipServerToConnect, portServerToConnect) :
        threading.Thread.__init__(self)
        self.ipServer = ipServerToConnect
        self.portServer = portServerToConnect
        self.lMessageToArduino = []
        self.lMessageToServer = []
    
    def run(self) :

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ipServer, self.portServer))
        print("Connected to Server")
        s.settimeout(20)

        s.send(bytes("%","utf-8"))

        while True:

            msg = s.recv(10)
            msg = msg.decode("utf-8")
            print("Message recu: ", msg)
            
            if (msg == "%") :
                if (len(self.lMessageToServer) > 0) :
                    auxMessage = self.lMessageToServer.pop(0)
                    s.send(bytes(auxMessage,"utf-8"))
                else :
                    s.send(bytes("%","utf-8"))

            else :
                if (msg[0] == 'C') :
                    self.lMessageToArduino.append(msg)
                
                s.send(bytes("%","utf-8"))
                
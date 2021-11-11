import cls_ClientTCP
import cls_ClientSerial
from time import sleep

cls_TCP = cls_ClientTCP.cls_ClientTCP("127.0.0.1", 700)
cls_Serial = cls_ClientSerial.cls_ClientSerial()

cls_TCP.start()
cls_Serial.start()

while True :
    if (len(cls_TCP.lMessageToArduino) > 0) :
        cls_Serial.lMessageToArduino.append(cls_TCP.lMessageToArduino.pop())

    sleep(0.002)

#!/usr/bin/env python3
import serial
import threading
from time import sleep

class cls_ClientSerial (threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)
        self.lMessageFromArduino = []
        self.lMessageToArduino = []
        pass

    def run(self) :
        ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

        while True :

            if (len(self.lMessageToArduino) > 0) :
                ser.write(bytes(str(self.lMessageToArduino.pop()),"utf-8"))
                sleep(0.04)


            #ser.flush()
            #while ser.in_waiting :
                #val = ser.readline()
                
            


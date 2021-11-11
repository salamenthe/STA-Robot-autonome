#!/usr/bin/env python3
import serial

ser = serial.Serial('/dev/ttyUSB0', 230400, timeout=1)
start_count = 0
auxBytesReads = [0x00, 0x00]

while True :
    auxBytesReads[start_count] = bytearray(ser.read(1))[0]

    if (start_count == 0) :
        if (auxBytesReads[start_count] == 0xFA) :
            start_count = 1

    elif (start_count == 1) :
        if (auxBytesReads[start_count] == 0xA0) :
            start_count = 0

            bytesReads = bytearray(ser.read(2518))
            bytesReads.insert(0, auxBytesReads[1])
            bytesReads.insert(0, auxBytesReads[0])
            
            

            for i in range(0, 2520, 42) :
                if bytesReads[i] == 0xFA and bytesReads[i + 1] == (0xA0 + i /42) :
                    for j in range(i + 4, i + 40, 6) :
                        index = 6*(i / 42) + (j - 4 - i) / 6

                        intensity = (bytesReads[j + 1] << 8) + bytesReads[j]
                        rangeRead = (bytesReads[j + 3] << 8) + bytesReads[j + 2]
                        if (index == 359) :
                            print("Valeur lu: ", (359 - index), " -> ", rangeRead/1000)

    



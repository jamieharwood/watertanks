#!/usr/bin/python

import serial
import json
import time
import sys

def main():
    serialData = serial.Serial('/dev/ttyAMA0',  115200)
    pumpPWM = 1500
    hose = 0
    irrigation = 0
    recSerialData = ""
    
    print("Serial read and write")
    
    settings = {'pumpPWM': pumpPWM, 'hose':hose, 'irrigation':irrigation}
    sys.stdout = open('serialLog.txt',  'a')
    
    while True:
        # Write to Arduino
        serialData.write(str.encode(json.dumps(settings) + chr(0)))
        
        # Read from Arduino
        recSerialData = serialData.readline()
        
        sys.stdout.write(str(recSerialData))
        sys.stdout.write(chr(0))
        sys.stdout.flush()
        #sys.stdout.close()
        
        #line = serialData.readline()
        
        #print("Serial data:{0}:", line)
        
        time.sleep(1)
        
main()

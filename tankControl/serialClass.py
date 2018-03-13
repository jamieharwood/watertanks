#!/usr/bin/env python

import serial
import json
import sys
#import string
#import datetime

class sensorComm():
    def __init__(self):
        self.serialData = serial.Serial('/dev/ttyAMA0',  115200)
        self.pumpPWM = 1500
        self.hose = 0
        self.irrigation = 0
        self.logToDisk = False
        self.recSerialData =""
        self.settings = {'pumpduration': 5}
        sys.stdout = open('serialLog.txt',  'a')

    def __call__(self):
        self.__init__()
    
    def setValues(self):
        # Write to Arduino
        #nowTime = datetime.datetime.now()
        settings = {'pumpPWM': self.pumpPWM, 'hose':self.hose, 'irrigation':self.irrigation}#, 'datestamp':nowTime.isoformat(),  'MT':'control:001'}
        message = str.encode(json.dumps(settings) + chr(0))
        
        self.serialData.write(message)
        
        return message
        
    def refresh(self):
        # Read from Arduino
        self.recSerialData = str(self.serialData.readline())
        newStr = self.recSerialData.replace('b\'', '')
        newStr = newStr.replace('\\r\\n\'', '')
        
        if (len(newStr) > 0):
            try:
                self.settings= json.loads(newStr)
            except:
                self.refresh()
        else:
            self.refresh()
        
        if (self.logToDisk == True):
            sys.stdout.write(str(self.recSerialData))
            sys.stdout.write(chr(0))
            sys.stdout.flush()
        
        return self.recSerialData

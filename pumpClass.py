#!/usr/bin/env python

from settings import settingsClass
import automationhat
import RPi.GPIO as gpio

class pump():

    def __init__(self):
        self.mySettings = settingsClass()
    
        self.pumpOn = False
        self.hoseOn = 0
        self.irrigationOn = False
    
        self.displayBrightness = 0.5
        self.outpin = 0
        self.pwmMid = 0
        self.pwmHigh = 0
        self.myPwm = gpio
        
        self.initHardware()
    
    def __call__(self):
        self.initHardware()
    
    def initHardware(self):
        if automationhat.is_automation_hat():
            # init local automation hat
            automationhat.light.power.write(1)
        
        mySettings = settingsClass() # get settings from db
        #mySettings.resetSettings()
        
        # setup pwm
        self.outpin = mySettings.settings['pwmPin']
        #pwmLow = mySettings.settings['pwmLow'] # Not used as this would reverse the pump
        self.pwmMid = mySettings.settings['pwmMid']
        self.pwmHigh = mySettings.settings['pwmHigh']
        
        self.hoseOn = self.pwmMid
        
        # Start pwm
        gpio.setmode(gpio.BCM)
        gpio.setup(self.outpin,  gpio.OUT)
        self.myPwm = gpio.PWM(self.outpin, mySettings.settings['pwmFrequency'])
        self.myPwm.start(self.pwmMid) # pump init
    
    def setIrrigationOn(self,  value):
        
        if (value == 0):
            self.irrigationOn = False
        else:
            self.irrigationOn = True
        
        self.setPumpPhysicalState()
    
    def getIrrigationOn(self):
        return self.irrigationOn
        
    def setHoseOn(self,  value):
        if (value == 0):
            self.hoseOn = False
        else:
            self.hoseOn = True
        
        self.setPumpPhysicalState()
    
    def getHoseOn(self):
        return self.hoseOn
    
    def setPumpPhysicalState(self):
        
        # action the water solenoid and pump
        automationhat.output.one.write(self.hoseOn) # irrigation solenoid on
        automationhat.output.two.write(self.irrigationOn) # hose solenoid off
        
        if (self.hoseOn or self.irrigationOn):
            self.pumpOn = self.pwmMid
        else:
            self.pumpOn = self.pwmHigh
            
        self.myPwm.start(self.pumpOn) # pump start






#!/usr/bin/env python

from settings import settingsClass
from sunrisesetClass import sunRiseSet
from ledcontrolClass import ledcontrol
import datetime
import automationhat
import RPi.GPIO as gpio

def main():
    state = -2
    myLedControl = ledcontrol()
    
    if automationhat.is_automation_hat():
        automationhat.light.power.write(1)
    
    automationhat.light.comms.write(1)
    mySettings = settingsClass()
    #mySettings.resetSettings()
    outpin = mySettings.settings['pwmPin']
    pwmLow = mySettings.settings['pwmLow']
    pwmMid = mySettings.settings['pwmMid']
    pwmHigh = mySettings.settings['pwmHigh']
    
    # Start pwm
    gpio.setmode(gpio.BCM)
    gpio.setup(outpin,  gpio.OUT)
    myPwm = gpio.PWM(outpin, mySettings.settings['pwmFrequency'])
    
    # Get sunrise and sunset from DB
    mySunrise = sunRiseSet()
    
    automationhat.light.comms.write(0)
        
    while True:
        myTimeNow = datetime.datetime.now()
        
        numStartTime = (myTimeNow.hour * 3600) + (myTimeNow.minute * 60) + myTimeNow.second
        
        if (((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) or (numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60)))) and state != 1):
            state = 1
            automationhat.light.comms.write(1) # Comm light on to show activity.
            
            automationhat.output.one.write(1)
            automationhat.relay.one.write(1)
            
            automationhat.output.two.write(0)
            automationhat.relay.two.write(0)
            
            myLedControl.setIrrigationGreen(1)
            myLedControl.setHoseGreen(0)
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (automationhat.input.one.read() == True and state != 2):
            state = 2
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.two.write(0)
            automationhat.relay.two.write(0)
            
            automationhat.output.two.write(1)
            automationhat.relay.two.write(1)
            
            myLedControl.setIrrigationGreen(0)
            myLedControl.setHoseGreen(1)
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (automationhat.input.one.read() == False and state != 0):
            state = 0
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.one.write(0)
            automationhat.relay.one.write(0)
            
            automationhat.output.two.write(0)
            automationhat.relay.two.write(0)
            
            
            myLedControl.setIrrigationGreen(0)
            myLedControl.setHoseGreen(0)
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (state == -2):
            state = -1
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            myLedControl.setIrrigationGreen(0)
            myLedControl.setHoseGreen(0)
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
    
main()

#!/usr/bin/env python

from settings import settingsClass
from sunrisesetClass import sunRiseSet
from ledcontrolClass import ledcontrol
import datetime
import automationhat
import RPi.GPIO as gpio

def main():
    state = -2
    myLedControl = ledcontrol() # init remote led control
    
    if automationhat.is_automation_hat():
        # init local automation hat
        automationhat.light.power.write(1)
    
    automationhat.light.comms.write(1)
    mySettings = settingsClass() # get settings from db
    #mySettings.resetSettings()
    outpin = mySettings.settings['pwmPin']
    pwmLow = mySettings.settings['pwmLow']
    pwmMid = mySettings.settings['pwmMid']
    pwmHigh = mySettings.settings['pwmHigh']
    
    # Start pwm
    gpio.setmode(gpio.BCM)
    gpio.setup(outpin,  gpio.OUT)
    myPwm = gpio.PWM(outpin, mySettings.settings['pwmFrequency'])
    myPwm.start(pwmMid) # pump init
    
    # Get sunrise and sunset from DB
    mySunrise = sunRiseSet()
    
    automationhat.light.comms.write(0)
        
    while True:
        myTimeNow = datetime.datetime.now()
        
        numStartTime = (myTimeNow.hour * 3600) + (myTimeNow.minute * 60) + myTimeNow.second
        
        if (((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) or (numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60)))) and state != 1):
            # irrigation requested
            state = 1
            automationhat.light.comms.write(1) # Comm light on to show activity.
            
            automationhat.output.one.write(1) # irrigation led on
            # automationhat.relay.one.write(1) # irrigation solenoid start
            
            automationhat.output.two.write(0) # hose led off
            # automationhat.relay.two.write(0) # hose solenoid stop
            
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (automationhat.input.one.read() == True and state != 2):
            # hose requested on
            state = 2
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.two.write(0) # irrigation led off
            # automationhat.relay.two.write(0) # irrigation solenoid stop
            
            automationhat.output.two.write(1) # hose led on
            # automationhat.relay.two.write(1) # hose solenoid start
            
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(1) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (automationhat.input.one.read() == False and state != 0):
            # hose requested off
            state = 0
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.one.write(0) # irrigation led off
            # automationhat.relay.one.write(0) # irrigation solenoid stop
            
            automationhat.output.two.write(0) # hose led off
            # automationhat.relay.two.write(0) # hose solenoid stop
            
            myPwm.start(pwmMid) # pump stop
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (state == -2):
            # BAU state
            state = -1
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.one.write(0) # irrigation led off
            # automationhat.relay.one.write(0) # irrigation solenoid stop
            
            automationhat.output.two.write(0) # hose led off
            # automationhat.relay.two.write(0) # hose solenoid stop
            
            myPwm.start(pwmMid) # pump stop
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
    
main()

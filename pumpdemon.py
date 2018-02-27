#!/usr/bin/env python

from settings import settingsClass
from sunrisesetClass import sunRiseSet
from ledcontrolClass import ledcontrol
import datetime
import automationhat
import RPi.GPIO as gpio

import time
#import signal
import scrollphathd
from scrollphathd.fonts import font5x7
#from scrollphathd.fonts import font3x5

def getStatusText(sunrise,  sunset):
    nowTime = datetime.datetime.now()
    if (nowTime.minute > 9):
        returnString = "  *" + str(nowTime.hour) + ":" + str(nowTime.minute) + chr(0)
    else:
        returnString = "  *" + str(nowTime.hour) + ":0" + str(nowTime.minute) + chr(0)
    returnString = returnString + chr(0) + chr(30) + sunrise[0:5] +"  "
    returnString = returnString + chr(31) + sunset[0:5]
    #eturnString = returnString + chr(8)
    #returnString= char(1)
    return returnString

def main():
    state = -2 # Startup state
    
    myLedControl = ledcontrol() # init remote led control
    
    if automationhat.is_automation_hat():
        # init local automation hat
        automationhat.light.power.write(1)
    
    automationhat.light.comms.write(1)
    
    time.sleep(0.05) # sleep to give the system time to set the LEDs
    
    mySettings = settingsClass() # get settings from db
    #mySettings.resetSettings()
    
    # setup pwm
    outpin = mySettings.settings['pwmPin']
    #pwmLow = mySettings.settings['pwmLow']
    pwmMid = mySettings.settings['pwmMid']
    pwmHigh = mySettings.settings['pwmHigh']
    
    # Start pwm
    gpio.setmode(gpio.BCM)
    gpio.setup(outpin,  gpio.OUT)
    myPwm = gpio.PWM(outpin, mySettings.settings['pwmFrequency'])
    myPwm.start(pwmMid) # pump init
    
    # Set sunrise sunset vars
    dayRollover = -1 # get new sunrise sunset times only once!
    mySunrise = sunRiseSet() # Get sunrise and sunset from DB
    
    # Config the display
    scrollphathd.set_brightness(0.5)
    #displayText = getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset))
    #scrollphathd.write_string(displayText , x=0, y=0, font=font5x7, brightness=0.7)
    #scrollphathd.write_string(displayText , x=0, y=0, font=font3x5, brightness=0.5)
    
    automationhat.light.comms.write(0)
    
    myTimeNow = datetime.datetime.now()
    currTime = myTimeNow.hour + myTimeNow.minute
    lastTime = currTime
    
    while True:
        myTimeNow = datetime.datetime.now()
        currTime = myTimeNow.hour + myTimeNow.minute
        
        if (currTime != lastTime):
            lastTime = currTime
            scrollphathd.clear()
            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness=0.5)
        
        rollTime = myTimeNow.hour + myTimeNow.minute
        #rollTime = 0
        if (rollTime == 0 and dayRollover == -1):
            mySunrise = sunRiseSet()
            dayRollover = 0
        elif (rollTime == 0 and dayRollover == 0):
            dayRollover = 0
        else:
            dayRollover = -1
        
        numStartTime = (myTimeNow.hour * 3600) + (myTimeNow.minute * 60) + myTimeNow.second
        
        # complex if conditions so I pulled them into variables
        ifSunrise = ((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1)
        ifSunset = ((numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1)
        ifHose = (automationhat.input.one.read() == True and state != 3)
        ifBauFromSunrise = (not(numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 1)
        ifBauFromSunset = (not(numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 2)
        ifBauFromStartup = ((automationhat.input.one.read() == False and state == 3) or state == -2)
        
        #if ((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1):
        if (ifSunrise):
            # sunrise irrigation requested
            state = 1 # Sunrise state
            automationhat.light.comms.write(1) # Comm light on to show activity.
            scrollphathd.clear()
            scrollphathd.write_string('  irrigation on: ' + str(mySettings.settings["pumpduration"]) + ' mins', x=0, y=0, font=font5x7, brightness=0.3)
            
            automationhat.output.one.write(1) # irrigation led on
            automationhat.output.two.write(0) # hose led off
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifSunset):
        #elif ((numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1):
            # sunset irrigation requested
            state = 2 # Sunset state
            automationhat.light.comms.write(1) # Comm light on to show activity.
            scrollphathd.clear()
            scrollphathd.write_string('  irrigation on: ' + str(mySettings.settings["pumpduration"]) + ' mins', x=0, y=0, font=font5x7, brightness=0.3)
            
            automationhat.output.one.write(1) # irrigation led on
            automationhat.output.two.write(0) # hose led off
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifHose):
        #elif (automationhat.input.one.read() == True and state != 3):
            # hose requested on
            state = 3 # Hose state
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            scrollphathd.clear()
            scrollphathd.write_string(' hose On', x=0, y=0, font=font5x7, brightness=0.7)
            
            automationhat.output.two.write(0) # irrigation led off
            automationhat.output.two.write(1) # hose led on
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(1) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
#        if (ifBauFromSunrise):
        #elif (not(numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 1):
            # BAU state
#            state = -1
#            scrollphathd.clear()
#            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness=0.5)
#            
#            automationhat.light.comms.write(1) # Comm light  on to show activity.
#            
#            automationhat.output.one.write(0) # irrigation led off
#            automationhat.output.two.write(0) # hose led off
#            myPwm.start(pwmMid) # pump stop
#            
#            myLedControl.setIrrigationGreen(0) # update remote display
#            myLedControl.setHoseGreen(0) # update remote display
#            
#            automationhat.light.comms.write(0) # Comm light off to show activity.
#        elif(ifBauFromSunset):
        #elif (not(numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 2):
            # BAU state
#            state = -1
#            scrollphathd.clear()
#            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness=0.5)
#            
#            automationhat.light.comms.write(1) # Comm light  on to show activity.
#            
#            automationhat.output.one.write(0) # irrigation led off
#            automationhat.output.two.write(0) # hose led off
#            myPwm.start(pwmMid) # pump stop
#            
#            myLedControl.setIrrigationGreen(0) # update remote display
#            myLedControl.setHoseGreen(0) # update remote display
#            
#            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifBauFromSunrise or ifBauFromSunset or ifBauFromStartup):
        #elif ((automationhat.input.one.read() == False and state == 3) or state == -2):
            # BAU state
            state = -1
            scrollphathd.clear()
            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness=0.5)
            
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            automationhat.output.one.write(0) # irrigation led off
            automationhat.output.two.write(0) # hose led off
            myPwm.start(pwmMid) # pump stop
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        
        # Scroll the display
        scrollphathd.show()
        scrollphathd.scroll()
        #time.sleep(0.05)
main()

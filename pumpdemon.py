#!/usr/bin/env python

from settings import settingsClass
from sunrisesetClass import sunRiseSet
from ledcontrolClass import ledcontrol
from weatherClass import weather
import datetime
import automationhat
import RPi.GPIO as gpio

#import time
#import signal
import scrollphathd
from scrollphathd.fonts import font5x7
#from scrollphathd.fonts import font3x5

def getStatusTrendText(trend):
    nowTime = datetime.datetime.now()
    trend = trend[1:len(trend)-1]
    
    if (nowTime.minute > 9):
        returnString = "  @" + str(nowTime.hour) + ":" + str(nowTime.minute)
    else:
        returnString = "  @" + str(nowTime.hour) + ":0" + str(nowTime.minute)
    
    returnString = returnString + chr(0) + "no irrigation due to " + trend.lower() +"."
    
    return returnString

def getStatusText(sunrise,  sunset):
    nowTime = datetime.datetime.now()
        
    if (nowTime.minute > 9):
        returnString = "  @" + str(nowTime.hour) + ":" + str(nowTime.minute) + chr(0)
    else:
        returnString = "  @" + str(nowTime.hour) + ":0" + str(nowTime.minute) + chr(0)
    returnString = returnString + chr(0) + chr(30) + sunrise[0:5] +"  "
    returnString = returnString + chr(31) + sunset[0:5]
    #eturnString = returnString + chr(8)
    #returnString= char(1)
    return returnString

def main():
    displayBrightness = 0.5
    state = -2 # Startup state
    myWeather  = weather()
    myLedControl = ledcontrol() # init remote led control
    
    if automationhat.is_automation_hat():
        # init local automation hat
        automationhat.light.power.write(1)
    
    automationhat.light.comms.write(1)
    
    #time.sleep(0.05) # sleep to give the system time to set the LEDs
    
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
    
    automationhat.light.comms.write(0)
    
    myTimeNow = datetime.datetime.now()
    currTime = myTimeNow.hour + myTimeNow.minute
    lastTime = currTime
    currHour = -1
    lastHour = -2
    
    while True:
        myTimeNow = datetime.datetime.now()
        currTime = myTimeNow.hour + myTimeNow.minute
        currHour = myTimeNow.hour
        
        # Update the time string for the display every minute
        if (currTime != lastTime and state == -1):
            lastTime = currTime
            scrollphathd.clear()
            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness=0.5)
        
        # Update the weather trend (last 24 hours) every hour
        if (currHour != lastHour):
            lastHour = currHour
            myWeather.getWeather()
            myWeather.getRecentTrend()
        
        # get new sunrise and sunset times
        rollTime = myTimeNow.hour + myTimeNow.minute
        if (rollTime == 0 and dayRollover == -1):
            mySunrise = sunRiseSet()
            dayRollover = 0
        elif (rollTime == 0 and dayRollover == 0):
            dayRollover = 0
        else:
            dayRollover = -1
        
        numStartTime = (myTimeNow.hour * 3600) + (myTimeNow.minute * 60) + myTimeNow.second
        
        # complex if conditions so I pulled them into variables
        ifWeatherTrend = ((myWeather.isTrend('Rain') or myWeather.isTrend('Snow')) and state != 5)
        ifSunrise = ((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1)
        ifSunset = ((numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 4)
        ifIrrigationButton = (automationhat.input.two.read() == True and state != 3)
        ifHose = (automationhat.input.one.read() == True and state != 2)
        #ifIrrigationAndHose = (automationhat.input.one.read() == True and automationhat.input.two.read() == True)
        ifBauFromSunrise = (not(numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 1) 
        ifBauFromSunset = (not(numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 4)
        ifBauFromIrrigationButton = (automationhat.input.two.read() == False and state == 3)
        ifBauFromStartup = ((automationhat.input.one.read() == False and state == 2) or state == -2)
        
        if (ifWeatherTrend == True and (ifHose == False and state != 2)):
            state = 5 # Sunrise state
            scrollphathd.clear()
            scrollphathd.write_string(getStatusTrendText(myWeather.trend), x=0, y=0, font=font5x7, brightness=displayBrightness)
            
        elif (automationhat.input.one.read() == True and automationhat.input.two.read() == True):
            #Fail
            scrollphathd.clear()
            scrollphathd.write_string(' Fail!!!', x=0, y=0, font=font5x7, brightness=0.9)
            
        elif (ifSunrise):
            # sunrise irrigation requested
            state = 1 # Sunrise state
            automationhat.light.comms.write(1) # Comm light on to show activity.
            
            scrollphathd.clear()
            scrollphathd.write_string('  irrigation on: ' + str(mySettings.settings["pumpduration"]) + ' mins', x=0, y=0, font=font5x7, brightness = displayBrightness)
            
            # action the water solenoid and pump
            automationhat.output.one.write(1) # irrigation solenoid on
            automationhat.output.two.write(0) # hose solenoid off
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifSunset):
            # sunrise irrigation requested
            state = 4 # Sunset state
            automationhat.light.comms.write(1) # Comm light on to show activity.
            
            scrollphathd.clear()
            scrollphathd.write_string('  irrigation on: ' + str(mySettings.settings["pumpduration"]) + ' mins', x=0, y=0, font=font5x7, brightness = displayBrightness)
            
            # action the water solenoid and pump
            automationhat.output.one.write(1) # irrigation solenoid on
            automationhat.output.two.write(0) # hose solenoid off
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifIrrigationButton):
            # sunrise irrigation requested
            state = 3 # Sunrise state
            automationhat.light.comms.write(1) # Comm light on to show activity.
            
            scrollphathd.clear()
            scrollphathd.write_string('  irrigation on: ' + str(mySettings.settings["pumpduration"]) + ' mins', x=0, y=0, font=font5x7, brightness = displayBrightness)
            
            automationhat.output.one.write(1) # irrigation solenoid on
            automationhat.output.two.write(0) # hose solenoid off
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifHose):
            # hose requested on
            state = 2 # Hose state
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            scrollphathd.clear()
            scrollphathd.write_string(' hose On', x=0, y=0, font=font5x7, brightness = displayBrightness)
            
            
            # action the water solenoid and pump
            automationhat.output.two.write(0) # irrigation solenoid off
            automationhat.output.two.write(1) # hose solenoid on
            myPwm.start(pwmHigh) # pump start
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(1) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifBauFromSunrise or ifBauFromSunset or ifBauFromStartup or ifBauFromIrrigationButton):
            # BAU state
            state = -1
            automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            scrollphathd.clear()
            scrollphathd.write_string(getStatusText(str(mySunrise.sunrise),  str(mySunrise.sunset)) , x=0, y=0, font=font5x7, brightness = displayBrightness)
            
            # action the water solenoid and pump
            automationhat.output.one.write(0) # irrigation led off
            automationhat.output.two.write(0) # hose led off
            myPwm.start(pwmMid) # pump stop
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            automationhat.light.comms.write(0) # Comm light off to show activity.
        
        # Scroll the display
        scrollphathd.show()
        scrollphathd.scroll()
        
main()

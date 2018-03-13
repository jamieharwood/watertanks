#!/usr/bin/env python
import RPi.GPIO as gpio
from settings import settingsClass
from sunrisesetClass import sunRiseSet
from ledcontrolClass import ledcontrol
from weatherClass import weather
import datetime
#import automationhat
from serialClass import sensorComm
#from PIL import ImageFont
#import inkyphat
#from mqClass import mqSensor,  mqControl
#import pika

#mySensor = sensorComm()

#def sendMQ(message):
#        if (isinstance(message,  str) or isinstance(message,  bytes)):
#            if (len(message)>0):
#                connection = pika.BlockingConnection(pika.URLParameters('amqp://tank:skinner2@192.168.86.43:5672/%2F?heartbeat_interval=1'))
#            
#                channel = connection.channel()
#            
#                channel.basic_publish(exchange='',routing_key='tank-to-control',  body=message)
#            
#                connection.close()
irrigationPin = 23
hosePin = 25
powerPin = 24

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
    
    return returnString
    
def main():
    gpio.setmode(gpio.BCM)
    gpio.setup([irrigationPin,  hosePin,  powerPin],  gpio.OUT)
    gpio.output([irrigationPin,  hosePin],  gpio.LOW)
    gpio.output([powerPin],  gpio.HIGH)
    
    #mqMessage = ""
    state = -2 # Startup state
    myWeather  = weather()
    myLedControl = ledcontrol() # init remote led control
    mySensor = sensorComm()
    #myMqSensor = mqSensor()
    #myMqControl = mqControl()
    mySettings = settingsClass() # get settings from db
    #mySettings.resetSettings()
    
    #automationhat.is_automation_hat()
    
    #if automationhat.is_automation_hat():
        # init local automation hat
        #automationhat.light.power.write(1)
    
    #automationhat.light.comms.write(1)
    
    #  setup pwm
    #pwmLow = mySettings.settings['pwmLow']
    pwmMid = mySettings.settings['pwmMid']
    pwmHigh = mySettings.settings['pwmHigh']
    
    # Start pwm
    # serial comm to the Arduino to set/get sensor data.
    mySensor.pumpPWM = pwmMid
    mySensor.setValues()
    #mqMessage = mySensor.setValues()
    #myMqControl.sendMQ(mqMessage)
    mySensor.refresh()
    #mqMessage = mySensor.refresh()
    #myMqSensor.sendMQ(mqMessage)
    
    # Set sunrise sunset vars
    dayRollover = -1 # get new sunrise sunset times only once!
    mySunrise = sunRiseSet() # Get sunrise and sunset from DB
    
    # Config the display
    #scrollphathd.set_brightness(0.5)
    
    myTimeNow = datetime.datetime.now()
    currTime = myTimeNow.hour + myTimeNow.minute
    lastTime = currTime
    currHour = -1
    lastHour = -2
    
    myWeather.getWeather()
    #automationhat.light.comms.write(0)
    
    while True:
        myTimeNow = datetime.datetime.now()
        currTime = myTimeNow.hour + myTimeNow.minute
        currHour = myTimeNow.hour
        
        # Update the time string for the display every minute
        if (currTime != lastTime and state == -1):
            lastTime = currTime
        
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
        
        #automationhat.light.comms.write(1) # Comm light on to show activity.

        mySensor.refresh()
        #mqMessage = mySensor.refresh()
        #myMqSensor.sendMQ(mqMessage)
        #automationhat.light.comms.write(0) # Comm light on to show activity.
        
        # complex if conditions so I pulled them into variables
        ifWeatherTrend = ((myWeather.isTrend('Rain') or myWeather.isTrend('Snow')) and state != 5)
        ifSunrise = ((numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 1)
        ifSunset = ((numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state != 4)
        
        ifIrrigationButton = (str(mySensor.settings['irrigationButton']) =='1');
        ifHose = (str(mySensor.settings['hoseButton']) =='1') ;
        
        ifBauFromSunrise = (not(numStartTime >= mySunrise.numSunriseSeconds and numStartTime <= (mySunrise.numSunriseSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 1) 
        ifBauFromSunset = (not(numStartTime >= mySunrise.numSunsetSeconds and numStartTime <= (mySunrise.numSunsetSeconds + (mySettings.settings["pumpduration"] * 60))) and state == 4)
        ifBauFromIrrigationButton = (ifIrrigationButton == False and state == 3)
        ifBauFromHoseButton = (ifHose == False and state == 2)
        ifBauFromStartup = ((ifIrrigationButton or ifHose) and state == -2)
        
        if (ifWeatherTrend == True and (ifHose == False and state != 2)):
            state = 5 # Weather is rain or snow 
            #automationhat.light.comms.write(1) # Comm light on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 0
            mySensor.pumpPWM = pwmMid
            mySensor.setValues()
            gpio.output([irrigationPin,  hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display            
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifIrrigationButton and ifHose):
            #Fail
            #automationhat.light.comms.write(1) # Comm light on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 0
            mySensor.pumpPWM = pwmHigh
            mySensor.setValues()
            gpio.output([irrigationPin,  hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display            
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifSunrise):
            # sunrise irrigation requested
            state = 1 # Sunrise state
            #automationhat.light.comms.write(1) # Comm light on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 1
            mySensor.pumpPWM = pwmHigh
            mySensor.setValues()
            gpio.output([irrigationPin],  gpio.HIGH)
            gpio.output([hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifSunset):
            # sunrise irrigation requested
            state = 4 # Sunset state
            #automationhat.light.comms.write(1) # Comm light on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 1
            mySensor.pumpPWM = pwmHigh
            mySensor.setValues()
            gpio.output([irrigationPin],  gpio.HIGH)
            gpio.output([hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifIrrigationButton and state != 3):
            # sunrise irrigation requested
            state = 3 # Sunrise state
            #automationhat.light.comms.write(1) # Comm light on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 1
            mySensor.pumpPWM = pwmHigh
            mySensor.setValues()
            gpio.output([irrigationPin],  gpio.HIGH)
            gpio.output([hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(1) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifHose and state != 2):
            # hose requested on
            state = 2 # Hose state
            #automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            mySensor.hose = 1
            mySensor.irrigation = 0
            mySensor.pumpPWM = pwmHigh
            mySensor.setValues()
            gpio.output([irrigationPin],  gpio.LOW)
            gpio.output([hosePin],  gpio.HIGH)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(1) # update remote display
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        elif (ifBauFromSunrise or ifBauFromSunset or ifBauFromStartup or ifBauFromIrrigationButton or ifBauFromHoseButton):
            # BAU state
            state = -1
            #automationhat.light.comms.write(1) # Comm light  on to show activity.
            
            mySensor.hose = 0
            mySensor.irrigation = 0
            mySensor.pumpPWM = pwmMid
            mySensor.setValues()
            gpio.output([irrigationPin,  hosePin],  gpio.LOW)
            #mqMessage = mySensor.setValues()
            #myMqControl.sendMQ(mqMessage)
            
            myLedControl.setIrrigationGreen(0) # update remote display
            myLedControl.setHoseGreen(0) # update remote display
            
            #automationhat.light.comms.write(0) # Comm light off to show activity.
        
main()

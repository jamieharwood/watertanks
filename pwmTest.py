#!/usr/bin/env python

import RPi.GPIO as gpio
from time import sleep
from settings import settingsClass

def main():
    mySettings = settingsClass()
    #mySettings.resetSettings()
    outpin = mySettings.settings['pwmPin']
    pwmLow = mySettings.settings['pwmLow']
    pwmMid = mySettings.settings['pwmMid']
    pwmHigh = mySettings.settings['pwmHigh']
    
    gpio.setmode(gpio.BCM)
    
    gpio.setup(outpin,  gpio.OUT)
    
    myPwm = gpio.PWM(outpin, mySettings.settings['pwmFrequency'])
    
    myPwm.start(pwmMid)
    sleep(5)
    
    while True:
        #myPwm.ChangeDutyCycle(1)

        myPwm.ChangeDutyCycle(pwmLow) # Low
        sleep(0.25)
        myPwm.ChangeDutyCycle(pwmMid) # mid pwm
        sleep(0.25)
        myPwm.ChangeDutyCycle(pwmHigh) # High
        sleep(0.25)
        myPwm.ChangeDutyCycle(pwmMid) # mid pwm
        sleep(0.25)
        
    #myPwm.ChangeDutyFrequency(1000)
    
main()

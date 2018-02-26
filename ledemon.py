#!/usr/bin/env python

from gpiozero import StatusBoard
from time import sleep
from ledcontrol import ledcontrolClass

def main():
    sb = StatusBoard(pwm=True)
    myLed = ledcontrolClass()
    
    while True:
        myLed.getStatus()
        
        sb.one.lights.green.value =  myLed.getWeatherGreen()
        sb.one.lights.red.value =  myLed.getWeatherRed()
        
        sb.two.lights.green.value =  myLed.getSunriseGreen()
        sb.two.lights.red.value =  myLed.getSunriseRed()
        
        sb.three.lights.green.value =  myLed.getSunsetGreen()
        sb.three.lights.red.value =  myLed.getSunsetRed()
        
        sleep(10)

main()

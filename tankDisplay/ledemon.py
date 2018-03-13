#!/usr/bin/env python

from gpiozero import StatusBoard
from time import sleep
from ledcontrol import ledcontrolClass

def main():
    sb = StatusBoard()#pwm=True)#7'weather','sunrise', 'sunset', 'irrigation', 'hose')
    myLed = ledcontrolClass()
    
    while True:
        myLed.getStatus()
        
        sb.one.lights.green.value =  myLed.getWeatherGreen()
        sb.one.lights.red.value =  myLed.getWeatherRed()
        
        sb.two.lights.green.value =  myLed.getSunriseGreen()
        sb.two.lights.red.value =  myLed.getSunriseRed()
        
        sb.three.lights.green.value =  myLed.getSunsetGreen()
        sb.three.lights.red.value =  myLed.getSunsetRed()
        
        sb.four.lights.green.value =  myLed.getIrrigationGreen()
        sb.four.lights.red.value =  myLed.getIrrigationRed()
        
        sb.five.lights.green.value =  myLed.getHoseGreen()
        sb.five.lights.red.value =  myLed.getHoseRed()
        sleep(2)

main()

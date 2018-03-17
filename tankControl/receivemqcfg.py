#!/usr/bin/env python

import RPi.GPIO as gpio

settings = []

ipAddress = '192.168.86.43'
    
powerPin = 17
pwmLedPin = 24
pwmPin = 18
irrigationPin = 23
hosePin = 25
relayHosePin = 20
relayIrrigationPin = 21

pwm = gpio.PWM

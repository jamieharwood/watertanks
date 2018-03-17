#!/usr/bin/env python

#import json
#from mqClass import mq
import RPi.GPIO as gpio
import pika
import json
import receivemqcfg as cfg

def receivetank_sendor_send(ch, method, properties, body):
        buffer = str(body).replace('b\'', '')
        buffer = buffer.replace('}\'', '}')
        buffer = buffer.replace('\\r\\n\'', '')
        #print(buffer)
        
        cfg.settings = json.loads(buffer)
        
        if (cfg.settings['hose'] == 0):    
            gpio.output(cfg.hosePin,  gpio.LOW)
            gpio.output(cfg.relayHosePin,  gpio.HIGH)
        else:
            gpio.output(cfg.hosePin,  gpio.HIGH)
            gpio.output(cfg.relayHosePin,  gpio.LOW)
        
        if (cfg.settings['irrigation'] == 0):
            gpio.output(cfg.irrigationPin,  gpio.LOW)
            gpio.output(cfg.relayIrrigationPin,  gpio.HIGH)
        else:
            gpio.output(cfg.irrigationPin,  gpio.HIGH)
            gpio.output(cfg.relayIrrigationPin,  gpio.LOW)
        
        if (cfg.settings['pump'] == 0):
            gpio.output(cfg.pwmLedPin,  gpio.LOW)
            #gpio.setup(cfg.pwmPin,  gpio.LOE)
            cfg.pwm.ChangeDutyCycle(50.0)
        else:
            gpio.output(cfg.pwmLedPin,  gpio.HIGH)
            cfg.pwm.ChangeDutyCycle(75.0)
        
        print("Received: %r" % buffer)
        
        #ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    ipAddress = '192.168.86.43'
    
    #cfg.powerPin = 17
    #cfg.pwmLedPin = 24
    #cfg.pwmPin = 18
    #cfg.irrigationPin = 23
    #cfg.hosePin = 25
    
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup([cfg.irrigationPin,  cfg.hosePin,  cfg.pwmLedPin,  cfg.powerPin,  cfg.pwmPin, cfg.relayHosePin,  cfg.relayIrrigationPin],  gpio.OUT)
    gpio.output([cfg.irrigationPin,  cfg.hosePin,  cfg.pwmLedPin, cfg.relayHosePin,  cfg.relayIrrigationPin],  gpio.LOW)
    gpio.output(cfg.powerPin,  gpio.HIGH)
    cfg.pwm = gpio.PWM(cfg.pwmPin,  200)
    cfg.pwm.start(50.0)
    
    connection = pika.BlockingConnection(pika.URLParameters('amqp://tank:skinner2@{0}:5672/%2F?heartbeat_interval=1'.replace('{0}',  ipAddress)))
    channel = connection.channel()
        
    channel.basic_consume(receivetank_sendor_send, queue='tanksendor-send',  no_ack=True)
    

    channel.start_consuming()
main()


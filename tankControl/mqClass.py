#!/usr/bin/env python

import pika

class mq():
    def __init__(self):
        self.lastMessage = ""
        self.lastQueue = ""

    def __call__(self):
        self.__init__()
    
    def sendMQ(self, queue,  message):
        
        self.lastMessage = message
        self.lastQueue = queue
        
        if (isinstance(message,  str) or isinstance(message,  bytes)):
            if (len(message)>0):
                connection = pika.BlockingConnection(pika.URLParameters('amqp://tank:skinner2@192.168.86.43:5672/%2F?heartbeat_interval=1'))
            
                channel = connection.channel()
            
                channel.basic_publish(exchange='',routing_key=queue,  body=message)
            
                connection.close()

class mqSensor(mq):
    def __init__(self):
        self.lastMessage = ""
        self.lastQueue = ""

    def __call__(self):
        self.__init__()
            
    def sendMQ(self, message):
        queue = 'tank-to-control'
        
        self.lastMessage = message
        self.lastQueue = queue
        
        mq.sendMQ(self,  queue ,  message)

class mqControl(mq):
    def __init__(self):
        self.lastMessage = ""
        self.lastQueue = ""

    def __call__(self):
        self.__init__()
            
    def sendMQ(self, message):
        queue = 'control-to-tank'
        
        self.lastMessage = message
        self.lastQueue = queue
        
        mq.sendMQ(self, queue ,  message)

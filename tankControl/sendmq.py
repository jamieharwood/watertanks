#!/usr/bin/env python

import sys,  getopt
import json
from mqClass import mq



def main(argv):
    hose = 0
    irrigation = 0
    pump = 0
    
    try:
        opts, args = getopt.getopt(argv,  "h:i:p:",["hose=","irrigation=", "pump="])
    except getopt.GetoptError:
        print('sendmq -h <0> -i <0> -p <0>')
        sys.exit()
    
    for opt,  arg in opts:
        if opt == '-h':
            hose = arg
        elif opt == '-i':
            irrigation = arg
        elif opt == '-p':
            pump = arg
    
    messagePump = {'hose': 0, 'irrigation': 0,  'pump': 0}
    messagePump['hose'] = int(hose)
    messagePump['irrigation'] = int(irrigation)
    messagePump['pump'] = int(pump)
    
    myMQ = mq('192.168.86.240')
    print(json.dumps(messagePump))
    myMQ.send('tankpump-send',  json.dumps(messagePump))
main(sys.argv[1::])

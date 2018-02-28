#!/usr/bin/env python

import psycopg2
from pumpClass import pump
import time

def main():
    myPump = pump()
    
    dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
    dbconn.autocommit = True
    dbCur = dbconn.cursor()
    
    while True:
        sql = "select hosestate, irrigationstate from pumpControl order by datestamp desc limit 1"
        
        dbCur.execute(sql)
        rows = dbCur.fetchall()
            
        if len(rows) > 0:
            for row in rows:
                myPump.setHoseOn(row[0])
                myPump.setIrrigationOn(row[1])
        
        time.sleep(10)
    
    
main()




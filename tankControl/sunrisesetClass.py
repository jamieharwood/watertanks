#!/usr/bin/env python

import psycopg2
import json
import datetime

class sunRiseSet:
    sunrise = datetime.time()
    numSunriseSeconds = 0
    
    sunset = datetime.time()
    numSunsetSeconds = 0
    
    def __init__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.43', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
        
        self.getSunriseset()

    def __call__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.43', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
        
    def getSunriseset(self):
        sql = "select id, datestamp, sunrise, sunset from sunrisesetnow where datestamp = (select max(datestamp) from sunrisesetnow);"
        
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        if len(rows) > 0:
            for row in rows:
                self.sunrise = row[2]
                self.numSunriseSeconds = (self.sunrise.hour * 3600) + (self.sunrise.minute * 60) + self.sunrise.second
                
                self.sunset = row[3]
                self.numSunsetSeconds = (self.sunset.hour * 3600) + (self.sunset.minute * 60) + self.sunset.second
                
        else:
            sql = "insert into settings (key, value) values('"+self.settingkey+"', '"+json.dumps(self.settings)+"')"
            self.dbCur.execute(sql)
            
            self.getSettings()

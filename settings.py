#!/usr/bin/env python

import psycopg2
import json

class settingsClass:
    settingkey = "settings"
    settings = {'pumpduration': 5, 'pwmLow':23, 'pwmMid':36, 'pwmHigh':48,  'pwmFrequency':250,  'pwmPin':17}
    
    def __init__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
       #self.resetSettings()
        self.getSettings()

    def __call__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
        
    def getSettings(self):
        sql = "select key, value from settings where key = '"+self.settingkey+"'"
        
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        if len(rows) > 0:
            for row in rows:
                self.settings= json.loads(row[1])
                
        else:
            sql = "insert into settings (key, value) values('"+self.settingkey+"', '"+json.dumps(self.settings)+"')"
            self.dbCur.execute(sql)
            
            self.getSettings()

    def resetSettings(self):
        sql = "delete from settings"
        self.dbCur.execute(sql)
        
        sql = "insert into settings (key, value) values('"+self.settingkey+"', '"+json.dumps(self.settings)+"')"
        self.dbCur.execute(sql)
        
        self.getSettings()

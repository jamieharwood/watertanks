#!/usr/bin/env python

import psycopg2

class ledcontrol:
    dbconn = psycopg2.extensions.connection
    dbCur = psycopg2.extensions.cursor
    weatherGreen = 0.0
    weatherRed = 0.0
    sunriseGreen = 0.0
    sunriseRed = 0.0
    sunsetGreen = 0.0
    sunsetRed = 0.0
    hoseGreen = 0.0
    hoseRed = 0.0
    irrigationGreen = 0.0
    irrigationRed = 0.0

    def __init__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
        
        self.getStatus()

    def __call__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()

    def getStatus(self):
        sql = "select led, green, red from ledstatus where led = 0"
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        for row in rows:
            self.weatherGreen = row[1]
            self.weatherRed = row[2]
    
        sql = "select led, green, red from ledstatus where led = 1"
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        for row in rows:
            self.sunriseGreen = row[1]
            self.sunriseRed = row[2]
        
        sql = "select led, green, red from ledstatus where led = 2"
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        for row in rows:
            self.sunsetGreen = row[1]
            self.sunsetRed = row[2]
    
        sql = "select led, green, red from ledstatus where led = 3"
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        for row in rows:
            self.hoseGreen = row[1]
            self.hoseRed = row[2]
        
        sql = "select led, green, red from ledstatus where led = 4"
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        for row in rows:
            self.irrigationGreen = row[1]
            self.irrigationRed = row[2]
    
    def setSatus(self):
        sql = "update ledstatus set green = " + str(self.weatherGreen) + ","
        sql = sql + "red = " + str(self.weatherRed)
        sql = sql + "where led = 0"
        self.dbCur.execute(sql)
        
        sql = "update ledstatus set green = " + str(self.sunriseGreen) + ","
        
        sql = sql + "red = " + str(self.sunriseRed)
        sql = sql + "where led = 1"
        self.dbCur.execute(sql)
        
        sql = "update ledstatus set green = " + str(self.sunsetGreen) + ","
        sql = sql + "red = " + str(self.sunsetRed)
        sql = sql + "where led = 2"
        self.dbCur.execute(sql)
        
        sql = "update ledstatus set green = " + str(self.hoseGreen) + ","
        sql = sql + "red = " + str(self.hoseRed)
        sql = sql + "where led = 3"
        self.dbCur.execute(sql)
        
        sql = "update ledstatus set green = " + str(self.irrigationGreen) + ","
        sql = sql + "red = " + str(self.irrigationRed)
        sql = sql + "where led = 4"
        self.dbCur.execute(sql)
        
    def resetled(self):
        sql = "delete from ledstatus"
        self.dbCur.execute(sql)
        
        sql = "insert into ledstatus (led, red, green, description) values(0,0.0,0.0, 'Weather source OK')"
        self.dbCur.execute(sql)
        
        sql = "insert into ledstatus (led, red, green, description) values(1,0.0,0.0, 'Sunrise source OK')"
        self.dbCur.execute(sql)
        
        sql = "insert into ledstatus (led, red, green, description) values(2,0.0,0.0, 'Sunset source OK')"
        self.dbCur.execute(sql)
        
        sql = "insert into ledstatus (led, red, green, description) values(3,0.0,0.0, 'Hose source OK')"
        self.dbCur.execute(sql)
        
        sql = "insert into ledstatus (led, red, green, description) values(4,0.0,0.0, 'Irrigation source OK')"
        self.dbCur.execute(sql)

# Weather led
    def setWeatherGreen(self, greenValue):
            self.weatherGreen = greenValue
            self.setSatus()
            
    def getWeatherGreen(self):
            return self.weatherGreen
    
    def setWeatherRed(self, redValue):
            self.weatherRed = redValue
            self.setSatus()
            
    def getWeatherRed(self):
            return self.weatherRed
    
# Sunrise led
    def setSunriseGreen(self, greenValue):
            self.sunriseGreen = greenValue
            self.setSatus()
            
    def getSunriseGreen(self):
            return self.sunriseGreen
    
    def setSunriseRed(self, redValue):
            self.sunriseRed = redValue
            self.setSatus()
            
    def getSunriseRed(self):
            return self.sunriseRed

# Sunset led
    def setSunsetGreen(self, greenValue):
            self.sunsetGreen = greenValue
            self.setSatus()
            
    def getSunsetGreen(self):
            return self.sunsetGreen
    
    def setSunsetRed(self, redValue):
            self.sunsetRed = redValue
            self.setSatus()
            
    def getSunsetRed(self):
            return self.sunsetRed

# Hose led
    def setHoseGreen(self, greenValue):
            self.hoseGreen = greenValue
            self.setSatus()
            
    def getHoseGreen(self):
            return self.hoseGreen
    
    def setHoseRed(self, redValue):
            self.hoseRed = redValue
            self.setSatus()
            
    def getHoseRed(self):
            return self.hoseRed
            
# Irrigation led
    def setIrrigationGreen(self, greenValue):
            self.irrigationGreen = greenValue
            self.setSatus()
            
    def getIrrigationGreen(self):
            return self.irrigationGreen
    
    def setIrrigationRed(self, redValue):
            self.irrigationRed = redValue
            self.setSatus()
            
    def getIrrigationRed(self):
            return self.irrigationRed

#!/usr/bin/env python

import psycopg2
import datetime

class weather():
    datestamp = datetime.datetime.now()
    weather = ""
    temp_c = 0
    wind_dir = ""
    wind_mph = 0
    wind_gust_mph = 0
    windchill_c = 0
    feelslike_c = 0
    visibility_mi = 0
    trend = ""
    
    def __init__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
        
        self.getWeather()
        self.getRecentTrend()

    def __call__(self):
        self.dbconn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        self.dbconn.autocommit = True
        self.dbCur = self.dbconn.cursor()
    
    def getWeather(self):
        sql = "SELECT * FROM weather where datestamp = (select max(datestamp) from weather);"
        
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        if len(rows) > 0:
            for row in rows:
                self.datestamp = row[1]
                self.weather = row[2]
                self.temp_c = row[3]
                self.wind_dir = row[4]
                self.wind_mph = row[5]
                self.wind_gust_mph = row[6]
                self.windchill_c = row[7]
                self.feelslike_c = row[8]
                self.visibility_mi = row[9]
    
    def getRecentTrend(self):
        
        sql = "select weather, count(weather) as hits from (select weather as hits from public.weather order by datestamp desc limit 24) as weather group by weather.* order by hits desc"
        
        self.dbCur.execute(sql)
        rows = self.dbCur.fetchall()
        
        if len(rows) > 0:
            for row in rows:
                self.trend = row[0]
                break
    
    def isTrend(self,  trend):
        if (self.trend == "(" + trend + ")"):
            return True
        else:
            return False






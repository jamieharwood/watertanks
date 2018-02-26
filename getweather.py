#!/usr/bin/env python

import requests
import psycopg2
from ledcontrol import ledcontrolClass 

def main():
    myled = ledcontrolClass()
    
    resp = requests.get('http://api.wunderground.com/api/29c8c14c8a1fabe6/conditions/q/CA/whitstable.json')

    if resp.status_code != 200:

        	# This means something went wrong.
	        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    else:
        myled.setWeatherGreen(0.5)
        myled.setWeatherRed(0.5)
        retrieved = resp.json()

        conn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        conn.autocommit = True
        cur = conn.cursor()


        sql = "INSERT INTO public.weather (weather, temp_c, wind_dir, wind_mph, wind_gust_mph, windchill_c, feelslike_c, visibility_mi) VALUES ("
        sql = sql + "'" + retrieved['current_observation']['weather'] + "', "
        sql = sql + str(retrieved['current_observation']['temp_c']) + ", "
        sql = sql + "'" + retrieved['current_observation']['wind_dir'] + "', "
        sql = sql + str(retrieved['current_observation']['wind_mph']) + ", "
        sql = sql + str(retrieved['current_observation']['wind_gust_mph']) + ", "
        sql = sql + str(retrieved['current_observation']['windchill_c']) + ", "
        sql = sql + str(retrieved['current_observation']['feelslike_c']) + ", "
        
        if (str(retrieved['current_observation']['visibility_mi']) == "N/A"):
            sql = sql + "-1"
        else:
            sql = sql + str(retrieved['current_observation']['visibility_mi'])
        
        sql = sql + ")"

        cur.execute(sql)
        myled.setWeatherRed(0.0)
main()

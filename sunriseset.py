#!/usr/bin/env python

import requests
import psycopg2
from ledcontrol import ledcontrolClass

def main():
    myled = ledcontrolClass()
    
    resp = requests.get('https://api.sunrise-sunset.org/json?lat=51.343056&lng=1.013754&date=today')

    if resp.status_code != 200:
        # This means something went wrong.
        myled.setSunriseGreen(0.0)
        myled.setSunsetGreen(0.0)
        myled.setSunriseRed(0.0)
        myled.setSunsetRed(0.0)

        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    else:
        myled.setSunriseGreen(0.5)
        myled.setSunsetGreen(0.5)
        myled.setSunriseRed(0.5)
        myled.setSunsetRed(0.0)
        
        retrieved = resp.json()
        conn = psycopg2.connect(host='192.168.86.23', dbname='tankstore', user='tank', password='skinner2')
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("INSERT INTO public.sunrisesetnow (sunrise, sunset) VALUES ('" + retrieved['results']['sunrise'] + "', '" + retrieved['results']['sunset'] + "')")

main()

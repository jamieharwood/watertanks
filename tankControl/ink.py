#!/usr/bin/env python

from settings import settingsClass
from sunrisesetClass import sunRiseSet
from weatherClass import weather
import datetime

from PIL import ImageFont
import inkyphat

fontSize = 12
textLineOffset = 0.2
# Load the built-in FredokaOne font
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, fontSize)
    
def printTitle(caption):
    nowTime = datetime.datetime.now()
    inkyphat.text((0, fontSize * 0), caption + ' @' + nowTime.isoformat()[0:19], inkyphat.RED, font=font)
    inkyphat.line((0, fontSize,  inkyphat.WIDTH, fontSize),  inkyphat.BLACK, 1)

def printFooter():
    nowTime = datetime.datetime.now()
    
    inkyphat.text((0, inkyphat.HEIGHT - fontSize), "@", inkyphat.BLACK, font=font)
    inkyphat.text((15, inkyphat.HEIGHT - fontSize), nowTime.isoformat()[0:19], inkyphat.RED, font=font)

def printText(row,  caption,  value, postValueCaption):
    inkyphat.text((0, fontSize * (row + textLineOffset)), caption, inkyphat.BLACK, font=font)
    inkyphat.text((65, fontSize * (row + textLineOffset)), str(value) + " " + postValueCaption, inkyphat.RED, font=font)

def main():
    mySettings = settingsClass() # get settings from db
    
    mySunrise = sunRiseSet() # Get sunrise and sunset from DB
    mySunrise.getSunriseset();
    
    myWeather  = weather()
    myWeather.getWeather()
    
    #inkyphat.set_border(inkyphat.WHITE)
    if (myWeather.wind_dir in ('South')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_s.png")
    elif (myWeather.wind_dir in ('SW', 'SSW')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_sw.png")
    elif (myWeather.wind_dir in ('SE', 'SSE')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_se.png")
    elif (myWeather.wind_dir in ('North', 'NNW',  'NNE')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_n.png")
    elif (myWeather.wind_dir in ('West', 'WSW',  'WNW')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_w.png")
    elif (myWeather.wind_dir in ('East', 'ESE',  'ENE')):
        inkyphat.set_image("/home/pi/pythonCode/resources/compass_e.png")
    else: #if (myWeather.wind_dir in ('S', 'SE',  'SW',  'NE',  'N', 'NW', 'W',  'S')):
        imgFile = "/home/pi/pythonCode/resources/compass_{0}.png".replace('{0}',  myWeather.wind_dir.lower())
        inkyphat.set_image(imgFile)
        
    printTitle("Tank")
    printText(1, "Sunrise:",  mySunrise.sunrise.isoformat()[0:8], '')
    printText(2, "Sunset:", mySunrise.sunset.isoformat()[0:8],  '')
    printText(3, "Water:", mySettings.settings["pumpduration"],  'min')
    temp_c = str(myWeather.temp_c)
    windchill_c = str(myWeather.windchill_c)
    printText(4, "Temp:", temp_c + 'c w/c ' +  windchill_c , 'c')
    printText(5, "Weather:", myWeather.weather, '')
    wind_mph = str(myWeather.wind_mph)
    wind_gust_mph = str(myWeather.wind_gust_mph)
    printText(6, "Wind:", myWeather.wind_dir + " spd: " + wind_mph + 'g: ' + wind_gust_mph, '')
    
    inkyphat.show() # And show it!
main()


#!/usr/bin/env python

from sunrisesetClass import sunRiseSet
from weatherClass import weather

from PIL import ImageFont

import inkyphat

def main():
    fontSize = 16
    mySunrise = sunRiseSet() # Get sunrise and sunset from DB
    mySunrise.getSunriseset();
    
    myWeather  = weather()
    myWeather.getWeather()
    
    # Load the built-in FredokaOne font
    font = ImageFont.truetype(inkyphat.fonts.FredokaOne, fontSize)

    inkyphat.set_border(inkyphat.BLACK)
    
    inkyphat.text((0, fontSize * 0), "Tank", inkyphat.BLACK, font=font)
    inkyphat.text((0, fontSize * 1), "Sunrise: " + mySunrise.sunrise.isoformat(), inkyphat.BLACK, font=font)
    inkyphat.text((0, fontSize * 2), "Sunset: " + mySunrise.sunset.isoformat(), inkyphat.BLACK, font=font)
    inkyphat.text((0, fontSize * 3), "Weather: " + myWeather.weather, inkyphat.BLACK, font=font)
    
    # And show it!
    inkyphat.show()
main()

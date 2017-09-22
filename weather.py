#!/usr/bin/env python

import unicornhat as uh
import time

### START CONFIG ###

# Colors used by the app (r,g,b)
NO_COLOR=(55,55,55)
CLEAR_COLOR=(255,191,0)
RAIN_COLOR=(0,72,186)
SNOW_COLOR=(0,255,255)
WIND_COLOR=(255,0,255)
FOG_COLOR=(0,127,0)
CLOUDY_COLOR=(240,248,255)
PARTLY_CLOUDY_COLOR=(90,94,97)

# Names used by darksky.net https://darksky.net/dev/docs#data-point-object
ICON_NAMES=['clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind', 'fog', 'cloudy', 'partly-cloudy-day', 'partly-cloudy-night']
ICON_COLORS=[CLEAR_COLOR,NO_COLOR,RAIN_COLOR,SNOW_COLOR,SNOW_COLOR,WIND_COLOR,FOG_COLOR,CLOUDY_COLOR,PARTLY_CLOUDY_COLOR,PARTLY_CLOUDY_COLOR]
ICON_UNKNOWN_COLOR=(127,0,0)

### END CONFIG ###


# Setup unicorn phat
uh.set_layout(uh.PHAT)
uh.rotation(0)
uh.brightness(0.6)

# Helpers to set pixel colors
def set_color(x,y,color):
  uh.set_pixel(x,y,color[0],color[1],color[2])

def get_condition_color(text):
  if text is "sunny":
    return SUNNY_COLOR
  elif text is "rainy":
    return RAINY_COLOR
  elif text is "cloudy":
    return CLOUDY_COLOR



#while True:

set_color(0,3,ICON_COLORS[0])
set_color(1,3,ICON_COLORS[0])
set_color(2,3,ICON_COLORS[2])
set_color(3,3,ICON_COLORS[3])
set_color(4,3,ICON_COLORS[5])
set_color(5,3,ICON_COLORS[6])
set_color(6,3,ICON_COLORS[7])
set_color(7,3,ICON_COLORS[8])

uh.show()
time.sleep(1.5)


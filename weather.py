#!/usr/bin/env python

import unicornhat as uh
import time
from darksky import forecast

### START CONFIG ###

# Colors used by the app (r,g,b)
NO_COLOR = (55,55,55)
CLEAR_COLOR = (255,191,0)
RAIN_COLOR = (0,72,186)
SNOW_COLOR = (0,255,255)
WIND_COLOR = (255,0,255)
FOG_COLOR = (0,127,0)
CLOUDY_COLOR = (240,248,255)
PARTLY_CLOUDY_COLOR = (90,94,97)

# Names used by darksky.net https://darksky.net/dev/docs#data-point-object
ICON_NAMES = ['clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind',
                'fog', 'cloudy', 'partly-cloudy-day', 'partly-cloudy-night']
ICON_COLORS = [CLEAR_COLOR, NO_COLOR, RAIN_COLOR, SNOW_COLOR, SNOW_COLOR,
                WIND_COLOR, FOG_COLOR, CLOUDY_COLOR, PARTLY_CLOUDY_COLOR,
                PARTLY_CLOUDY_COLOR]
ICON_UNKNOWN_COLOR = (127,0,0)

# Dark Sky API key
DARKSKY_KEY = 'API_KEY'

# Dark Sky coordinates for weather forecast; from URL of forecast
DARKSKY_LOC = [38.895,-77.0366]

# Update frequency in seconds
UPDATE_SPEED = 300

# Settings for pulses
PULSE_MULTIPLIER = 5
PULSE_STEPS = 20 * PULSE_MULTIPLIER

# Time in sec between refreshes, effects pulse cycle time
TIME_STEP = 0.075

# Base temp in degree F to show temps as green => comfortable
BASE_TEMP=70

### END CONFIG ###

### START CONSTANTS ###

# Column numbers
COL_ICON = 3
COL_TEMP = 2
COL_PRECIP = 1
COL_WIND = 0

### END CONSTANTS ###

### START GLOBALS ###
PRECIP_VALS = [0,0,0,0,0,0,0,0]
WIND_VALS = [0,0,0,0,0,0,0,0]

# Counter for animations
TICK = 0

# Last update
UPDATE_LAST = 0

### END GLOBALS ###

# Setup unicorn phat
uh.set_layout(uh.PHAT)
uh.rotation(0)
uh.brightness(0.5)

# Helpers to set pixel colors
def set_color(x, y, color):
    r = int(max(0, min(255, color[0])))
    g = int(max(0, min(255, color[1])))
    b = int(max(0, min(255, color[2])))
    uh.set_pixel(x, y, r, g, b)

def colorFade(x, y, colorFrom, colorTo, steps=10, step=0):
    step_R = (colorTo[0] - colorFrom[0]) / steps
    step_G = (colorTo[1] - colorFrom[1]) / steps
    step_B = (colorTo[2] - colorFrom[2]) / steps
    r = int(colorFrom[0]) + step_R*(step+1)
    g = int(colorFrom[1]) + step_G*(step+1)
    b = int(colorFrom[2]) + step_B*(step+1)
    set_color(x,y,[r,g,b])

# Helpers for updating weather data
def set_icon(x, icon):
    color = ICON_UNKNOWN_COLOR
    idx = 0
    for name in ICON_NAMES:
        if name == icon:
            color = ICON_COLORS[idx]
            break
        idx+=1
    set_color(x,COL_ICON,color)

def set_temp(x, temp):
    return

def set_precip(x, precip):
    PRECIP_VALS[x] = int(precip * 100)

def set_wind(x, wind):
    WIND_VALS[x] = int(wind)

def update_weather():
    global UPDATE_LAST
    if UPDATE_LAST == 0 or UPDATE_SPEED + UPDATE_LAST < time.time():
        weather = forecast(DARKSKY_KEY, DARKSKY_LOC[0], DARKSKY_LOC[1])

        for i in range(8):
            icon = weather.hourly[i]['icon']
            temp = weather.hourly[i]['apparentTemperature']
            precip = weather.hourly[i]['precipProbability']
            wind = weather.hourly[i]['windSpeed']
            set_icon(i, icon)
            #set_temp(i, temp)
            set_precip(i, precip)
            set_wind(i, wind)

        UPDATE_LAST=time.time()

# Helpers for updating pulses
def get_pulse_duration_wind(val):
    if val >= 35:
        return 20 * PULSE_MULTIPLIER
    elif val < 35 and val >= 25:
        return 16 * PULSE_MULTIPLIER
    elif val < 25 and val >= 19:
        return 12 * PULSE_MULTIPLIER
    elif val < 19 and val >= 13:
        return 8 * PULSE_MULTIPLIER
    elif val < 13 and val >= 8:
        return 4 * PULSE_MULTIPLIER
    elif val < 8 and val >= 5:
        return 2 * PULSE_MULTIPLIER
    elif val < 5 and val > 3:
        return 1
    else:
        return -1

def get_pulse_duration_precip(val):
    if val >= 100:
        return 20 * PULSE_MULTIPLIER
    elif val < 100 and val >= 90:
        return 18 * PULSE_MULTIPLIER
    elif val < 90 and val >= 80:
        return 16 * PULSE_MULTIPLIER
    elif val < 80 and val >= 70:
        return 14 * PULSE_MULTIPLIER
    elif val < 70 and val >= 60:
        return 12 * PULSE_MULTIPLIER
    elif val < 60 and val >= 50:
        return 10 * PULSE_MULTIPLIER
    elif val < 50 and val >= 40:
        return 8 * PULSE_MULTIPLIER
    elif val < 40 and val >= 30:
        return 6 * PULSE_MULTIPLIER
    elif val < 30 and val >= 20:
        return 4 * PULSE_MULTIPLIER
    elif val < 20 and val >= 10:
        return 2 * PULSE_MULTIPLIER
    elif val < 10 and val >= 5:
        return PULSE_MULTIPLIER
    elif val < 5 and val > 3:
        return 1
    else:
        return -1

def set_pulse(x, y, duration, color):
    if duration == -1:
        # Always off
        set_color(x, y, NO_COLOR)

    offset = int((PULSE_STEPS - duration) / 2)
    if duration > 0 and TICK % PULSE_STEPS >= offset \
        and TICK % PULSE_STEPS < PULSE_STEPS - offset:
        # Activate
        colorFade(x, y, NO_COLOR, color, step=9)
    elif duration > 0:
        # Deactivate
        colorFade(x, y, NO_COLOR, color, step=1)

def update_pulse():
    for x in range(len(PRECIP_VALS)):
        duration = get_pulse_duration_precip(PRECIP_VALS[x])
        set_pulse(x, COL_PRECIP, duration, RAIN_COLOR)
    for x in range(len(WIND_VALS)):
        duration = get_pulse_duration_wind(WIND_VALS[x])
        set_pulse(x, COL_WIND, duration, WIND_COLOR)

# Main code
def main():
    while True:
        global TICK
        update_pulse()
        uh.show()
        TICK += 1
        time.sleep(TIME_STEP)
        update_weather()

# Init
if __name__ == "__main__":
    main()
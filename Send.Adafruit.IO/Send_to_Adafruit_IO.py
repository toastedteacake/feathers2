# Send data to Adafruit IO dashboard

import time

# The secrets.py file holds API keys etc. The location varies. On Laptop is stored at /Users/miles/Desktop
# Python path env variable to this path needs to be set using the sys library
# If secrets.py is in local directory then this is not needed

import sys
sys.path.insert(0, '/Users/miles/Desktop')

# Now import secrets
from secrets import secrets

# Note the Adafruit_IO library needs to added. To check if it has been installed, in console, run : pip3 list
# It will show up as 'adafruit-io'. note the name of the library is different !
# To show what the library gives, in python, run:
#   >>> import Adafruit_IO
#   >>> dir(Adafruit_IO)

from Adafruit_IO import Client, Feed, RequestError

# Send data

def sendtoaio(button, slider):
    
    try:
        aio = Client(secrets["ADAFRUIT_IO_USERNAME"],secrets["ADAFRUIT_IO_KEY"])

        aio.send('milesbutton', button)
        aio.send('welcome-feed', slider)
        print("data sent to dashboard")

    except:
        print("Something went wrong with send to AdafruitIO")

# Get data

def getfromaio(button, slider):
    aio = Client(secrets["ADAFRUIT_IO_USERNAME"],secrets["ADAFRUIT_IO_KEY"])
    button_in = aio.receive('milesbutton')
    slider_in = aio.receive('welcome-feed')
    button = button_in.value
    slider = slider_in.value
    return button, slider


# MAIN

button_value = 0
slider = 50
button = False


sendtoaio(button_value, slider)


while True:
    button_value, slider = getfromaio(button_value, slider)
    button = (int(button_value) == 1)
    print("Received: got button", button_value, button, "got slider", slider)
    time.sleep(0.1)

print("end of run")

# Send data to Adafruit IO dashboard

# The secrets.py file holds API keys etc. The location varies
# On Laptop is stored at /Users/miles/Desktop
# Python path env variable to this path needs to be set using the sys library
# If secrets.py is in local directory then this is not needed
import sys
sys.path.insert(0, '/Users/miles/Desktop')

# Now import secrets
from secrets import secrets

# the Adafruit_IO library needs to added 
# check if it has been installed by running 
#   pip3 list
# It will show up as 'adafruit-io'
# note the name of the library is different !
# To show what the library gives
#   >>> import Adafruit_IO
#   >>> dir(Adafruit_IO)

from Adafruit_IO import Client, Feed, RequestError

# Send data

try:
    aio = Client(secrets["ADAFRUIT_IO_USERNAME"],secrets["ADAFRUIT_IO_KEY"])

    aio.send('milesbutton', 0)
    aio.send('welcome-feed', 22)
    print("data sent to dashboard")

except:
    print("Something else went wrong")
    
print("end of run")

#import requests
#
#TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
#JSON_URL = "https://www.adafruit.com/api/quotes.php"
#
#import time
#import ipaddress
#import ssl
# required for FeatherS2
# import wifi  # required for FeatherS2
# import socketpool
#
#
#def getjson(json_url, json_field):
#    response = requests.get(json_url)
#    json_data = response.json()
#    field_data = json_data[0][json_field]
#    response.close()
#    return field_data
#
#quote = getjson(JSON_URL, 'text')
#print("quote::", quote)
#pload = {'username':'Olivia','password':'123'}
#r = requests.post('https://httpbin.org/post',data = pload)
#print(r.text)
#print("-" * 40)

# basic button stuff
# https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/basics/digital_in.py

# dashboard is at
# https://io.adafruit.com/milesj/dashboards/welcome-dashboard

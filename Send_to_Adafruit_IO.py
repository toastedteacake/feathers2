
# This is the path to secrets.py on Desktop
import sys
sys.path.insert(0, '/Users/miles/Desktop')


from secrets import secrets

import requests

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "https://www.adafruit.com/api/quotes.php"

#import time
#import ipaddress
#import ssl
# required for FeatherS2
# import wifi  # required for FeatherS2
# import socketpool

def getjson(json_url, json_field):
    response = requests.get(json_url)
    json_data = response.json()
    field_data = json_data[0][json_field]
    response.close()
    return field_data

#quote = getjson(JSON_URL, 'text')
#print("quote::", quote)

#pload = {'username':'Olivia','password':'123'}
#r = requests.post('https://httpbin.org/post',data = pload)
#print(r.text)

print("-" * 40)

#from Adafruit_IO import Client

#, Feed, Data 

from Adafruit_IO import Client, Feed, RequestError

try:
    aio = Client(secrets["ADAFRUIT_IO_USERNAME"],secrets["ADAFRUIT_IO_KEY"])

    aio.send('milesbutton', 0)
    aio.send('welcome-feed', 22)
    print("data sent to dashboard")

except:
    print("Something else went wrong")
    



#digital = aio.feeds('digital')

# basic button stuff
# https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/basics/digital_in.py

# dashboard is at
# https://io.adafruit.com/milesj/dashboards/welcome-dashboard












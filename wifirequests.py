
#Get and send data on the board using requests lib
#
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

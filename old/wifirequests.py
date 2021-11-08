#Get and send data using requests library
#
import requests


# Some sites that produce simple text to test with
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "https://www.adafruit.com/api/quotes.php"

# required for FeatherS2
# import wifi, time, ipaddress, ssl, socketpool  # required for FeatherS2




response = requests.get(JSON_URL)
json_data = response.json()

print("Example 1. using: ", JSON_URL)
print("The whole json is ::", json_data)

selected_json_field_name = 'text'

selected_field_data = json_data[0][selected_json_field_name]
    
response.close()

print("The selected field is ::", selected_field_data)

print("-" * 40)




# Example 2
print("Example 2. Using an API key in local secrets.py - \n Get weather in Manchester from Openweathermap.org")



# Get the API_Key from secrets.py (on local Desktop)
# add path to the file using sys library
import sys
sys.path.insert(0, '/Users/miles/Desktop')

# Now import secrets
from secrets import secrets

API_key = secrets["openweathermap_API_KEY"]
URL="https://api.openweathermap.org/data/2.5/weather?id="+ API_key


response = requests.get(URL)
json_data = response.json()

# Select out some fields
description_of_weather = json_data['weather'][0]['description']
current_temp = round((json_data['main']['temp'] - 273.15) , 1)
current_humidity = json_data['main']['humidity']
    
output = "Manchester weather = " + description_of_weather + ", " + str(current_temp) + " degrees C, "+ str(current_humidity)+  "% humidity"

print(output)


#pload = {'username':'Olivia','password':'123'}
#r = requests.post('https://httpbin.org/post',data = pload)
#print(r.text)




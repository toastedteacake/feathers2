#Google spreadsheets access with Python using gspread library 
#
#Uses gspread library.
#See: https://docs.gspread.org/en/latest/api.html
#
#First get google oauth() authentication.
#See - https://docs.gspread.org/en/latest/oauth2.html
#creates credentials.json and authorized_user.json
#
#Be careful about path to the .json files, these need to be in the python path:
#credentials.json and authorized_user.json
#
#The adafruit guide is here
#https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/connecting-to-googles-docs-python3
#Note on Feather the following libraries will also be required
# import sys, time, datetime,
# import board, adafruit_dht
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials




import gspread

# Name of the spreadsheet in google drive


# Open the SHEET_NAME using oauth
# either have credentials.json and authorized_user.json in the local path
authorizeopen = gspread.oauth()

# or set the search path using:
# authorizeopen = gspread.oauth(credentials_filename='path/to/the/credentials.json', authorized_user_filename='path/to/the/authorized_user.json')

# Name of sheet in google sheets to open
SHEET_NAME = "sensor.data"

myspreadsheet = authorizeopen.open(SHEET_NAME).sheet1

# Testing
print("test get a value")

getA1value = myspreadsheet.get('A1')

print("A1 value is: ", getA1value)

#To add some data
print("testing put values")

import datetime
a = 33
b = 44

putvalues=[(datetime.datetime.now().isoformat()),a,b]

myspreadsheet.append_row(putvalues)



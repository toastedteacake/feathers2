#####################################################
# Micropython code for Unexpected Maker / Adafruit
# "FeatherS2" = ESP32-S2 maker board
#
# Miles. Nov 2021
#
#####################################################

import time, gc, os
import board
import busio

# Bootdiagnostics
exec(open("boot.diagnostic.py").read())


####################################################
# Onboard internal LED
# import digital io to control the on board LED
#####################################################
from digitalio import DigitalInOut, Direction, Pull
onboard_LED = DigitalInOut(board.LED)
onboard_LED.direction = Direction.OUTPUT
onboard_LED.value = False

def LEDs(status):
    if status:
        onboard_LED.value = True
    else:
        onboard_LED.value = False
    return


#####################################################
#Adafruit_BME680_I2C multisensor
#connected via I2C
#####################################################
i2c = board.I2C()
import adafruit_bme680
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

def bme680():
    #Flash the onboard_LED on whilst uploading data to Adafruit_IO
    LEDs(True)
    print(("Temp: %0.3f C" % (sensor.temperature))
    + (" Humid: %0.1f %%" % sensor.humidity)
    + (" Gas: %d ohm" % sensor.gas)
    + (" Press: %0.3f hPa" % sensor.pressure)
    + (" Alt: %0.2f meters" % sensor.altitude))
    aio.send_data("temp2", sensor.temperature)
    LEDs(False)
    return


#####################################################
# General wifi related
#####################################################
print("Import WIFI libraries")
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
#import secrets
from secrets import secrets
print("Loaded local secrets.py file with API keys")

def connect_to_wifi():
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("ESP32-S2 WebClient Test")
    print("Connecting to %s"%secrets["ssid"])
    print("Connected to %s!"%secrets["ssid"])
    print("My IP address is", wifi.radio.ipv4_address)
    return

try:
    connect_to_wifi()

finally:
    print("Connected to internet")


#####################################################
# Adafruit IO
#####################################################
import adafruit_io
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
print("loaded : IO_HTTP, AdafruitIO_RequestError")

# AIO connection via HTTP requests
print("Setting up AIO connection")

# Initialize an Adafruit IO HTTP API object
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
aio = IO_HTTP(secrets["ADAFRUIT_IO_USERNAME"], secrets["ADAFRUIT_IO_KEY"], requests)
print("aio HTTP object initialized ", aio)


#####################################################
# MAIN LOOP
#####################################################

try:
    while True:
        bme680()
        time.sleep(10)

finally:
    print("END of LOOP")



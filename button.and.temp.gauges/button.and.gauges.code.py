import time, gc, os
import board
import busio
import analogio

# import digital io to control board LED

from digitalio import DigitalInOut, Direction, Pull

# Bootdiagnostics
exec(open("boot.diagnostic.py").read())


import adafruit_sht4x

i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))


sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

def SHT4x_temphumid():
    temperature, relative_humidity = sht.measurements
    print(("Temp: %0.3f C" % temperature) + (" Humid: %0.1f %%" % relative_humidity))

    aio.send_data("temp1", temperature)

import adafruit_bme680
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)


def bme680():
    print(("Temp: %0.3f C" % (sensor.temperature))
    + (" Humid: %0.1f %%" % sensor.humidity)
    + (" Gas: %d ohm" % sensor.gas)
    + (" Press: %0.3f hPa" % sensor.pressure)
    + (" Alt: %0.2f meters" % sensor.altitude))
    aio.send_data("temp2", sensor.temperature)


#Set internal LED to led13
led13 = DigitalInOut(board.LED)
led13.direction = Direction.OUTPUT
led13.value = False

#############################################################################################
# I2C local button related
#############################################################################################

i2c = board.I2C()

# Set button variables
button_i2c_addr = 0x6F
button_LED_addr = 0x19
brightness = 0x30
button_press_register = bytes([0x03])
EVENT = False
CLICK = False
PRESSED = False
result = bytearray(1)



######################################
# Use potentiometer to set brightness


##analogin = analogio.AnalogIn(board.A5)
bb_led = analogio.AnalogOut(board.IO17)



############## breadboard LED on DAC1 / IO17
bb_led = analogio.AnalogOut(board.IO17)

# clear button register
def clear_reg(reg_in):
    i2c.writeto(button_i2c_addr, bytes([reg_in, 0x00]))

# set LEDs on or off
def LEDs(status):
    i2c.try_lock()
    if status:
       #LEDs on
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, brightness]))
        led13.value = True
        ##potbrightness = analogin.value
        ##bb_led.value = potbrightness
        bb_led.value = 50000

    else:
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, 0x00]))
        led13.value = False
        bb_led.value = 0
    i2c.unlock()

# check for button click
def clickcheck():
    i2c.writeto_then_readfrom(button_i2c_addr, button_press_register, result)
    press_reg_string= ('00000000'+bin(int.from_bytes(result, "little"))[2:])[-8:] #result byte in binary string with leading zeros
    EVENT = (press_reg_string[7] == "1" )
    CLICK = (press_reg_string[6] == "1" )
    PRESSED = (press_reg_string[5] == "1" )
    print("result ", result, "EVENT=", EVENT, " CLICK= ", CLICK, " PRESSED= ", PRESSED)
    return CLICK

#############################################################################################
# wifi related
#############################################################################################
print("Import WIFI libraries")
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import adafruit_io
#from Adafruit_IO import Client, Feed, RequestError
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

print("loaded : IO_HTTP, AdafruitIO_RequestError")


#import secrets
print("Import secrets")
from secrets import secrets

def connect_to_wifi():
    print("ESP32-S2 WebClient Test")
    print("Connecting to %s"%secrets["ssid"])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to %s!"%secrets["ssid"])
    print("My IP address is", wifi.radio.ipv4_address)
    return

def fetch_json_test():
    print("Fetching JSON", JSON_URL)

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    response = requests.get(JSON_URL)
    print("Response status code ", response.status_code)
    get_json = response.json()
    text = get_json[0]['text']
    author = get_json[0]['author']
    print("Famous QUOTE -->'", text, "'" , " --", author)
    response.close()

def ping_test():
    ipv4 = ipaddress.ip_address("8.8.4.4")
    print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))


# Connect to internet and test with ping and json requests
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "https://www.adafruit.com/api/quotes.php"

try:
    connect_to_wifi()
    ping_test()
    #fetch_json_test()

finally:
    print("Internet Connected")

############################################################################
# AIO connection via HTTP requests
#
print("Set up AIO connection")

# Initialize an Adafruit IO HTTP API object
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
aio = IO_HTTP(secrets["ADAFRUIT_IO_USERNAME"], secrets["ADAFRUIT_IO_KEY"], requests)
print("aio HTTP object initialized ", aio)


def getAIObutton():
    AIO_return = False
    webbutton = aio.receive_data("milesbutton")
    AIO_return = (int(webbutton["value"]) == 1)
    print("Return AIO_button", AIO_return)
    return AIO_return


def sendAIObutton(sendcond):
    if sendcond:
        sendvalue = 1
    else:
        sendvalue = 0

    aio.send_data("milesbutton", sendvalue)
    print("Sent to AIO: Cond", sendcond, " value ", sendvalue)
    return

# Check AIO button state


def localbutton():
    i2c.try_lock()
    i2c.writeto_then_readfrom(button_i2c_addr, button_press_register, result)
    click = (result == bytearray(b'\x03'))
    clear_reg(0x03)
    i2c.unlock()
    return click

local_button = False

try:
    while True:


        # getAIObutton()

        local_state = getAIObutton()

        LEDs(local_state)

        print("local button", local_state)

        local_click = localbutton()

        if local_click:

            print("There has been a click", local_click)
            newstate = not local_state
            sendAIObutton(newstate)
            LEDs(newstate)



        SHT4x_temphumid()
        bme680()
        time.sleep(100)


finally:
    print("END of LOOP")







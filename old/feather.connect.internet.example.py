
# THIS NEEDS TIDYING UP

import time, gc, os
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import re


# Say hello
print("\nHello from FeatherS2!")
print("---------------------\n")
# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))
flash = os.statvfs("/")
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))


#################################################################################
#
#   I2C
#
#################################################################################
i2c = board.I2C()

# i2c.scan() -> I2C addresses found: ['0x6f']


#################################################################################
#
#   Button related
#
#################################################################################

button_i2c_addr = 0x6F
button_LED_addr = 0x19
brightness = 0x00

button_press_register = bytes([0x03])

EVENT = False
CLICK = False
PRESSED = False

result = bytearray(1)
held = 0

led13 = DigitalInOut(board.LED)
led13.direction = Direction.OUTPUT
led13.value = False


def clear_reg(reg_in):
    i2c.writeto(button_i2c_addr, bytes([reg_in, 0x00]))

clicked = True
clicked_code = bytearray(b'\x03')

def button():
    i2c.writeto_then_readfrom(button_i2c_addr, button_press_register, result)
    clicked = ( result == clicked_code )
    #print("clicked --->", clicked)
    return(clicked)

def LEDs(state) :
    if state :
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, 0x80]))
        led13.value = True
    else:
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, 0x00]))
        led13.value = False

    return

def button_check():
        # Button Loop
    LEDs(False)
    buttonclicked = button()
    if buttonclicked :
        clear_reg(0x03)
        LEDs(True)
        return(True)

##########################################################
#
#   Wifi related
#
##########################################################

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "https://www.adafruit.com/api/quotes.php"


def connect_to_wifi():
    from secrets import secrets
    print("ESP32-S2 WebClient Test")
    print("Connecting to %s"%secrets["ssid"])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to %s!"%secrets["ssid"])
    print("My IP address is", wifi.radio.ipv4_address)
    return

#############################################################
#
#   MAIN LOOP
#
############################################################


while not i2c.try_lock():
    pass

print("Press to connect to internet")
while (not button_check()):
    time.sleep(0.2)


###########################################################

try:

    connect_to_wifi()

    #ipv4 = ipaddress.ip_address("8.8.4.4")
    #print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    ################################################
    print("Press to get quote")
    while (not button_check()):
        time.sleep(0.2)
    #################################################

    print("Fetching ", JSON_URL);
    response = requests.get(JSON_URL)
    print("Response status code ", response.status_code)

    get_json = response.json()

    # extract text
    #print("get_json", get_json)

    text = get_json[0]['text']
    author = get_json[0]['author']

    print("Famous QUOTE -->")
    print("'", text, "'" , " --", author)

    response.close()

finally:
    LEDs(False)
    i2c.unlock()

print("END")




# Need write general button example #####
import time, gc, os
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests


# Say hello
print("\nHello from FeatherS2!")
print("---------------------\n")

# Turn on the internal blue LED

#feathers2.led_set(False)

led13 = DigitalInOut(board.LED)
led13.direction = Direction.OUTPUT
led13.value = False


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

i2c = board.I2C()

# i2c.scan() -> I2C addresses found: ['0x6f']

button_i2c_addr = 0x6F
button_LED_addr = 0x19
brightness = 0x00

button_press_register = bytes([0x03])

EVENT = False
CLICK = False
PRESSED = False

result = bytearray(1)
held = 0

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




while not i2c.try_lock():
    pass

try:
    while True:

        button_check()

        time.sleep(0.2)

finally:
    i2c.unlock()


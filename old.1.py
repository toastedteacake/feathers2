import time, gc, os
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import adafruit_io


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

#############################################################################################

# Simple latching button & light

#############################################################################################


i2c = board.I2C()

# i2c.scan() -> I2C addresses found: ['0x6f']

button_i2c_addr = 0x6F
button_LED_addr = 0x19
brightness = 0x30
button_press_register = bytes([0x03])
EVENT = False
CLICK = False
PRESSED = False

result = bytearray(1)


def clear_reg(reg_in):
    i2c.writeto(button_i2c_addr, bytes([reg_in, 0x00]))

def LEDs(status):
    if status:
       #LEDs on
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, brightness]))
        led13.value = True
    else:
        i2c.writeto(button_i2c_addr, bytes([button_LED_addr, 0x00]))
        led13.value = False


def clickcheck():
    i2c.writeto_then_readfrom(button_i2c_addr, button_press_register, result)
    press_reg_string= ('00000000'+bin(int.from_bytes(result, "little"))[2:])[-8:] #result byte in binary string with leading zeros
    EVENT = (press_reg_string[7] == "1" )
    CLICK = (press_reg_string[6] == "1" )
    PRESSED = (press_reg_string[5] == "1" )
    #print("result ", result, "EVENT=", EVENT, " CLICK= ", CLICK, " PRESSED= ", PRESSED, "HELD=", held, "Brightness ", brightness)
    return CLICK




while not i2c.try_lock():
    pass


latch = False
LEDs(latch)

try:
    while True:
        CLICK = clickcheck()


        if CLICK :
            clear_reg(0x03)
            latch = not latch
            LEDs(latch)

        time.sleep(0.2)

finally:
    i2c.unlock()

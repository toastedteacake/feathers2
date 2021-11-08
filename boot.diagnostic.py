# Write your code here :-)
print("UnexpectedMaker Adafruit FeatherS2. Boot Diagnostics")
print("The Board has booted")

print("Loading libraries")
import time, gc, os
import board
import busio

# import digital io library to control board LED
from digitalio import DigitalInOut, Direction, Pull

# Show available memory
print("Memory Info - gc.mem_free()", "{} Bytes".format(gc.mem_free()))
flash = os.statvfs("/")
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
print("Flash - os.statvfs('/')Size: {} Bytes\nFree: {} Bytes".format(flash_size, flash_free))

#Set internal LED to internal_led
print("Internal LED check. Should flash x5 times")
internal_led = DigitalInOut(board.LED)
internal_led.direction = Direction.OUTPUT
internal_led.value = False

#Flash internal_led
for _ in range(10):
    internal_led.value = not internal_led.value
    time.sleep(0.05)
#release the LED
internal_led.deinit()

# I2C bus check
print("I2C bus checks:")
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C bus loaded")
while not i2c.try_lock():
    print("I2C bus locked")
    pass
print("Found connected I2C devices at following addresses:")
print([hex(x) for x in i2c.scan()])
i2c.unlock()
i2c.deinit()
print("I2C unlocked")

# LDO2 check

import digitalio
ldo2 = digitalio.DigitalInOut(board.LDO2)
ldo2.direction = digitalio.Direction.OUTPUT
ldo2.value = True
time.sleep(0.25)
ldo2.value = False
ldo2.deinit()
print("LDO2 turned on, then off")



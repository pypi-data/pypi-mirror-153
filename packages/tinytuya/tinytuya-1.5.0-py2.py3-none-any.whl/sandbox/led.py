# LED Strip

import tinytuya
import time
import random

tinytuya.set_debug()

# LED Strip
DEVICEID = "ebf734c3ca19c78118cxuk"
DEVICEIP = "10.0.1.254"
DEVICEKEY = "657d0d254738ea22"
#DEVICEKEY = "657d0d254738ea21"

d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)

# Show status of device
data = d.status()
print('\nCurrent Status of Bulb: %r' % data)

# Set to full brightness warm white
print('\nWarm White Test')
d.set_white()
time.sleep(1)

# Power Control Test
print('\nPower Control Test')
print('    Turn off lamp')
d.turn_off()
time.sleep(1)
print('    Turn on lamp')
d.turn_on()
time.sleep(1)

# Random Color Test
print('\nRandom Color Test')
for x in range(10):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    print('    RGB (%d,%d,%d)' % (r, g, b))
    d.set_colour(r, g, b)
    time.sleep(1)

d.turn_off()


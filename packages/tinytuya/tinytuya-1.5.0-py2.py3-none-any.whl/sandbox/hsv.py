import tinytuya
import time
import os
import random
import colorsys

# LED
DEVICEID = "ebf734c3ca19c78118cxuk"
DEVICEIP = "10.0.1.253"
DEVICEKEY = "657d0d254738ea22"
DEVICEVERS = "3.3"
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)
d.set_socketPersistent(True)  

# SmartBulb
DEVICEID = "26056530b8f009013cc3"
DEVICEIP = "10.0.1.244"
DEVICEKEY = "cd7a80204718ac56"
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)
d.set_socketPersistent(True)  
data = d.status()

d.set_colour(255,0,0) # red
time.sleep(1)

x = 100
while x > 0:
    d.set_brightness_percentage(x)
    x = x - 5
    time.sleep(0.1)
while x <= 100:
    d.set_brightness_percentage(x)
    x = x + 5
    time.sleep(0.1)


d.set_colour(255,255,0) # cyan
time.sleep(1)

x = 100
while x > 0:
    d.set_brightness_percentage(x)
    x = x - 5
    time.sleep(0.1)
while x <= 100:
    d.set_brightness_percentage(x)
    x = x + 5
    time.sleep(0.1)

time.sleep(1)

d.set_white()
x = 100
while x > 0:
    d.set_brightness_percentage(x)
    x = x - 5
    time.sleep(0.1)

d.set_white()

# TinyTuya Example
# -*- coding: utf-8 -*-
"""
 TinyTuya - Smart Bulb RGB Test

 Author: Jason A. Cox
 For more information see https://github.com/jasonacox/tinytuya

"""
import tinytuya
import time
import os
import random

DEVICEID="eb154d944a38a229e7ijss"
DEVICEIP="10.0.1.35"
DEVICEKEY="edef4dd71a1feb7d"
DEVICEVERS="3.3"

print("TinyTuya - Smart Bulb RGB Test [%s]\n" % tinytuya.__version__)
print('TESTING: Device %s at %s with key %s version %s' %
      (DEVICEID, DEVICEIP, DEVICEKEY, DEVICEVERS))

# Connect to Tuya BulbDevice
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
print(d)
if(DEVICEVERS == '3.3'):    # IMPORTANT to always set version 
    d.set_version(3.3)
else:
    d.set_version(3.1)
# Keep socket connection open between commands
d.set_socketPersistent(True)  

# Show status of device
data = d.status()
print('\nCurrent Status of Bulb: %r' % data)

# Set to full brightness warm white
print('\nWarm White Test')
d.set_white()

# Random Color Test
d.set_mode('colour')
d.turn_on()
print('\nRandom Color Test')
for x in range(10):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    print('    RGB (%d,%d,%d)' % (r, g, b))
    d.set_colour(r, g, b)
    time.sleep(2)

# Done
print('\nDone')
d.set_white()

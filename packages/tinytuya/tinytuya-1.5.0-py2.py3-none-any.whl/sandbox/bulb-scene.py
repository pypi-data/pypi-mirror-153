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

#tinytuya.set_debug()

# Time to wait between commands
WAIT = 1

# SmartBulb
DEVICEID = "26056530b8f009013cc3"
DEVICEIP = "10.0.1.244"
DEVICEKEY = "cd7a80204718ac56"
DEVICEVERS = "3.3"

print("TinyTuya - Smart Bulb Scene Test [%s]\n" % tinytuya.__version__)
print('TESTING: Device %s at %s with key %s version %s' %
      (DEVICEID, DEVICEIP, DEVICEKEY, DEVICEVERS))

# Connect to Tuya BulbDevice
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
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
time.sleep(WAIT)

# Power Control Test
print('\nPower Control Test')
print('    Turn off lamp')
d.turn_off()
time.sleep(WAIT)
print('    Turn on lamp')
d.turn_on()
time.sleep(WAIT)

# Scene Test
print('    Scene')
d.set_mode('scene')
# Color rotation mode
d.set_value(25, '07464602000003e803e800000000464602007803e803e80000000046460200f003e803e800000000464602003d03e803e80000000046460200ae03e803e800000000464602011303e803e800000000')


time.sleep(WAIT*10)

# Done
print('\nDone')
d.set_white()

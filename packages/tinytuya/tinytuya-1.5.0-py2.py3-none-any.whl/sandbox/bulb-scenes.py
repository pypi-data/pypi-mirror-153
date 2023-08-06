# TinyTuya Example
# -*- coding: utf-8 -*-
"""
 TinyTuya - RGB SmartBulb - Scene Test for Bulbs with DPS Index 25

 Author: Jason A. Cox
 For more information see https://github.com/jasonacox/tinytuya

"""
import tinytuya
import time
import random

DEVICEID = "01234567891234567890"
DEVICEIP = "10.0.1.99"
DEVICEKEY = "0123456789abcdef"
DEVICEVERS = "3.3"

print("TinyTuya - Smart Bulb RGB Test [%s]\n" % tinytuya.__version__)
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

# Determine bulb type - if it has index 25 it uses strings to set scene
# if()

# Test Some Scenes
print('\nTesting Bulb Scenes')
d.set_mode('scene')

# Example: Color rotation mode
print('    Scene - Color Rotation Mode')
d.set_value(25, '07464602000003e803e800000000464602007803e803e80000000046460200f003e803e800000000464602003d03e803e80000000046460200ae03e803e800000000464602011303e803e800000000')
time.sleep(10)

# Example: Read scene
print('    Scene - Reading Light')
d.set_value(25, '010e0d0000000000000003e803e8')
time.sleep(5)

# Done
print('\nDone')
d.set_white()

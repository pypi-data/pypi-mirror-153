import tinytuya
import time

DEVICEID = "eb154d944a38a229e7ijss"
DEVICEIP = "0.0.0.0"
DEVICEKEY = "edef4dd71a1feb7d"
DEVICEVERS = "3.3"

# Connect to Tuya BulbDevice
print('\nConnecting to Tuya Bulb')
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)

# Show status of device
data = d.status()
print('\nCurrent Status of Bulb: %r' % data)

# Check to see if the bulb is on and get state of device
data = d.state()
print('\nStatus of Bulb: %r and the Bulb is: ' % data)
if (data['is_on']==True):
    print('ON')
else:
    print('OFF')

# Power Control Test
print('\nPower Control Test')
print('    Turn off lamp')
d.turn_off()
time.sleep(2)
print('    Turn on lamp')
d.turn_on()

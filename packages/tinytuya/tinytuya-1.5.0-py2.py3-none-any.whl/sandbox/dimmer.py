import tinytuya
import time

"""
        "name": "Chandelier",
        "id": "00712485d8f15bc9d55b",
        "key": "377d01b7c86e970c"

"""

DEVICEID = "00712485d8f15bc9d55b"
DEVICEIP = "10.0.1.36"
DEVICEKEY = "377d01b7c86e970c"
DEVICEVERS = "3.3"

tinytuya.set_debug()

# Connect to Tuya BulbDevice
print('\nDimmer Switch - Test')
d = tinytuya.OutletDevice(DEVICEID, DEVICEIP, DEVICEKEY)
print(d)
d.set_version(3.3)

# Show status of device
data = d.status()
print('\nCurrent Status of Light: %r' % data)

# Check to see if the bulb is on and get state of device
data = d.status()
dim = data['dps']['3']
print('\nStatus of light: %r' % data)
print('\nStatus of light on: %r' % data['dps']['1'])
print('\nStatus of dimmer on: %r' % data['dps']['3'])

# Power Control Test
print('\nPower Control Test')
print('    Turn off light')
d.turn_off()
time.sleep(2)
print('    Turn on light')
d.turn_on()
time.sleep(1)
print('    Dim to 10%')
d.set_value(3, 25) 
time.sleep(1)
print('    Dim to 25%')
d.set_value(3, 63) 
time.sleep(1)
print('    Dim to 50%')
d.set_value(3, 128) 
time.sleep(1)
print('    Dim back to %r',dim)
d.set_value(3, dim) 

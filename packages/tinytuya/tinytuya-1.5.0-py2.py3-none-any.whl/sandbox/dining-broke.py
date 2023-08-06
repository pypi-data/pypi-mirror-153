import tinytuya
import time

"""
        "name": "Dining Room",
        "key": "9b7eeb55d0c7819e",
        "id": "047555462cf432a18791"
"""

DEVICEID = "047555462cf432a18791"
DEVICEIP = "10.0.1.45"
#DEVICEKEY = "9b7eeb55d0c7819e"
DEVICEKEY = "9b7eeb55d0c7819f"
DEVICEVERS = "3.3"

# Connect to Tuya BulbDevice
print(tinytuya.version)

tinytuya.set_debug(True)

print('\nDining Room - Test')
d = tinytuya.OutletDevice(DEVICEID, DEVICEIP, DEVICEKEY)
print(d)
d.set_version(3.3)

# Show status of device
data = d.status()
print('\nCurrent Status of Light: %r' % data)

# Check to see if the bulb is on and get state of device
data = d.status()
print('\nStatus of light: %r' % data)

# Power Control Test
print('\nPower Control Test')
print('    Turn off light')
d.turn_off()
time.sleep(2)
print('    Turn on light')
d.turn_on()

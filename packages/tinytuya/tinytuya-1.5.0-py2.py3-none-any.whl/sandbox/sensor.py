import tinytuya
import time

"""
        "name": "Dining Room",
        "key": "9b7eeb55d0c7819e",
        "id": "047555462cf432a18791"
"""

DEVICEID = "047555462cf432a18791"
DEVICEIP = "10.0.1.45"
DEVICEKEY = "9b7eeb55d0c7819e"
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

# Generate the payload to send 
payload=d.generate_payload(tinytuya.DP_QUERY, data=None, gwId='a7e57', devId='047555462cf432a18791', uid='fab0')

# Send the payload to the device
data = d._send_receive(payload)
print('\nResponse from DP_QUERY: %r' % data)

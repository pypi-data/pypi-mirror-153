# Stand Lamp by Fireplace  Product ID = AiHXxAyyn7eAkLQY  [Valid payload]:
#    Address = 10.0.1.32,  Device ID = 177623502462ab3c5631,  Local Key = 4e55f14d495e7d2a,  Version = 3.3

DEVICEID = "177623502462ab3c5631"
DEVICEIP = "10.0.1.32"
DEVICEKEY = "4e55f14d495e7d2a"

import tinytuya
import time

print("TinyTuya (Tuya Interface) [%s]\n"%tinytuya.__version__)
tinytuya.set_debug(True)

d = tinytuya.OutletDevice(DEVICEID, DEVICEIP, DEVICEKEY)
print(d)
d.set_version(3.3)

print(" > Fetch Status < ")
data = d.status()
print(data)

print(" > Set Timer to 5s < ")
data = d.set_timer(5)
print(data)

print(" > Waiting 10s <")
time.sleep(10)

print(" > Turning back on < ")
data = d.turn_on()
print(data)

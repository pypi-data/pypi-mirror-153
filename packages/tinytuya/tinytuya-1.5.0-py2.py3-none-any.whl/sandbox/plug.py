
DEVICEID = "03200329b4e62d00cff2"
DEVICEIP = "10.0.1.27"
DEVICEKEY = "1e6b4a41e5e765ed"

import tinytuya

print("TinyTuya (Tuya Interface) [%s]\n"%tinytuya.__version__)
tinytuya.set_debug(True)

d = tinytuya.OutletDevice(DEVICEID, DEVICEIP, DEVICEKEY)
print(d)
d.set_version(3.1)

print(" > Fetch Status < ")
data = d.status()
print(data)



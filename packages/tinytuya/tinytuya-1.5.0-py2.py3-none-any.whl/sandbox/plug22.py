import tinytuya
import time

print("TinyTuya (Tuya Interface) [%s]\n"%tinytuya.__version__)
tinytuya.set_debug(True)

d = tinytuya.OutletDevice('03200329b4e62d00cff2', '10.0.1.27', '1e6b4a41e5e765ed', 'device22')
print(d)
d.set_version(3.1)

print(" > Fetch Status < ")
data = d.status()
print(data)

# device 22
import tinytuya

tinytuya.set_debug(True)   # use tinytuya.set_debug(True,False) for non-ANSI color terminal

d = tinytuya.OutletDevice(ID, IP, KEY, 'device22')
d.set_version(3.3)
d.set_dpsUsed({"1": None})  # This needs to be a datapoint available on the device
data =  d.status()
print(data)


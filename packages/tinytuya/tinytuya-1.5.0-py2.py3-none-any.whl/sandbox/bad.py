import tinytuya
import time

print("TinyTuya (Tuya Interface) [%s]\n"%tinytuya.__version__)
tinytuya.set_debug(True)

d = tinytuya.OutletDevice('03200329b4e62d00cff2', '10.0.1.99', '1e6b4a41e5e765ed')
print(d)
d.set_version(3.1)

print(" > Fetch Status < ")
data = d.status()
print(data)



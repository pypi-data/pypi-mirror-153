import tinytuya
import time

print("TinyTuya (Tuya Interface) [%s]\n"%tinytuya.__version__)

tinytuya.set_debug(True,False)

d = tinytuya.OutletDevice('eba1a5ca763ca479da7jyp', '10.0.1.225', '02bc2d7593be459b')
#d = tinytuya.OutletDevice('eba1a5ca763ca479da7jyp', None, '02bc2d7593be459b')
#d = tinytuya.OutletDevice('55004706bcddc23d1bd7', '10.0.1.49', '7bc8e49956e6c1bd')
print(d)
d.set_version(3.3)
d.set_socketPersistent(True)
d.disabledetect = True

print(" > Fetch Status < ")
data = d.status()
print(data)

print(" > Wait 5 sec < ")
time.sleep(5)

print(" > Request Update < ")
result = d.updatedps(['18','19','20'])
print(result)

print(" > Fetch Status Again < ")
data2 = d.status()
print(data2)

print("")
print("Before %r" % data)
print("After  %r" % data2)



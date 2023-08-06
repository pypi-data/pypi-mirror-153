import tinytuya
import time

DEVICEID = "047555462cf432a18791"
DEVICEIP = "10.0.1.45"
DEVICEKEY = "9b7eeb55d0c7819e"
DEVICEVERS = "3.3"


DEVICEID = "eb3b3b0d93895ea3b0x9by"
DEVICEIP = "10.0.1.59"
DEVICEKEY = "9ecd07e16b5371f8"

print('\nConnecting')
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)
d.set_socketPersistent(True)
data = d.status()

input("Press enter to turn on")
print('    Turn on light')
d.turn_on()

input("Press enter to turn off")
print('    Turn off light')
d.turn_off()

input("Press enter to turn on")
print('    Turn on light')
d.turn_on()

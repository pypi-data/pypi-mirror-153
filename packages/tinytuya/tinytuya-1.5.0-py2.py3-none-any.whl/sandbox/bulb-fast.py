import tinytuya
import time

# SmartBulb
DEVICEID = "26056530b8f009013cc3"
DEVICEIP = "10.0.1.83"
DEVICEKEY = "dc7a87be0ce203fe"
DEVICEVERS = "3.3"

#tinytuya.set_debug(True)
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
if(DEVICEVERS == '3.3'):    # IMPORTANT to always set version 
    d.set_version(3.3)
else:
    d.set_version(3.1)
# Keep socket connection open between commands
d.set_socketPersistent(True)  

# Flip through colors of rainbow - set_colour(r, g, b):
print('\nColor Test - Cycle through rainbow')
rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0],
           "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95],
           "violet": [139, 0, 255]}
for x in range(2):
    for i in rainbow:
        r = rainbow[i][0]
        g = rainbow[i][1]
        b = rainbow[i][2]
        print('    %s (%d,%d,%d)' % (i, r, g, b))
        d.set_colour(r, g, b)
        time.sleep(1)
    print('')

time.sleep(5)
d.set_white()

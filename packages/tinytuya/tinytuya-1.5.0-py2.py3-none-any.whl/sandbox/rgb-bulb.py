import tinytuya
DEVICEID = "26056530b8f009013cc3"
DEVICEIP = "10.0.1.83"
DEVICEKEY = "dc7a87be0ce203fe"
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)

d.set_socketPersistent(True)  

# Show status of device
data = d.status()
print('\nCurrent Status of Bulb: %r' % data)

# Test
# d.set_socketNODELAY(False)

# Set to full brightness warm white
print('\nWarm White Test')
d.set_white()
time.sleep(1)

# Power Control Test
print('\nPower Control Test')
print('    Turn off lamp')
d.turn_off()
time.sleep(2)
print('    Turn on lamp')
d.turn_on()
time.sleep(2)

# Dimmer Test
print('\nDimmer Control Test')
for level in range(11):
    print('    Level: %d%%' % (level*10))
    d.set_brightness_percentage(level*10)
    time.sleep(1)


# Flip through colors of rainbow - set_colour(r, g, b):
print('\nColor Test - Cycle through rainbow')
rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0],
           "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95],
           "violet": [139, 0, 255]}
for i in rainbow:
    r = rainbow[i][0]
    g = rainbow[i][1]
    b = rainbow[i][2]
    print('    %s (%d,%d,%d)' % (i, r, g, b))
    d.set_colour(r, g, b)
    time.sleep(1)
print('')

# Done
print('\nDone')
d.set_white()

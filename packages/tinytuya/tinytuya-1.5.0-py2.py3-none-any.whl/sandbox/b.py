import tinytuya
#tinytuya.set_debug()

# SmartBulb
DEVICEID = "26056530b8f009013cc3"
DEVICEIP = "10.0.1.83"
DEVICEKEY = "dc7a87be0ce203fe"

"""
SmartBulb  Product ID = keycuag84ttsx3fm  [Valid payload]:
    Address = 10.0.1.83,  Device ID = 26056530b8f009013cc3,  Local Key = dc7a87be0ce203fe,  Version = 3.3
"""
d = tinytuya.BulbDevice(DEVICEID, DEVICEIP, DEVICEKEY)
d.set_version(3.3)
d.set_socketPersistent(True)  

# Show status of device
data = d.status()
print('\nCurrent Status of Bulb: %r' % data)

# Set to full brightness warm white
print('\nWarm White Test')
d.set_white()
time.sleep(WAIT)

# Power Control Test
print('\nPower Control Test')
print('    Turn off lamp')
d.turn_off()
time.sleep(WAIT)
print('    Turn on lamp')
d.turn_on()
time.sleep(WAIT)

# Dimmer Test
print('\nDimmer Control Test')
for level in range(11):
    print('    Level: %d%%' % (level*10))
    d.set_brightness_percentage(level*10)
    time.sleep(WAIT)

# Colortemp Test
print('\nColortemp Control Test (Warm to Cool)')
for level in range(11):
    print('    Level: %d%%' % (level*10))
    d.set_colourtemp_percentage(level*10)
    time.sleep(WAIT)

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
        time.sleep(WAIT)
    print('')

# Turn off
d.turn_off()
time.sleep(WAIT)

# Random Color Test
d.turn_on()
print('\nRandom Color Test')
for x in range(10):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    print('    RGB (%d,%d,%d)' % (r, g, b))
    d.set_colour(r, g, b)
    time.sleep(WAIT)

# Test Modes
print('\nTesting Bulb Modes')
print('    White')
d.set_mode('white')
time.sleep(WAIT)
print('    Colour')
d.set_mode('colour')
time.sleep(WAIT)
print('    Scene')
d.set_mode('scene')
time.sleep(WAIT)
print('    Music')
d.set_mode('music')
time.sleep(WAIT)

# Done
print('\nDone')
d.set_white()

import tinytuya
import colorsys
import time

# Connect to Tuya Cloud - uses tinytuya.json 
c = tinytuya.Cloud()
#id = DEVICEID
id = '26056530b8f009013cc3'

# Function to set color via RGB values - Bulb type B
def set_color(rgb):
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    commands = {
        'commands': [{
            'code': 'colour_data_v2',
            'value': {
                "h": int(hsv[0] * 360),
                "s": int(hsv[1] * 1000),
                "v": int(hsv[2] * 1000)
            }
        }]
    }
    c.sendcommand(id, commands)

rainbow = {"red": (255, 0, 0), "orange": (255, 127, 0), "yellow": (255, 200, 0),
           "green": (0, 255, 0), "blue": (0, 0, 255), "indigo": (46, 43, 95),
           "violet": (139, 0, 255)}

for color in rainbow:
    print("Changing color to %s" % color)
    set_color(rainbow[color])
    time.sleep(5)

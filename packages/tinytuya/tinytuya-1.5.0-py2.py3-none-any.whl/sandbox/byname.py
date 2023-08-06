import tinytuya
import json
import time

tinytuya.set_debug(True)

with open('snapshot.json') as json_file:
     data = json.load(json_file)

# Turn on a device by name
def turn_on(name):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nTurning On: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.turn_on()

# Turn off a device by name
def turn_off(name):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nTurning Off: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.turn_off()


# Test it
turn_off('SmartBulb')
time.sleep(2)
turn_on('SmartBulb')

# TinyTuya Example
# -*- coding: utf-8 -*-
"""
 TinyTuya - Tuya Cloud Functions

 This examples uses the Tinytuya Cloud class and functions
 to access the Tuya Cloud to pull device information and
 control the device via the cloud.

 Author: Jason A. Cox
 For more information see https://github.com/jasonacox/tinytuya

""" 
import tinytuya

# Turn on Debug Mode
tinytuya.set_debug(True)

# You can have tinytuya pull the API credentials
# from the tinytuya.json file created by the wizard
# c = tinytuya.Cloud()
# Alternatively you can specify those values here:
# Connect to Tuya Cloud
c = tinytuya.Cloud(
        apiRegion="us", 
        apiKey="vhukewes9u1x8or4dp1g", 
        apiSecret="303e48ec13ec4e499006ed0d36817b31", 
        apiDeviceID="00712485d8f15bc9d55b")

# Display list of devices
devices = c.getdevices()
print("Device List: %r" % devices)

# Select a Device ID to Test
id = '03200329b4e62d00cff2'
id = '78074020600194d9ec8e' # sofa lamp
id = '177623502462ab3c5631' # lamp by fireplace

# Display Properties of Device
result = c.getproperties(id)
print("Properties of device:\n", result)

# Display Functions of Device
result = c.getfunctions(id)
print("Functions of device:\n", result)

# Display DPS IDs of Device
result = c.getdps(id)
print("DPS IDs of device:\n", result)

# Display Status of Device
result = c.getstatus(id)
print("Status of device:\n", result)

# Send Command - This example assumes a basic switch
commands = {
	'commands': [{
		'code': 'switch_1',
		'value': True
	}, {
		'code': 'countdown_1',
		'value': 0
	}]
}
print("Sending command...")
result = c.sendcommand(id,commands)
print("Results\n:", result)
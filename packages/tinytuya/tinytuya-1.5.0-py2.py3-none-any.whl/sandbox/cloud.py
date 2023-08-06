# TinyTuya Example
import tinytuya
import time

# Turn on Debug Mode
tinytuya.set_debug(True)

c = tinytuya.Cloud()

# Display list of devices
devices = c.getdevices()
print("Device List: %r" % devices)

# Select a Device ID to Test
id = '03200329b4e62d00cff2'
id = '78074020600194d9ec8e' # sofa lamp
id = '177623502462ab3c5631' # lamp by fireplace

# Display Status of Device
result = c.getstatus(id)
print("Status of device:\n", result)
time.sleep(5)

c.token = "4da9155e907808b6c2788f3b06b6e029"
result = c.getstatus(id)
print("Status of device:\n", result)


"""
while(True):
    # Display Status of Device
    result = c.getstatus(id)
    print("Status of device:\n", result)
    time.sleep(60)

"""

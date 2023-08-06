# TinyTuya Example
import tinytuya

# Turn on Debug Mode
tinytuya.set_debug(True)

c = tinytuya.Cloud(
        apiRegion="us", 
        apiKey="gmegnrdybdgr3dfylvdo", 
        apiSecret="188f4b07bde9450bb6f6c8e3b4a288f9", 
        apiDeviceID="*")

#apiDeviceID="03200329b4e62d00cff2")

# Display list of devices
devices = c.getdevices()
print("Device List: %r" % devices)


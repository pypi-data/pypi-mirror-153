# Modules
from __future__ import print_function   # python 2.7 support
from hashlib import md5
import json
import asyncio
# Required module: pycryptodome
try:
    import Crypto
    from Crypto.Cipher import AES  # PyCrypto
except ImportError:
    Crypto = AES = None
    import pyaes  # https://github.com/ricmoo/pyaes

# Globals
MAXCOUNT = 15       # How many tries before stopping
UDPPORT = 6666      # Tuya 3.1 UDP Port
UDPPORTS = 6667     # Tuya 3.3 encrypted UDP Port
TIMEOUT = 6.0       # Seconds to wait for a broadcast
DEVICEFILE = 'devices.json'
havekeys = False
tuyadevices = []

# Check to see if we have additional Device info
try:
    # Load defaults
    with open(DEVICEFILE) as f:
        tuyadevices = json.load(f)
        havekeys = True
except:
    # No Device info
    pass

if(havekeys):
    print("[%s Loaded %d devices]" % (DEVICEFILE,len(tuyadevices)))

# Crypto Functions
def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
def unpad(s): return s[:-ord(s[len(s) - 1:])]


def encrypt(msg, key): return AES.new(
    key, AES.MODE_ECB).encrypt(pad(msg).encode())
def decrypt(msg, key): return unpad(
    AES.new(key, AES.MODE_ECB).decrypt(msg)).decode()

udpkey = md5(b"yGAdlopoPVldABfn").digest()
def decrypt_udp(msg): return decrypt(msg, udpkey)

devices = {}

def appenddevice(newdevice, devices):
    if(newdevice['ip'] in devices):
        return True
    devices[newdevice['ip']] = newdevice
    return False

# Lookup Tuya device info by (id) returning (name, key)
def tuyaLookup(deviceid):
    for i in tuyadevices:
        if (i['id'] == deviceid):
            return (i['name'], i['key'])
    return ("", "")

class UDPListener:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        ip = addr[0]
        gwId = productKey = version = dname = dkey = ""
        result = data
        try:
            result = data[20:-8]
            try:
                result = decrypt_udp(result)
            except:
                result = result.decode()

            result = json.loads(result)
            print("Valid UDP Packet: %r" % result)

            note = 'Valid'
            ip = result['ip']
            gwId = result['gwId']
            productKey = result['productKey']
            version = result['version']
        except:
            print("*  Unexpected payload=%r\n" % result)
            result = {"ip": ip}
            note = "Unknown"

        # check to see if we have seen this device before and add to devices array
        if appenddevice(result, devices) == False:
            # new device found - back off count if we keep getting new devices
            if(havekeys):
                try:
                    # Try to pull name and key data
                    (dname, dkey) = tuyaLookup(gwId)
                except:
                    pass
            if(dname == ""):    
                print("Device: %s %s\n    ID = %s, Product ID = %s, Version = %s" % (
                    note, ip, gwId, productKey, version))

# UDP Scanning Server
async def scan():
    print("Starting UDP server")
    loop = asyncio.get_running_loop()
    listener = loop.create_datagram_endpoint(
        lambda: UDPListener(), 
        local_addr=("0.0.0.0", 6666)
    )
    encrypted_listener = loop.create_datagram_endpoint(
        lambda: UDPListener(), 
        local_addr=("0.0.0.0", 6667)
    )

    listeners = await asyncio.gather(listener, encrypted_listener)
    print("Listening to broadcasts on UDP port 6666 and 6667")

# User input
async def prompt():
    try:
        user = input("#")
        print('Devices = %d\n\n' % len(devices))
    except KeyboardInterrupt:
        pass
        exit()
        
# Start UDP Listeners
loop = asyncio.get_event_loop()
loop.create_task(scan())
loop.run_forever()
"""
async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        prompt(),
        scan(),
    )

asyncio.run(main())

"""

# test multiprocessing

# Modules
from __future__ import print_function   # python 2.7 support
from multiprocessing import Process, Queue
import base64
from hashlib import md5
import json
import logging
import socket
import time

# Required module: pycryptodome
try:
    import Crypto
    from Crypto.Cipher import AES  # PyCrypto
except ImportError:
    Crypto = AES = None
    import pyaes  # https://github.com/ricmoo/pyaes

# Logging

log = logging.getLogger(__name__)

# SCAN network for Tuya devices
MAXCOUNT = 15       # How many tries before stopping
UDPPORT = 6666      # Tuya 3.1 UDP Port
UDPPORTS = 6667     # Tuya 3.3 encrypted UDP Port
TIMEOUT = 3.0       # Seconds to wait for a broadcast

# Cryptography Helpers

class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.key = key

    def encrypt(self, raw, use_base64=True):
        if Crypto:
            raw = self._pad(raw)
            cipher = AES.new(self.key, mode=AES.MODE_ECB)
            crypted_text = cipher.encrypt(raw)
        else:
            _ = self._pad(raw)
            cipher = pyaes.blockfeeder.Encrypter(
                pyaes.AESModeOfOperationECB(self.key))  # no IV, auto pads to 16
            crypted_text = cipher.feed(raw)
            crypted_text += cipher.feed()  # flush final block

        if use_base64:
            return base64.b64encode(crypted_text)
        else:
            return crypted_text

    def decrypt(self, enc, use_base64=True):
        if use_base64:
            enc = base64.b64decode(enc)

        if Crypto:
            cipher = AES.new(self.key, AES.MODE_ECB)
            raw = cipher.decrypt(enc)
            return self._unpad(raw).decode('utf-8')

        else:
            cipher = pyaes.blockfeeder.Decrypter(
                pyaes.AESModeOfOperationECB(self.key))  # no IV, auto pads to 16
            plain_text = cipher.feed(enc)
            plain_text += cipher.feed()  # flush final block
            return plain_text

    def _pad(self, s):
        padnum = self.bs - len(s) % self.bs
        return s + padnum * chr(padnum).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

# Misc Helpers

def bin2hex(x, pretty=False):
    if pretty:
        space = ' '
    else:
        space = ''
    if IS_PY2:
        result = ''.join('%02X%s' % (ord(y), space) for y in x)
    else:
        result = ''.join('%02X%s' % (y, space) for y in x)
    return result

def hex2bin(x):
    if IS_PY2:
        return x.decode('hex')
    else:
        return bytes.fromhex(x)

# Utility Functions

# UDP packet payload decryption - credit to tuya-convert

def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
def unpad(s): return s[:-ord(s[len(s) - 1:])]


def encrypt(msg, key): return AES.new(
    key, AES.MODE_ECB).encrypt(pad(msg).encode())
def decrypt(msg, key): return unpad(
    AES.new(key, AES.MODE_ECB).decrypt(msg)).decode()


udpkey = md5(b"yGAdlopoPVldABfn").digest()
def decrypt_udp(msg): return decrypt(msg, udpkey)

# Return positive number or zero

def floor(x):
    if x > 0:
        return x
    else:
        return 0

def appenddevice(newdevice, devices):
    if(newdevice['ip'] in devices):
        return True
    """
    for i in devices:
        if i['ip'] == newdevice['ip']:
                return True
    """
    devices[newdevice['ip']] = newdevice
    return False

def deviceScan(q):
    """ Multi processing function that cans your network for Tuya devices and 
        returns array of device details discovered via queue.

    Parameters:
        q = multiprocessing queue

    Response (queue message format):
        [gwId, ip, version, productKey, dname, dkey, note]

    """
    DEVICEFILE = 'devices.json'
    havekeys = False
    tuyadevices = []

    # Lookup Tuya device info by (id) returning (name, key)
    def tuyaLookup(deviceid):
        for i in tuyadevices:
            if (i['id'] == deviceid):
                return (i['name'], i['key'])
        return ("", "")

    # Check to see if we have additional Device info
    try:
        # Load defaults
        with open(DEVICEFILE) as f:
            tuyadevices = json.load(f)
            havekeys = True
    except:
        # No Device info
        pass

    # Enable UDP listening broadcasting mode on UDP port 6666 - 3.1 Devices
    client = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", UDPPORT))
    client.settimeout(TIMEOUT)
    # Enable UDP listening broadcasting mode on encrypted UDP port 6667 - 3.3 Devices
    clients = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    clients.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clients.bind(("", UDPPORTS))
    clients.settimeout(TIMEOUT)

    # globals
    devices = {}
    count = 0
    counts = 0

    # forever loop
    while True:
        note = 'invalid'
        # pick up broadcast
        if (count <= counts):  # alternate between 6666 and 6667 ports
            try:
                data, addr = client.recvfrom(4048)
            except KeyboardInterrupt as err:
                log.debug('Keyboard Interrupt - Exiting')
                exit()
            except Exception as err:
                # Timeout
                count = count + 1
                continue
        else:
            try:
                data, addr = clients.recvfrom(4048)
            except KeyboardInterrupt as err:
                log.debug('Keyboard Interrupt - Exiting')

                exit()
            except Exception as err:
                # Timeout
                counts = counts + 1
                continue
        
        # process payload
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
            log.debug("Valid UDP Packet: %r" % result)

            note = 'Valid'
            ip = result['ip']
            gwId = result['gwId']
            productKey = result['productKey']
            version = result['version']
        except:
            result = {"ip": ip}
            note = "Unknown"
            log.debug("Invalid UDP Packet: %r" % result)

        # check to see if we have seen this device before and add to devices array
        if appenddevice(result, devices) == False:
            # new device found - back off count if we keep getting new devices
            if(version == '3.1'):
                count = floor(count - 1)
            else:
                counts = floor(counts - 1)
            if(havekeys):
                try:
                    # Try to pull name and key data
                    (dname, dkey) = tuyaLookup(gwId)
                except:
                    pass
            # Send details back to parent via queue
            q.put_nowait([gwId, ip, version, productKey, dname, dkey, note])

        else:
            if(version == '3.1'):
                count = count + 1
            else:
                counts = counts + 1

    # never reach here
    clients.close()
    client.close()


if __name__ == '__main__':
    count = 0
    q = Queue()
    p = Process(target=deviceScan, args=(q,))
    p.start()
    while True:
        while(q.empty() is False):
            # drain the queue
            data = q.get_nowait()
            print(" %d> %r" % (count, data))
        print(" %d> *queue empty*" % (count))
        count = count + 1
        time.sleep(1)

    p.join()

# TinyTuya Setup Wizard
# -*- coding: utf-8 -*-
"""
TinyTuya Terminal Shell for Tuya based WiFi smart devices

Author: Jason A. Cox
For more information see https://github.com/jasonacox/tinytuya

Description
    The Shell utility provides an interactive terminal to view, query and
    control Tuya based WiFi smart devices on your local network.

    HOW to set up your Tuya IoT Developer account: iot.tuya.com:
    https://github.com/jasonacox/tinytuya#get-the-tuya-device-local-key

"""
# Modules
from __future__ import print_function   # python 2.7 support
from multiprocessing import Process, Queue
import time
import json
import tinytuya
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
import collections
import sys
import base64
from hashlib import md5
import socket
import logging

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def is_windows():
    """
    True when we are using Windows.
    """
    return sys.platform.startswith("win")  # E.g. 'win32', not 'darwin' or 'linux2'

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

color = True

def addDevice(newdevice, devices):
    [gwId, ip, version, productKey, dname, dkey, note] = newdevice
    devices[ip] = {'ip': ip, 'gwId': gwId, 'version': version, 'productKey': productKey, 'name': dname, 'key': dkey}
    
"""
TinyTuya Terminal Shell for Tuya based WiFi smart devices

Parameter:
    color = True or False, print output in color [Default: True]

Description
    The Shell utility provides an interactive terminal to view, query and
    control Tuya based WiFi smart devices on your local network.

    HOW to set up your Tuya IoT Developer account: iot.tuya.com:
    https://github.com/jasonacox/tinytuya#get-the-tuya-device-local-key
"""
if __name__ == '__main__':
    # Fire up deviceScan to locate local network Tuya devices
    q = Queue()
    p = Process(target=deviceScan, args=(q,))
    p.start()

    # Local Configuration Data
    DEVICEFILE = 'devices.json'
    SNAPSHOTFILE = 'snapshot.json'
    MAXRETRY = 10
    havekeys = False
    tuyadevices = []
    devices = {}
    device_dir = {}

    # Helper Functions

    # Lookup Tuya device IP by id
    def getIP(d, gwid):
        for ip in d:
            if (gwid == d[ip]['gwId']):
                return (ip, d[ip]['version'])
        return (0, 0)

    # Lookup Tuya device info by (id) returning (name, key)
    def tuyaLookup(deviceid):
        for i in tuyadevices:
            if (i['id'] == deviceid):
                return (i['name'], i['key'])
        return ("", "")

    # Lookup device details by id or name
    def deviceLookup(name):
        # look up by IP first        
        return {'path': '~', 'id': '', 'ip': '', 'key': '', 'ver': '3.1', 'name': ''}

    # Check to see if we have additional Device info
    try:
        # Load defaults
        with open(DEVICEFILE) as f:
            tuyadevices = json.load(f)
            havekeys = True
    except:
        # No Device info
        pass
    
    if(color == False):
        # Disable Terminal Color Formatting
        bold = subbold = normal = dim = alert = alertdim = ""
    else:
        # Terminal Color Formatting
        bold = "\033[0m\033[97m\033[1m"
        subbold = "\033[0m\033[32m"
        normal = "\033[97m\033[0m"
        dim = "\033[0m\033[97m\033[2m"
        alert = "\033[0m\033[91m\033[1m"
        alertdim = "\033[0m\033[91m\033[2m"

    print(bold + 'TinyTuya Terminal Shell' + dim + ' [%s]' % (tinytuya.version) + normal)
    print('')
    if(havekeys):
        print("%s[Loaded devices.json - %d devices]\n" % (dim,len(tuyadevices)))
    else:
        print("%sWARNING:%s No devices.json found - Device keys unknown.%s\n" % (alert,alertdim,dim))

    print("%sScanning network for devices in the background ...%s\n" %
            (subbold, normal)),

    #updateDevices(devices)
    # devices = tinytuya.deviceScan(False, MAXRETRY, poll=False)
    # print("%s[Discovered %d devices]\n" % (dim,len(devices)))
        
    focus = {}
    focus['path'] = "~"
    focus['id'] = ""
    focus['ip'] = ""
    focus['key'] = ""
    focus['ver'] = "3.1"
    focus['name'] = ""

    # COMMANDS = ['help', 'ls', 'poll', 'wizard', 'exit', 'dir', 'cat']
    COMMANDS = {
        'help': None,
        'ls': None,
        'poll': None,
        'wizard': None,
        'dir': None,
        'cat': None,
        'version': None,
        'cd': device_dir,
        'select': device_dir,
        'exit': None,
    }
    completer = NestedCompleter.from_nested_dict(COMMANDS)

    commandArray = []
    for i in COMMANDS:
        commandArray.append(i)
    
    commands_string = ",".join(commandArray)
    HELP = "\n" + bold + "Commands: " + commands_string
    
    #commands_sorted = sorted(COMMANDS)
    #print(commands_sorted)
    
    # def complete(text, state):
    #     # try to auto-complete commands
    #     print("text = %s state = %r" % (text,state))
    #     response = None
    #     if state == 0:
    #             # This is the first time for this text, so build a match list.
    #             if text:
    #                 matches = [s 
    #                                 for s in commands_sorted
    #                                 if s and s.startswith(text)]
    #             else:
    #                 matches = commands_sorted[:]
    #     # Return the state'th item from the match list,
    #     # if we have that many.
    #     try:
    #         response = matches[state]
    #     except IndexError:
    #         response = None
    #     print("response = %r" % response)
    #     return response

    # readline.set_completer_delims(' \t\n;')
    # readline.parse_and_bind("tab: complete")
    # readline.set_completer(complete)

    # line = input(subbold + "Tuya" + bold + ":" + dim + path + normal + "> ")
    # user = line

    # print(HELP)
    style = Style.from_dict({
        # User input (default text).
        '':          'ansiwhite',

        # Prompt.
        'tuya':     'ansigreen',
        'colon':    'ansiwhite',
        'path':     'ansidarkgray',
        'pound':    'ansiwhite',
    })


    #
    # Main Interactive LOOP
    #
    while(True):
        # check for messages from deviceScan
        while(q.empty() is False):
            # drain the queue
            data = q.get_nowait()
            addDevice(data, devices)
            log.debug("Tuya UDP> %r" % (data))
        
        device_dir = {}
        count = 0
        for ip in devices:
            count = count + 1
            if devices[ip]['name'] == '':
                name = '"' + ip + '"'
                device_dir[name] = None
            else:
                name = '"' + devices[ip]['name'] + '"'
                device_dir[name] = None

        path = focus['path']
        # Prompt and Wait for user response
        message = [
            ('class:tuya', 'Tuya (%d Devices)' % count),
            ('class:colon',    ':'),
            ('class:path',     path),
            ('class:pound',    '> '),
        ]
        line = prompt(message, style=style, completer=completer)
        user = line.split(' ',1)[0]
        arg = ''
        if len(line.split(' ',1)) > 1:
            arg = line.split(' ',1)[1]

        # EXIT
        if user == "exit":
            print
            p.terminate()
            break

        # VERSION
        if user == "version" or user =="ver" or user =="v":
            if path == "~":
                print(bold + 'TinyTuya Terminal Shell' + dim + ' [%s]' % (tinytuya.version) + normal + '\n')
            else:
                print('%s: Version %s\n' % (focus['name'],focus['ver]']))

        # HELP
        if user == "help":
            print(HELP)   

        # CD
        if user == "select" or user == "cd":
            # Set scope for a device
            if arg == '..' or arg == '':
                path = '~'
                focus = {'path': '~', 'id': '', 'ip': '', 'key': '', 'ver': '3.1', 'name': ''}
            else:
                path = arg
                focus = deviceLookup(arg)
        
        # WIZARD
        if user == "wizard" or user == "setup":
            # Run setup wizard
            tinytuya.wizard.wizard(color)
            exit()

        # LS
        if user == "ls" or user == "dir" or user == "l":
            if focus['path'] == '~':
                # Display device list
                print("\n\n" + bold + "Device Listing:\n" + subbold)
                print("%-30s %-24s %-16s %-5s %-17s%s" % ("Name","ID", "IP","Ver","Key",dim))
                number = 0
                for ip in devices:
                    number = number + 1
                    if devices[ip]['name'] != '':
                        name = devices[ip]['name']
                        if " " in name:
                            name = '"' + name + '"'
                    else:
                        name = ip
                    if 'key' in devices[ip]:
                        key = devices[ip]['key']
                    else:
                        key = alertdim + "undefined" + dim
                    ver = devices[ip]['version']
                    id = devices[ip]['gwId']
                    print("%-30.30s %-24s %-16s %-5s %-15s" % (
                        name,id,ip,ver,key))
                
                if number == 0:
                    print ("No devices found yet.\n\n")
                if number == 1:
                    print("\n%d Device found.\n\n" % number)
                if number > 1:
                    print("\n%d Devices found.\n\n" % number)

                #output = json.dumps(tuyadevices, indent=4)  # sort_keys=True)
                #print(output)
            else:
                # Display device details
                print("\n\n" + bold + "%s Details:\n" % path + subbold)
                #lookupName(path)
                print("%-25s %-24s %-16s %-5s %-17s%s" % ("Name","ID", "IP","Version","Key",dim))
                print("{}")

        if user == "scan":
            # Find out if we should scan for devices
            answer = input(subbold + '\nScan for local devices? ' +
                        normal + '(Y/n): ')
            if(answer[0:1].lower() != 'n'):
                # Scan network for devices and provide polling data
                print(normal + "\nScanning local network for Tuya devices...")
                devices = tinytuya.deviceScan(False, MAXRETRY)
                print("    %s%s local devices discovered%s" %
                    (dim, len(devices), normal))
                print("")

        if user == "poll":
            # Find out if we should poll all devices
            if(not havekeys):
                print("%sWARNING:%s No devices.json found - Run wizard to get keys.%s\n" % (alert,alertdim,dim))

            answer = input(subbold + '\nPoll local devices? ' +
                        normal + '(Y/n): ')
            if(answer[0:1].lower() != 'n'):
                polling = []
                print("Polling %d local devices..." % len(tuyadevices))
                for i in tuyadevices:
                    item = {}
                    name = i['name']
                    (ip, ver) = getIP(devices, i['id'])
                    item['name'] = name
                    item['ip'] = ip
                    item['ver'] = ver
                    item['id'] = i['id']
                    item['key'] = i['key']
                    if (ip == 0):
                        print("    %s[%s] - %s%s - %sError: No IP found%s" %
                            (subbold, name, dim, ip, alert, normal))
                    else:
                        try:
                            d = tinytuya.OutletDevice(i['id'], ip, i['key'])
                            if ver == "3.3":
                                d.set_version(3.3)
                            data = d.status()
                            if 'dps' in data:
                                item['dps'] = data
                                state = alertdim + "Off" + dim
                                try:
                                    if '1' in data['dps'] or '20' in data['dps']:
                                        state = bold + "On" + dim
                                        print("    %s[%s] - %s%s - %s - DPS: %r" %
                                            (subbold, name, dim, ip, state, data['dps']))
                                    else:
                                        print("    %s[%s] - %s%s - DPS: %r" %
                                            (subbold, name, dim, ip, data['dps']))
                                except:
                                    print("    %s[%s] - %s%s - %sNo Response" %
                                        (subbold, name, dim, ip, alertdim))
                            else:
                                print("    %s[%s] - %s%s - %sNo Response" %
                                    (subbold, name, dim, ip, alertdim))
                        except:
                            print("    %s[%s] - %s%s - %sNo Response" %
                                (subbold, name, dim, ip, alertdim))
                    polling.append(item)
                # for loop

                # Save polling data snapsot
                current = {'timestamp' : time.time(), 'devices' : polling}
                output = json.dumps(current, indent=4) 
                print(bold + "\n>> " + normal + "Saving device snapshot data to " + SNAPSHOTFILE)
                with open(SNAPSHOTFILE, "w") as outfile:
                    outfile.write(output)
        # if poll

    # while


# if __name__ == '__main__':

#     try:
#         shell()
#     except KeyboardInterrupt:
#         pass
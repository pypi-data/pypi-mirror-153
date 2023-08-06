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
"""
import readline
import requests
import time
import hmac
import hashlib
import json
import pprint
import logging
import tinytuya
"""
#import readline
import time
import json
import tinytuya
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
import collections
import sys

# Backward compatability for python2
#try:
#    input = raw_input
#except NameError:
#    pass

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

def is_windows() -> bool:
    """
    True when we are using Windows.
    """
    return sys.platform.startswith("win")  # E.g. 'win32', not 'darwin' or 'linux2'
    
def shell(color=True):
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

    # Get Configuration Data
    DEVICEFILE = 'devices.json'
    SNAPSHOTFILE = 'snapshot.json'
    MAXRETRY = 10
    havekeys = False
    tuyadevices = []

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

    print("%sScanning network for devices ...%s" %
            (subbold, normal)),

    devices = tinytuya.deviceScan(False, MAXRETRY, poll=False)
    print("%s[Discovered %d devices]\n" % (dim,len(devices)))

    device_dir = {}
    for ip in devices:
        if 'name' in devices[ip]:
            name = '"' + devices[ip]['name'] + '"'
            device_dir[name] = None
        name = '"' + ip + '"'
        device_dir[name] = None
        
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
        path = focus['path']
        # Prompt and Wait for user response
        message = [
            ('class:tuya', 'Tuya'),
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
            break

        # VERSION
        if user == "version":
            if path == "~":
                print(bold + 'TinyTuya Terminal Shell' + dim + ' [%s]' % (tinytuya.version) + normal)
            else:
                print('%s: Version %s' % (focus['name'],focus['ver]']))

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
        if user == "ls" or user == "dir":
            if state['path'] == '~':
                # Display device list
                print("\n\n" + bold + "Device Listing:\n" + subbold)
                print("%-25s %-24s %-16s %-5s %-17s%s" % ("Name","ID", "IP","Version","Key",dim))

                for ip in devices:
                    if 'name' in devices[ip]:
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
                    print("%-25.25s %-24s %-16s %-5s %-15s" % (
                        name,id,ip,ver,key))

                print("%d Devices\n" % len(ip))
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
            # if
        # while
    return


if __name__ == '__main__':

    try:
        shell()
    except KeyboardInterrupt:
        pass
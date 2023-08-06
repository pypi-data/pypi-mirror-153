# Wizard

import json

# Terminal Color Formatting
bold="\033[0m\033[97m\033[1m"
subbold="\033[0m\033[32m"
normal="\033[97m\033[0m"
dim="\033[0m\033[97m\033[2m"
alert="\033[0m\033[91m\033[1m"
alertdim="\033[0m\033[91m\033[2m"

# backward compatability for python2
try:
    input = raw_input
except NameError:
    pass

CONFIGFILE = 'tinytuya.json'

config = {}
config['apiKey'] = ''
config['apiSecret'] = ''
config['apiRegion'] = ''
config['apiDeviceID'] = ''

needconfigs = True

try:
    # Load defaults
    with open(CONFIGFILE) as f:
        config = json.load(f)
except:
    # First Time Setup
    pass

print(bold + 'TinyTuya Setup Wizard' + dim + ' [0.0.1]' + normal)
print('')

if(config['apiKey'] != '' and config['apiSecret'] != '' and 
    config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    print("    " + alert + "Existing settings:" + dim + 
        "\n        API Key=%s \n        Secret=%s\n        Region=%s\n        DeviceID=%s" % 
        (config['apiKey'], config['apiSecret'], config['apiRegion'], 
        config['apiDeviceID']))
    print('')
    answer = input(subbold + '    Use existing credentials ' + normal + '(Y/n): ')
    if(answer[0:1].lower()=='n'):
        needconfigs = True

if(needconfigs):
    # Ask user for config settings
    print('')
    config['apiKey'] = input(subbold + "    Enter " + bold + "API Key" + subbold + 
        " from tuya.com: " + normal)
    config['apiSecret'] = input(subbold + "    Enter " + bold + "API secret" + subbold + 
        " from tuya.com: " + normal)
    # TO DO - Determine apiRegion from Device (default = us)
    config['apiRegion'] = 'us'
    config['apiDeviceID'] = input(subbold +
        "    Enter " + bold + "any Device ID" + subbold + 
        " currently registered in Tuya App (used to pull full list): " + normal)
    # Write Config
    json_object = json.dumps(config, indent = 4) 
    with open(CONFIGFILE, "w") as outfile: 
        outfile.write(json_object) 
    print(bold + "\n    Configuration Data Saved to %s" % CONFIGFILE)
    print(dim + json_object)

apiKey = config['apiKey']
apiSecret = config['apiSecret']
apiRegion = config['apiRegion'] 
apiDeviceID = config['apiDeviceID'] 

print(normal)


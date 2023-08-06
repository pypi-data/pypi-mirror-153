#!/usr/bin/env python3

import tinytuya

# d = tinytuya.OutletDevice(DEVICEID, DEVICEIP, DEVICEKEY)
tinytuya.set_debug(True)
d = tinytuya.OutletDevice('55004706bcddc23d1bd7', '10.0.1.37', '7bc8e49956e6c1bd')
d.set_version(3.3)
print(d.status())

ad = tinytuya.OutletDevice('55004706bcddc23d1bd7', None, '7bc8e49956e6c1bd')
ad.set_version(3.3)
print(ad.status())




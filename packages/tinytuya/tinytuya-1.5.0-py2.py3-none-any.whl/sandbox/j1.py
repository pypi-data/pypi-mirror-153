import sys
import time

dim=''

spinnerx = 0
spinner = "|/-\\|"
count = 0
maxretry = 10000
while count <= maxretry:
    print("%sScanning... %s\r" % (dim, spinner[spinnerx % 4]), end="")
    spinnerx = spinnerx + 1
    count = count + 1
    sys.stdout.flush()
    time.sleep(1)

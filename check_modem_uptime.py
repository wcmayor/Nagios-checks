#!/usr/bin/python

import urllib2
import sys
import re

if len(sys.argv) == 1:
    print("ERROR: No arguments received!")
    exit(3)

if len(sys.argv) != 4:
    print("ERROR: Incorrect number of arguments received!")
    exit(3)

try:
    hostip = str(sys.argv[1])
    warning = int(sys.argv[2])
    critical = int(sys.argv[3])

except:
    print("ERROR: Unable to parse arguments!")
    exit(3)

if warning < critical:
    print("ERROR: Warning value cannot be greater than critical")
    exit(3)

url = "http://" + hostip + "/indexData.htm"

try:
    modem_output = urllib2.urlopen(url).read()
except:
    print("CRITICAL: Unable to open the modem status page!")
    exit(2)

printnext = False

uptime = ''
try:
    for line in modem_output.split("\n"):
        if printnext:
            uptime = re.sub('</?T.>', '', line.strip())
        printnext = False
        if "System Up Time" in line:
            printnext = True
except:
    print("ERROR: Unable to parse modem output")
    exit(3)

if uptime == '':
    print("ERROR: Unable to find output in modem output")
    exit(3)

days = uptime[:uptime.find(' ')]
hours = uptime[uptime.find('days ') + 5:uptime.find('h:')]
minutes = uptime[uptime.find('h:') + 2:uptime.find('m:')]
seconds = uptime[uptime.find('m:') + 2:uptime.find('s', -1)]
total_minutes = int(minutes) + (int(hours) * 60) + (int(days) * 1440)

output = "Modem uptime: " + str(total_minutes) + " minutes (" + str(days) + "d, " + str(hours) + "h, " + str(minutes) + "m, " + str(seconds) + "s)|uptime=" + str(total_minutes) + ";" + str(warning) + ";" + str(critical)

status_text = "UNKNOWN: "
exit_code = 3
if total_minutes <= critical:
    status_text = "CRITICAL: "
    exit_code = 2
elif total_minutes <= warning:
    status_text = "WARNING: "
    exit_code = 1
elif total_minutes > warning:
    status_text = "OK: "
    exit_code = 0
else:
    status_text = "UNKNOWN: "
    exit_code = 3

print(status_text + output)
exit(exit_code)

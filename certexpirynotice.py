#!/usr/bin/python3.8
import os, sys
from query_cert_Exp import cert

try:
    cert()
    with open("/mnt/d/LinuxRoot/python/qualys/NRPE_status") as file: 
        status = (file.readline()).rstrip()
        if status == '0':
            print("OK. No certs pending renewal.")
            sys.exit(0)
        else:
            print("WARNING - %s certs are expiring soon. Act Now." % status)
            sys.exit(1)
except IOError:
    print("UNKOWN- Unable to perform check.")
    sys.exit(3)

#!/usr/bin/python3.8
import os, sys
#Import query_cert_Exp python function.
#If you are not using Nagios, you can simply ignore this certexpirynotice file, and just use the other python files in standalone mode. 
import query_cert_Exp as certquery

try:
    #Calling the function main() inside query_cert_Ex.py using reference ohbject.
    certquery.main()
    #The above function interacts with Qualys, performs validation on the returned data and writes two files:
    # 1. NRPE_status - A file with either "0", "1", "2" or "3". This is used by NRPE checks to map below.
    # 2. NRPE_list - Validated output from qualys. If using other monitoring systems, this file gives exact list of all certs to be renewed with their SAN domains. This file can be mofified to include other information with very little code changes. 
    # Go to query_cert_Exp.py file to continue the
    with open("/mnt/d/LinuxRoot/python/qualys/NRPE_status") as file: 
        #read the NRPE_status file and copy the value into status variable. 
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

#!/usr/bin/python3.8
from credlib import credential
import requests
from mycredentials import qualys_prod
import os, time, datetime

def system_login(*args): # this is new function definition

    if len(args) == 1 and isinstance(args[0], credential):
        hostname = args[0].hostname
        username = args[0].username
        password = args[0].password
        permissions = args[0].permissions
    elif len(args) == 3:
        hostname = args[0]
        username = args[1]
        password = args[2]
        permissions = args[3]

    else:
        raise ValueError('Invalid arguments')

    get_token(hostname, username, password, permissions) # this is original system login call

def get_token(hostname,username,password,permissions):	
    url = hostname
    payload = 'username='+username+'&password='+password+'&permissions='+permissions
    headers = {'ContentType': 'application/x-www-form-urlencoded', 'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data = payload)
    os.environ["jwt_token"] = response.text
    #print(os.environ["jwt_token"])
    WriteTxtFile = open(".secret", "w")
    WriteTxtFile.write(response.text)
    WriteTxtFile.close()


try:
    with open('.secret') as f:
        token_age_minutes = (time.time() - (os.stat('.secret').st_mtime))/60
        if (token_age_minutes < 120):
            print("Valid JTW Token available. Using it to run operations.")
            #print(f.readlines())
            #print(f.read().replace('\n', ''))
        else:
            print("Token Expired, generating new token")
            system_login(qualys_prod)
except IOError:
    print("Generating JTW Token")    
    system_login(qualys_prod)
    
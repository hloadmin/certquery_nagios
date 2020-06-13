#!/usr/bin/python3.8
# Importing credentials mapping.
from credlib import credential
# Python library for HTTPS requests. 
import requests
#mycredentials python file is where login credentials are stored as best practice. WHen used in production modify the code to read from ENV variable.
#Below, I am importing qualys_prod credentials. You can store other crendentials here and import them to use withing this function.
from mycredentials import qualys_prod
import os, time, datetime

#the function below, is called from query_cert_Exp python code to login and store Tokens for qualys. The code here, performs simply mapping of credentials. 
# note, we are using the code under if condition, as we are only passing one argument from calling section. 
# the code under elif, can be used if you want to directly pass username, password etc from code, like legacy.
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

    #call function to login to qualys and get/store token on local file system in a file called .secret. 
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
    

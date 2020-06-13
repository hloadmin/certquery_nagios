#!/usr/bin/python3.8
import requests, os, time, json

#mysystemlib python file is where login modules are written for simplicity and code reuse. 
import mysystemlib as token
#mycredentials python file is where login credentials are stored as best practice. WHen used in production modify the code to read from ENV variable.
#Below, I am importing qualys_prod credentials. You can store other crendentials here and import them to use withing this function.
from mycredentials import qualys_prod

#check main() function first and comeback to build_token. 

# this token builder function, does the following:
# 1. Check if a token is already existing in a hidden file called .secret. 
# 2. If yes, then check its age. If less than 2 hours old, provide this token to main() function to login to qualys API.
# 3. If file not found, or age more than 2 hours - Generate a new token, save it in .secret file and send this new token to login code below.
def build_token():
    bearer_token = ''
    try:
        with open('.secret') as (f):
            token_age_minutes = (time.time() - os.stat('.secret').st_mtime) / 60
            if token_age_minutes < 120:
                print('Valid token found. Using it for operations.')
                bearer_token = 'Bearer ' + f.read().replace('\n', '')
                return bearer_token
            print('Token age more than 2 hours. Generating new JTW Token')
            token.system_login(qualys_prod)
            bearer_token = 'Bearer ' + os.environ['jwt_token']
            return bearer_token
    except IOError:
        print('No token file found. Generating JTW Token')
        token.system_login(qualys_prod)
        bearer_token = 'Bearer ' + os.environ['jwt_token']
        return bearer_token

#main function of this python file. Here we are doing the following:
# 1. Login to Qualys Certview, using build_token function. This function will provide refreshed token if current token is more than 2 hours old.
# 2. Search Qualys about certificate expiry. I have used the following query, you can replace this with any valid query. Refer Qualys API section in README for more info.
# 3. Create two files as described in the certexpirynotice.py nagios plugin.
    # a. NRPE_status - Nagios status code. 
    # b. NRPE_list - List of certs to be renewed with its SAN domains. We can modify the code under "##NRPE_list builder." below to add or remove stuff from this output file.
def main():
    url = 'https://gateway.qg3.apps.qualys.com/certview/v1/certificates'
    ##filter string represents the query you use for searching in the GUI. Do not change certificateDetails, pagenumber etc. unless you are sure. For more info refer README.
    payload = '{ \n\t"filter" : \t"selfSigned:false and expiryGroup:In 100 Days and issuer.organization:\'Let\'s Encrypt\'",\n\t"certificateDetails": "basic",\n\t"pageNumber": 0, \n\t"pageSize" : 10\n}'
    jwt_token = build_token()
    headers = {'ContentType': 'application/json', 
       'Accept': 'application/json', 
       'Authorization': jwt_token, 
       'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    jsonData = json.loads(response.text)
    print("Total Let's Encrypt Expiring in next 10 days: " + str(len(jsonData)) + ' certs. Summary below, detailed list in file QueryResult \n')
    NRPE_list = []
    if len(jsonData) == 0:
        try:
            NRPEErrorTxtFile = open('NRPE_status', 'w')
            NRPEErrorTxtFile.write('0')
            NRPEErrorTxtFile.close()
        except IOError:
            print('error opening file')

    else:
        try:
            NRPEErrorTxtFile = open('NRPE_status', 'w')
            NRPEErrorTxtFile.write('1')
            NRPEErrorTxtFile.close()
        except IOError:
            print('error opening file')

        for cert in jsonData:
            san = cert['subjectAlternativeNames']
            san_dns = san['DNS Name']
            if san_dns != [] and len(san_dns) > 1:
                print(cert['dn'] + 'with ' + str(len(san_dns)) + ' SAN domains')
                ##NRPE_list builder.
                NRPE_list.append(cert['dn'])
            else:
                print(cert['dn'] + ' - Standalone Cert')
                NRPE_list.append(cert['dn'])

        print(NRPE_list)
        try:
            NRPEWriteTxtFile = open('NRPE_list', 'w')
            NRPEWriteTxtFile.write(str(NRPE_list))
            NRPEWriteTxtFile.close()
        except IOError:
            print('error opening file')


if __name__ == '__main__':
    main()
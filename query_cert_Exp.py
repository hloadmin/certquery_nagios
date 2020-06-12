#!/usr/bin/python3.8
import requests, os, time, json, mysystemlib as token
from mycredentials import qualys_prod

def build_token():
    bearer_token = ''
    try:
        with open('.secret') as (f):
            token_age_minutes = (time.time() - os.stat('.secret').st_mtime) / 60
            if token_age_minutes < 120:
                bearer_token = 'Bearer ' + f.read().replace('\n', '')
                return bearer_token
            token.system_login(qualys_prod)
            bearer_token = 'Bearer ' + os.environ['jwt_token']
            return bearer_token
    except IOError:
        print('Generating JTW Token')
        token.system_login(qualys_prod)
        bearer_token = 'Bearer ' + os.environ['jwt_token']
        return bearer_token


def cert():
    url = 'https://gateway.qg3.apps.qualys.com/certview/v1/certificates'
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
                print cert['dn'] + 'with ' + str(len(san_dns)) + ' SAN domains'
                NRPE_list.append(cert['dn'])
            else:
                print cert['dn'] + ' - Standalone Cert'
                NRPE_list.append(cert['dn'])

        print NRPE_list
        try:
            NRPEWriteTxtFile = open('NRPE_list', 'w')
            NRPEWriteTxtFile.write(str(NRPE_list))
            NRPEWriteTxtFile.close()
        except IOError:
            print( 'error opening file')


if __name__ == '__main__':
    main()
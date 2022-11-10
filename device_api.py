#!/usr/bin/python3
"""
Query device api and return status code with number of devices
First, query the latest payload from device reported on LNS
Device_UID, credential and URL stored in config.yml


"""

import json
import yaml
import requests
from requests.packages import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Reading configuration
file = 'config.yml'
data = yaml.safe_load(open(file))
data_api = data['api']

IP = data_api['IP']
DEV = data_api['DEV']
#URL: https://host[:port]/rest/nodes/{deveui}/payloads/ul/latest
#url = 'https://'+ IP +':50001/rest/nodes/'
#url = 'https://'+ IP +'/rest/nodes/70B3D5A31FFFFF95/status'# +DEV+ 'status' #'payloads/ul'
url = 'https://' + IP  + '/rest/nodes/' + DEV + '/payloads/ul/latest'

userid= data_api['userid']
password= data_api['password']
remove = ["dataFrame", "confirmed", "data_format","decrypted", "device_redundancy","dr_used","id","port","session_id"]

def dev_api():
    #resp= requests.get(url, auth =HTTPBasicAuth('device_api','Charter123'),verify=False)
    resp= requests.get(url, auth =HTTPBasicAuth(userid, password),verify=False)
    #Convert response to the list of dictionary
    info = resp.json()
    for key in remove:
        del info[key]

    #print(type(info),info)
    return(resp.status_code, info)

if __name__=='__main__':
  out = dev_api()
  print(out)

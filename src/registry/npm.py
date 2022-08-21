import os
import json
import requests
import sys
from datetime import datetime as dt

# checking against npms.io API
# deets: https://api-docs.npms.io/#api-Package-GetPackageInfo
REGISTRY_URL = "https://api.npms.io/v2/package/mget"

def get_keys(data):
    result = []
    for key in data.keys():
        if type(data[key]) != dict:
            result.append(key)
        else:
            result += get_keys(data[key])
    return result


def recv_pkg_info(pkgs, url=REGISTRY_URL):
    print("[PROC] npm checker engaged.")
    pkg_list = []
    for x in pkgs:
        pkg_list.append(x.pkg_name)
    payload =  '['+','.join(f'"{w}"' for w in pkg_list)+']' #list->payload conv
    headers = { 'Accept': 'application/json',
                'Content-Type': 'application/json'}
    print("[PROC] Connecting to registry at " + url +   "  ...")
    try:
        res = requests.post(url, data=payload, headers=headers)
        if res.status_code != 200:
            print("[ERR] Unexpected status code (" + res.status_code + ")")
            sys.exit(2)
        x = {}
        x = json.loads(res.text)
    except:
        print("[ERR] Connection error.")
        sys.exit(2)
    for i in pkgs:
        if i.pkg_name in x:
            i.exists = True
            i.score = x[i.pkg_name]['score']['final']
            timex = x[i.pkg_name]['collected']['metadata']['date']
            fmtx ='%Y-%m-%dT%H:%M:%S.%fZ'
            unixtime = int(dt.timestamp(dt.strptime(timex, fmtx))*1000)
            i.timestamp = unixtime
        else:
            i.exists = False
            

def scan_source(dir_):
    try:
        with open(os.path.join(dir_, "package.json"), "r") as file:
            filex = json.load(file)
    except:
        print("[ERR] Couldn't import from given path.")
        sys.exit(1)

    lister = list(filex['dependencies'].keys())
    if 'devDependencies' in filex:
        lister.append(filex['devDependencies'].keys())
        # OPTIONAL - de-comment if you would like to add peer deps.
        #lister.append(filex['peerDependencies'].keys())
    return lister
    
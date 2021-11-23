import json
import requests
from datetime import datetime as dt
#import xml.etree.ElementTree as ET

# classic api - https://pypi.org/pypi/<package-name>/json
REGISTRY_URL = "https://pypi.org/pypi/"


def recv_pkg_info(pkgs, url=REGISTRY_URL):
    print("[PROC] PyPI registry engaged.")
    payload = {}
    names = []
    for x in pkgs:
        fullurl = url + str(x) + '/json'
        print(fullurl)
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        try:
            res = requests.get(fullurl, params=payload, headers=headers)
        except:
            print("[ERR] Connection error.")
            exit(2)
        try:
            j = json.loads(res.text)
        except:
            x.exists = False
            return
        if j['info']:
            names.append(j['info']['name'])  # add pkgName
            x.exists = True
            latest = j['info']['version']
            for version in j['releases']:
                if version == latest:
                    timex = j['releases'][version][0]['upload_time_iso_8601']
                    fmtx = '%Y-%m-%dT%H:%M:%S.%fZ'
                    unixtime = int(dt.timestamp(dt.strptime(timex, fmtx)) * 1000)
                    x.timestamp = unixtime
            x.verCount = len(j['releases'])
        else:
            x.exists = False
    return names

# TODO add a source scan for pypi alternatives

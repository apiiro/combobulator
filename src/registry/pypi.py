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
"""
def scan_source(dir):
    try:
        path = dir + "./pom.xml"
        tree = ET.parse(path)
        pom = tree.getroot()
        ns = ".//{http://maven.apache.org/POM/4.0.0}"
        lister = []
        for dependencies in pom.findall(ns + 'dependencies'):
            for dependency in dependencies.findall(ns + 'dependency'):
                group = dependency.find(ns + 'groupId').text
                artifact = dependency.find(ns + 'artifactId').text
                lister.append(group + ':' + artifact)
            # print(lister)
        return lister
    except:
        print("[ERR] Couldn't import from given path.")
        exit(1)
"""
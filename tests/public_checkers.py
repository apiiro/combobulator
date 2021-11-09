from pathlib import Path
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import requests
import metapackage

def public_npm_checker(pkg_list):
    print("npm checker")
    url     = 'https://api.npms.io/v2/package/mget'
    payload =  '['+','.join(f'"{w}"' for w in pkg_list.keys())+']' 
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    res = requests.post(url, data=payload, headers=headers)
    x = json.loHads(res.text)
    if not x:
        return
        
    for k,v in x.items():
        print(k)
        uname=""
        email=""
        url=""
        pkg_list[k].update_found_in_global_package_registry(True)
        
        if "author" in v["collected"]["metadata"]:
            uname=v["collected"]["metadata"]["author"]["name"]
            email=v["collected"]["metadata"]["author"]["email"]
            url=v["collected"]["metadata"]["author"]["url"]
        elif "publisher" in v["collected"]["metadata"]:
            uname=v["collected"]["metadata"]["publisher"]["username"]
            email=v["collected"]["metadata"]["publisher"]["email"]

        pkg_list[k].update_global_author_information(uname,email,url)
        downloads_count = v['evaluation']['popularity']['downloadsCount']
        pkg_list[k].update_global_download_count(downloads_count)
    
def public_nuget_checker(pkg_nuget_list):
    print("nuget checker")
    url="https://azuresearch-usnc.nuget.org/query"
    pkg_query = ' '.join(f"PackageId:{w}" for w in pkg_nuget_list.keys()) 

    params={'q':pkg_query,'packageType':'Dependency'}
    res = requests.get(url,params=params)
    x = json.loads(res.text)
    if not x:
        return
    if x["totalHits"] == 0:
        return

    print(res.text)
    for k in x["data"]:
        print(k)
        uname=k["authors"]
        url=k["projectUrl"]
        pkg_nuget_list[k["id"]].update_found_in_global_package_registry(True)
        pkg_nuget_list[k["id"]].update_global_author_information(uname,"",url)
        downloads_count = k['totalDownloads']
        pkg_nuget_list[k["id"]].update_global_download_count(downloads_count)



def public_maven_checker(pkg_maven_list):
    print("maven checker")
    for pkg in pkg_maven_list:
        url='https://search.maven.org/solrsearch/select?q='+pkg+'&rows=1&wt=json'
        res = requests.get(url)
        x=json.loads(res.text)
        if not x:
            continue
        if x['response']['numFound'] == 0:
            continue

        pkg_maven_list[pkg].update_found_in_global_package_registry(True)
        pkg_id=x['response']['docs'][0]['id']
        pkg_g_id=x['response']['docs'][0]['g']
        pkg_a_id=x['response']['docs'][0]['a']
        pkg_l_v=x['response']['docs'][0]['latestVersion']
        pkg_repo_id=x['response']['docs'][0]['repositoryId']
        pkg_maven_list[pkg].update_maven_global_info(pkg_id,pkg_g_id,pkg_a_id,pkg_l_v,pkg_repo_id)


 
def public_pipy_checker(pkg_pipy_list):
    print("pipy checker")
    for pkg in pkg_pipy_list:
        url='https://pypi.org/pypi/'+pkg+'/json'
        res = requests.get(url)
        x=json.loads(res.text)
        if not x:
            continue
        print(res.text)
        pkg_pipy_list[pkg].update_found_in_global_package_registry(True)
        uname=x['info']['author']
        email=x['info']['author_email']
        url=x['info']['package_url']
        pkg_pipy_list[pkg].update_global_author_information(uname,email,url)
        url_release = 'http://pypistats.org/api/packages/'+pkg+'/recent?period=month'
        res2 = requests.get(url_release)
        y=json.loads(res2.text)
        if not y:
            continue
        downloads_count=y['data']['last_month']
        pkg_pipy_list[pkg].update_global_download_count(downloads_count)




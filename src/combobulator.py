import argparse
import os

from dotenv import load_dotenv

# internal module imports
from metapackage import MetaPackage as metapkg
import registry.npm as npm
import registry.maven as maven
import registry.pypi as pypi
from analysis import heuristics as heur

# export
import csv
import sys
from json import dump


SUPPORTED_PACKAGES=['npm', 'pypi', 'maven']
LEVELS = ['compare', "comp", 'heuristics', "heur"]

def init_args():
    # WARNING: don't populate this instance with a hard-coded value
    # it is merely for initializing a string variable.
    GITHUB_TOKEN=""

def parse_args():
    parser = argparse.ArgumentParser(
        prog="combobulator.py",
        description="Dependency Combobulator - Dependency Confusion Checker",
        epilog='Apiiro <Heart> Community',
        add_help=True)
    parser.add_argument("-t", "--type",
                        dest="package_type",
                        help="Package Manager Type, i.e: npm, PyPI, maven",
                        action="store",type=str, choices=SUPPORTED_PACKAGES,
                        required=True )
    # https://docs.python.org/3/library/argparse.html#mutual-exclusion
    # input_group as a mutually exclusive arg group: 
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-l", "--load_list",
                        dest="LIST_FROM_FILE",
                        help="Load list of dependencies from a file",
                        action="append",type=str,
                        default=[] )
    input_group.add_argument("-d", "--directory",
                    dest="FROM_SRC",
                    help="Extract dependencies from local source repository",
                    action="append",
                    type=str)
    input_group.add_argument("-p" "--package",
                            dest="SINGLE",
                            help="Name a single package.",
                            action="append",type=str )
    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument("-c", "--csv",
        dest="CSV",
        help="Export packages properties onto CSV file",
                    action="store", type=str)
    output_group.add_argument("-j", "--json",
                              dest="JSON",
                              help="Export packages properties onto JSON file",
                              action="store", type=str)

    # support variables
    parser.add_argument("-gh", "--github",
                    dest="GITHUB_TOKEN",
                    help="GitHub Access Token (Overrides .env file setting)",
                    action="store", type=str )
    parser.add_argument("-a", "--analysis",
        dest="LEVEL",
        help="Required analysis level - compare (comp), heuristics (heur) (default: compare)",
                    action="store", default="compare", type=str,
                    choices = LEVELS)
    return parser.parse_args()


def load_env():
    """
    .env file example:

    # GitHub Token
    GITHUB_TOKEN=ghp_123456789012345678901234567890123456
    """

    load_dotenv('.env')
    GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')


def load_pkgs_file(pkgs):
    try:
        lister = []
        lines = open(pkgs).readlines()
        for i in lines:
            lister.append(i.strip())
        return lister
    except:
        print("[ERR]  Cannot process input list/file")
        raise TypeError

def scan_source(pkgtype, dir):
    if pkgtype == "npm":
        return npm.scan_source(dir)
    elif pkgtype == "maven":
        return maven.scan_source(dir)
    #TODO: add pypi scanner
    else:
        print("[ERROR]  Selected package type doesn't support import scan.")
        sys.exit(1)

def check_against(check_type, check_list):
    if check_type == "npm":
        response = npm.recv_pkg_info(check_list)
        return response
    elif check_type == "NuGet":
        return True #placeholder
    elif check_type == "maven":
        response = maven.recv_pkg_info(check_list)
        return response
    elif check_type == "pypi":
        response = pypi.recv_pkg_info(check_list)

def export_csv(instances, path):
    #filer = open(path, 'w', newline='')
    headers = ["Package Name","Package Type", "Exists on External",
            "Org/Group ID","Score","Version Count","Timestamp"]
    rows = [headers]
    for x in instances:
        rows.append(x.listall())
    try:
        with open(path, 'w', newline='') as file:
            export = csv.writer(file)
            export.writerows(rows)
        print("[EXPORT]  CSV file has been successfuly exported at: " + path)
    except:
        print("[ERROR]  CSV file couldn't be written to disk.")
        sys.exit(1)


def export_json(instances, path):
    headers = ["Package Name", "Package Type", "Exists on External",
               "Org/Group ID", "Score", "Version Count", "Timestamp"]
    data = [{k: v for k, v in zip(headers, x.listall())} for x in instances]
    print(len(instances))
    print(data)
    try:
        with open(path, 'w', newline='') as file:
            dump(data, file)

        print("[EXPORT]  JSON file has been successfuly exported at: " + path)
    except:
        print("[ERROR]  JSON file couldn't be written to disk.")
        sys.exit(1)


def main():
    # envs to be consumed: GITHUB_TOKEN
    init_args()
    load_env()

    # the most important part of any program starts here

    print("""
  ____  _____ ____  _____ _   _ ____  _____ _   _  ______   __
 |  _ \| ____|  _ \| ____| \ | |  _ \| ____| \ | |/ ___\ \ / /
 | | | |  _| | |_) |  _| |  \| | | | |  _| |  \| | |    \ V / 
 | |_| | |___|  __/| |___| |\  | |_| | |___| |\  | |___  | |  
 |____/|_____|_|   |_____|_| \_|____/|_____|_| \_|\____| |_|  

   ____ ____  __  __ ____   ____  ____  _   _ _        _  _____ ____  ____  
  / ___/ /\ \|  \/  | __ ) / /\ \| __ )| | | | |      / \|_   _/ /\ \|  _ \ 
 | |  / /  \ \ |\/| |  _ \/ /  \ \  _ \| | | | |     / _ \ | |/ /  \ \ |_) |
 | |__\ \  / / |  | | |_) \ \  / / |_) | |_| | |___ / ___ \| |\ \  / /  _ < 
  \____\_\/_/|_|  |_|____/ \_\/_/|____/ \___/|_____/_/   \_\_| \_\/_/|_| \_\
""")

    # are you amazed yet?

    # SCAN & FLAG ARGS
    args = parse_args()
    print("[PROC] Arguments parsed.")
    GITHUB_TOKEN = args.GITHUB_TOKEN

    #IMPORT
    if args.LIST_FROM_FILE:
        pkglist = load_pkgs_file(args.LIST_FROM_FILE[0])
    elif args.FROM_SRC:
        pkglist = scan_source(args.package_type, args.FROM_SRC[0])
    elif args.SINGLE:
        pkglist = []
        pkglist.append(args.SINGLE[0])
    print("[PROC] Package list imported....  " + str(pkglist))
    
    if args.package_type == 'npm':
        for x in pkglist:
            metapkg(x, args.package_type)
    if args.package_type == 'maven':
        for x in pkglist: # format orgId:packageId
            metapkg(x.split(':')[1], args.package_type, x.split(':')[0])
    if args.package_type == 'pypi':
        for x in pkglist:
            metapkg(x, args.package_type)

    # QUERY & POPULATE
    check_against(args.package_type, metapkg.instances)

    # ANALYZE
    if args.LEVEL == LEVELS[0] or args.LEVEL == LEVELS[1]:
        heur.combobulate_min(metapkg.instances)
    elif args.LEVEL == LEVELS[2] or args.LEVEL == LEVELS[3]:
        heur.combobulate_heur(metapkg.instances)

    # OUTPUT
    if args.CSV:
        export_csv(metapkg.instances, args.CSV)
    if args.JSON:
        export_json(metapkg.instances, args.JSON)


if __name__ == "__main__":
    main()
import os
import json
import sys
import csv
import requests
import base64
from getpass import getpass
from npmvaliddep.utils.github_url import get_github_file_url
from npmvaliddep.utils.dependency_change import get_dependency_version_flag

def getgithubcreds():
    github_path = os.path.join(os.getcwd(), 'github.json')
    exist = os.path.exists(github_path)
    if not exist:
        temp_github_json = {"github_username": "", "github_password": ""}
        with open(github_path, "w") as outfile:
            outfile.write(json.dumps(temp_github_json, indent = 4))

    with open("github.json", "r") as f:
        variables = json.load(f)

    print(f"Github username: {variables['github_username']}")
    print(f"Github password: ****")

def setgithubcreds():
    variables = {}
    variables["github_username"] = input("Enter github username: ")
    variables["github_password"] = getpass("Enter github password: ")

    with open("github.json", "w") as f:
        json.dump(variables, f, indent = 4)

def matchgithubpass():
    with open("github.json", "r") as f:
        variables = json.load(f)

    password = getpass("Enter github password: ")
    
    if password == variables["github_password"]:
        print("Password matched")
    else:
        print("Password does not match try agaain or reset credentials using --setgithubcreds !!")

def check_dependency(args):
    with open("github.json", "r") as f:
        variables = json.load(f)

    if variables["github_username"] == "":
        print("Please set github credentials first using --setgithubcreds !!")
        sys.exit()

    csv_path = args.check[0]

    pipe = os.popen("node --version")
    data = pipe.read().strip().split('\n')
    pipe.close()

    if data[0] == '':
        print("Please install node !!")
        sys.exit()

    pipe = os.popen("npm --version")
    data = pipe.read().strip().split('\n')
    pipe.close()

    if data[0] == '':
        print("Please install npm !!")
        sys.exit()

    if not args.deps:
        print("Please specify dependencies to check !!")

    dependencies = [[x.split("@")[0], x.split("@")[1]] for x in args.deps]

    try:
        f = open(csv_path, "r")
    except:
        print("Input file not found/accessible !!")
        sys.exit()

    try:
        if args.output:
            fo = open(args.output[0], "w")
        else:
            fo = open(os.path.expanduser("~/output.csv"), "w")
        
        fieldnames = ['name', 'repo']

        for d in dependencies:
            fieldnames.extend([d[0], f"{d[0]}_satisfied"])

        if args.createpr:
            fieldnames.append('update_pr')

        writer = csv.DictWriter(fo, fieldnames)
        writer.writeheader()
    except:
        print("Cannot generate file !!")
        sys.exit()

    csv_reader = csv.DictReader(f)

    for r in csv_reader:
        record = dict(r)
        github_url = get_github_file_url(record["repo"])
        req = requests.get(github_url, headers={
            "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
        })
        if req.status_code == requests.codes.ok:
            owner = record["repo"].split("https://github.com/")[1].split("/")[0]
            if owner == variables["github_username"]:
                owner = True
            else:
                owner = False

            if not args.createpr:
                data = get_dependency_version_flag(req, record, dependencies, False, variables, owner)
            else:
                data = get_dependency_version_flag(req, record, dependencies, True, variables, owner)
            
            writer.writerow(data)

        else:
            print(f'Cannot access - {record["name"]} !!')
            continue

    fo.close()
import json
import base64
import requests
import os
from npmvaliddep.utils.github_url import *

def get_dependency_version_flag(req, record, dependencies, update, variables, owner):
    req = req.json()
    content = json.loads(base64.b64decode(req["content"]).decode())

    data = {
        "name": record["name"],
        "repo": record["repo"]
    }

    dependencies_to_update = []

    for d in dependencies:
        if d[0] in content["dependencies"]:
            current_version = content["dependencies"][d[0]]
            if (content["dependencies"][d[0]][0] == '^') or (content["dependencies"][d[0]][0] == '~'):
                current_version = content["dependencies"][d[0]][1:]
            else:
                current_version = content["dependencies"][d[0]]

            if current_version >= d[1]:
                data[d[0]] = current_version
                data[f'{d[0]}_satisfied'] = True
            else:
                dependencies_to_update.append(d)
                data[d[0]] = current_version
                data[f'{d[0]}_satisfied'] = False
        else:
            data[d[0]] = "Not Found"
            data[f'{d[0]}_satisfied'] = "NA"

    if update:
        if len(dependencies_to_update) == 0:
            data["update_pr"] = ""
        else:
            if not owner:
                data["update_pr"] = get_dependency_update_fork(record, content, dependencies_to_update, variables)
            else:
                data["update_pr"] = "NA"
                get_dependency_update_commit(record, content, dependencies_to_update, variables)

    return data

def get_dependency_update_fork(record, content, dependencies_to_update, variables):
    fork_url = get_github_fork_url(record["repo"])
    fork_repo = requests.post(fork_url, headers={
        "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
    })
    if fork_repo.status_code == 202:

        for d in dependencies_to_update:
            if (content["dependencies"][d[0]][0] == '^') or (content["dependencies"][d[0]][0] == '~'):
                content["dependencies"][d[0]] = content["dependencies"][d[0]][0] + d[1]
            else:
                content["dependencies"][d[0]] = d[1]

        package_json_url = get_github_package_json_url(variables["github_username"], record["repo"])
        req = requests.get(package_json_url, headers={
            "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
        })
        
        package_sha = req.json()["sha"]

        update_string = ", ".join([x[0] for x in dependencies_to_update])

        update_data = base64.b64encode(json.dumps(content, indent=2).encode('utf-8')).decode()
        req = requests.put(package_json_url, 
            json = {
                "message": f"Update package.json for - {update_string}",
                "content": update_data,
                "sha": package_sha,
            },
            headers={
                "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
            }
        )

        path = os.path.join(os.getcwd(), 'temp_data')
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)
        os.chdir(path)

        json_object = json.dumps(content, indent = 4)
        package_path = os.path.join(path, 'package.json')
        with open(package_path, "w") as outfile:
            outfile.write(json_object)

        pipe = os.popen("npm i --package-lock-only")
        _ = pipe.read().strip().split('\n')
        pipe.close()

        package_lock_path = os.path.join(path, 'package-lock.json')
        with open(package_lock_path, "r") as package_lock_file:
            package_lock_json = json.load(package_lock_file)

        package_lock_url = get_github_package_lock_url(variables["github_username"], record["repo"])

        req = requests.get(package_lock_url, headers={
            "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
        })
        
        update_data = base64.b64encode(json.dumps(package_lock_json, indent=2).encode('utf-8')).decode()
        try:
            package_lock_sha = req.json()["sha"]
            req = requests.put(package_lock_url, 
                json = {
                    "message": f"Update package-lock.json for - {update_string}",
                    "content": update_data,
                    "sha": package_lock_sha,
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
                }
            )
        except:
            req = requests.put(package_lock_url, 
                json = {
                    "message": f"Update package-lock.json for - {update_string}",
                    "content": update_data,
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
                }
            )

        os.remove(package_lock_path)
        os.remove(package_path)

        if req.status_code == 200 or req.status_code == 201:
            pull_url = get_github_pull_url(record["repo"])
            req = requests.post(pull_url,
                json = {
                    "title": "Dependency Update",
                    "body": f"Dependency update for packages - {update_string}",
                    "head": f"{variables['github_username']}:main",
                    "base": f"main"
                },
                headers = {
                    "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
                }
            )

            if req.status_code == 201:
                return req.json()["html_url"]
            else:
                print(f"Pull request failed - {fork_repo.json()['html_url']} !!")

        else:
            print(f"Commiting to forked repo failed - {fork_repo.json()['html_url']} !!")

    else:
        print(f"Fork failed - {fork_repo} !!")

    return ""

def get_dependency_update_commit(record, content, dependencies_to_update, variables):

    for d in dependencies_to_update:
        if (content["dependencies"][d[0]][0] == '^') or (content["dependencies"][d[0]][0] == '~'):
            content["dependencies"][d[0]] = content["dependencies"][d[0]][0] + d[1]
        else:
            content["dependencies"][d[0]] = d[1]

    package_json_url = get_github_package_json_url(variables["github_username"], record["repo"])
    req = requests.get(package_json_url, headers={
        "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
    })
    
    package_sha = req.json()["sha"]

    update_string = ", ".join([x[0] for x in dependencies_to_update])

    update_data = base64.b64encode(json.dumps(content, indent=2).encode('utf-8')).decode()
    req = requests.put(package_json_url, 
        json = {
            "message": f"Update package.json for - {update_string}",
            "content": update_data,
            "sha": package_sha,
        },
        headers={
            "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
        }
    )

    path = os.path.join(os.getcwd(), 'temp_data')
    exist = os.path.exists(path)
    if not exist:
        os.makedirs(path)
    os.chdir(path)

    json_object = json.dumps(content, indent = 4)
    package_path = os.path.join(path, 'package.json')
    with open(package_path, "w") as outfile:
        outfile.write(json_object)

    pipe = os.popen("npm i --package-lock-only")
    _ = pipe.read().strip().split('\n')
    pipe.close()

    package_lock_path = os.path.join(path, 'package-lock.json')
    with open(package_lock_path, "r") as package_lock_file:
        package_lock_json = json.load(package_lock_file)

    package_lock_url = get_github_package_lock_url(variables["github_username"], record["repo"])

    req = requests.get(package_lock_url, headers={
        "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
    })
    
    update_data = base64.b64encode(json.dumps(package_lock_json, indent=2).encode('utf-8')).decode()
    try:
        package_lock_sha = req.json()["sha"]
        req = requests.put(package_lock_url, 
            json = {
                "message": f"Update package-lock.json for - {update_string}",
                "content": update_data,
                "sha": package_lock_sha,
            },
            headers={
                "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
            }
        )
    except:
        req = requests.put(package_lock_url, 
            json = {
                "message": f"Update package-lock.json for - {update_string}",
                "content": update_data,
            },
            headers={
                "Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')
            }
        )

    os.remove(package_lock_path)
    os.remove(package_path)

    if req.status_code != 200 and req.status_code != 201:
        print(f"Commiting to repo failed - {record['repo']} !!")
    
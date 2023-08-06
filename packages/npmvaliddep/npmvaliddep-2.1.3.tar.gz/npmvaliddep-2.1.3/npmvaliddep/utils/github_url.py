def get_github_file_url(url):
    url = url.split("https://github.com/")[1].split("/")
    username, repo = url[0], url[1]
    new_url = f"https://api.github.com/repos/{username}/{repo}/contents/package.json"
    return new_url

def get_github_fork_url(url):
    url = url.split("https://github.com/")[1].split("/")
    username, repo = url[0], url[1]
    new_url = f"https://api.github.com/repos/{username}/{repo}/forks"
    return new_url

def get_github_package_json_url(username, url):
    url = url.split("https://github.com/")[1].split("/")
    user, repo = url[0], url[1]
    new_url = f"https://api.github.com/repos/{username}/{repo}/contents/package.json"
    return new_url

def get_github_package_lock_url(username, url):
    url = url.split("https://github.com/")[1].split("/")
    user, repo = url[0], url[1]
    new_url = f"https://api.github.com/repos/{username}/{repo}/contents/package-lock.json"
    return new_url

def get_github_pull_url(url):
    url = url.split("https://github.com/")[1].split("/")
    username, repo = url[0], url[1]
    new_url = f"https://api.github.com/repos/{username}/{repo}/pulls"
    return new_url
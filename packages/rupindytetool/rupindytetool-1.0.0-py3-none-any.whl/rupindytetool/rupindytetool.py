import json
import wget
import git
import os
from github import Github
import argparse
import requests
from git import Repo, GitCommandError
def url_pull_request(project_name, repo_name, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    payload = {
        "owner":project_name,
        "repo":repo_name,
    }
    r=requests.get(
        git_pulls_api,
        auth=(project_name,git_token),
        data=json.dumps(payload),
        )

    if not r.ok:
        print("Request Failed: {0}".format(r.text))
    return(r.json()[0]['url'])

def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)

    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "owner":project_name,
        "repo":repo_name,
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }
    # s = requests.Session()
    # res = s.get('https://github.com/login').text, 'html.parser'
    r=requests.post(
        git_pulls_api,
        auth=(project_name,git_token),
        data=json.dumps(payload),
        )

    if not r.ok:
        print("Request Failed: {0}".format(r.text))


def forking(url):

    token = "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"
    g = Github(token)
    user = g.get_user()
    url = str(url).replace("https://github.com/", "").split("/")
    org = g.get_organization(url[0])
    repo = org.get_repo(url[1])
    my_fork = user.create_fork(repo)
    print("https://github.com/" + str(user.login) + "/" + str(repo.name) + ".git",
                                     os.getcwd() + "/" + str(repo.name))
    try:
        git.Git(url[1]).clone("https://github.com/" + str(user.login) + "/" + str(repo.name) + ".git")
    except GitCommandError:
        print
        "Directory already exists and is not empty. Not cloning."
        pass
def versionCompare(v1, v2):
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    n = len(arr1)
    m = len(arr2)

    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]
    if n > m:
        for i in range(m, n):
            arr2.append(0)
    elif m > n:
        for i in range(n, m):
            arr1.append(0)
    for i in range(len(arr1)):
        if arr1[i] > arr2[i]:
            return 1
        elif arr2[i] > arr1[i]:
            return -1
    return 0
def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", required=True,nargs="+",
        help="CSV file path <space> dependency version")
    ap.add_argument("-u","--update",metavar='update')
    args = vars(ap.parse_args())
    print(args['i'])
    if(args['update']):
        print("yes")

    gg = Github("patel-rupin2000", "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")
    github_user = gg.get_user()

    import pandas as pd
    df = pd.read_csv(args['i'][0])
    t=df['repo']
    names=df['name']
    t.to_numpy()
    names.to_numpy()
    s=""
    print(t)
    versions=[]
    check=[]
    update=[]
    for i in range (0,len(t)):
        s=t[i].replace("github.com","raw.githubusercontent.com")
        s+="master/package.json"
        print(s)
        q=t[i].replace("github.com","raw.githubusercontent.com")
        q+="master/package-lock.json"
        if not os.path.exists("jsonfiles/"+names[i]):
            os.makedirs("jsonfiles/"+names[i])
        file_name = wget.download(s,"jsonfiles/"+names[i]+"/"+"package.json")
        file_name_q = wget.download(s, "jsonfiles/" + names[i] + "/" + "package-lock.json")
        f = open("jsonfiles/"+names[i]+"/"+"package.json")
        fq=open("jsonfiles/"+names[i]+"/"+"package-lock.json")
        data = json.load(f)
        dataq=json.load(fq)
        print(data['dependencies'][args['i'][1].split('@')[0]])
        current_version=data['dependencies'][str(args['i'][1].split("@")[0])][1:]
        versions.append(current_version)
        ans = versionCompare(current_version, args['i'][1].split('@',1)[1])
        f.close()
        if ans < 0:
            check.append(False)
            if (args['update']):
                forking(t[i])

                data['dependencies'][args['i'][1].split('@')[0]]='^'+args['i'][1].split('@',1)[1]
                dataq['dependencies'][args['i'][1].split('@')[0]] = '^' + args['i'][1].split('@', 1)[1]
                f = open(t[i][19:].split("/")[1]+"/"+"package.json", "w")
                fq = open(t[i][19:].split("/")[1] + "/" + "package-lock.json", "w")

                json.dump(data, f)
                json.dump(data,fq)
                f.close()
                fq.close()


                repo = git.Repo(t[i][19:].split("/")[1])
                eq=repo.create_head("Test")
                eq.checkout()
                print(repo.head)
                print(repo.branches)
                with repo.config_writer() as git_config:
                    git_config.set_value('user', 'email', 'patelrupin63@gmail.com')
                    git_config.set_value('user', 'name', 'Rupin Patel')
                origin = repo.create_remote('Test', "https://github.com/patel-rupin2000/" + t[i][19:].split("/")[1])
                repo.index.add(["package.json","package-lock.json"])
                repo.index.commit('Initial commit.')

                repo.git.push('--set-upstream',repo.head.ref)


                create_pull_request("patel-rupin2000",t[i][19:].split("/")[1],"update","change of version of "+args['i'][1].split('@',1)[0]+ " current_version to "+args['i'][1].split('@',1)[1],"Test","main","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")
                update.append(url_pull_request("patel-rupin2000",t[i][19:].split("/")[1],"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"))


        else:
            check.append(True)
            update.append("--")
    df['version']=versions
    df['version_satisfied']=check
    if(args['update']):
        df['update_pr']=update
    df.to_csv('result.csv')



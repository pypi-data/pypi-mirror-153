import argparse
from distutils.dir_util import create_tree
import sys
import requests
import base64
import json
from openpyxl import Workbook 
import csv



#Create fork
def create_fork(repo_name,own_user, username, token):
    try:
        url = "https://api.github.com/repos/"+str(own_user)+"/"+str(repo_name)+"/forks"
        rpost = requests.post(url, auth=(username, token))
        return True
    except:
        return False


def comp_ver(curr_ver, dep_ver):
    curr_ver = curr_ver.split(".")
    dep_ver = dep_ver.split(".")
    for i in range(len(curr_ver), len(dep_ver)):
        curr_ver.append(0)
    for i in range(len(dep_ver), len(curr_ver)):
        dep_ver.append(0)
    for i in range(len(curr_ver)):
        n = int(curr_ver[i])
        m = int(dep_ver[i])
        if n>m:
            #print("version true")
            return True
        if n<m:
            
            return False
   
    return True

def update_version(data, dep_name, dep_ver, username, repo_name, user_email, sha, token):
    msg = json.dumps(data, indent=2)
    msg = msg.encode('utf-8')
    enc_data=str(base64.b64encode(msg))[2:-1]

    payload = {
    "message": "updated "+dep_name +" version to "+dep_ver,
    "committer": {
        "name": username,
        "email": user_email
    },
    "content": enc_data,
    "sha": sha
    }

    st_data=json.dumps(payload)
    url = "https://api.github.com/repos/"+username+"/"+repo_name+"/contents/package.json"

    res = requests.put(url, auth=(username, token), data=st_data)



def check_and_update_version(dep_name,  dep_ver, username, repo_name, user_email, token, to_update):
    url = "https://api.github.com/repos/"+username+"/"+repo_name+"/contents/package.json"
    req = requests.get(url)

    if req.status_code == 200:
        req = req.json()
        data = json.loads(base64.b64decode(req['content']))

        try:
            curr_ver = data['dependencies'][dep_name][1:]
            sym = data['dependencies'][dep_name][0:1]
            comp_res = comp_ver(curr_ver, dep_ver)
            if not comp_res and to_update == True:
                data['dependencies'][dep_name]=sym+dep_ver
                update_version(data, dep_name, dep_ver, username, repo_name, user_email, req['sha'], token)
                
                return [True,curr_ver, "false"]

            else:
                if not comp_res:
                    return [True,curr_ver, "false"]
                return [False,curr_ver, "true"]
        except:
            return [False,"No dependency of this name found", "NA"]


def create_pr(own_user, username, repo_name, token, dep_name, dep_ver):
    payload = {
        "title": "updated "+dep_name +" version to "+dep_ver,
        "head": username+":main",
        "base": "main",
    }
    st_data=json.dumps(payload)

    url = "https://api.github.com/repos/"+own_user+"/"+repo_name+"/pulls"
    res = requests.post(url, auth=(username, token), data=st_data)
    res = res.json()
    return res['url']
    

def parse_file(args):
    if not args.file:
        return "Please give file name"
    if not args.dep:
        return "Please give which dependency to check"
    if not args.user:
        return "Please give your github username"
    if not args.auth:
        return "Please give github auth token"
    if not args.email:
        return "Please give github email"
    try:
        file_name = args.file
        repo_list = []
        with open(file_name, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                repo_list.append(row)
    except:
        print("No file found")
        
    username = args.user
    token = args.auth
    dep_list = args.dep.split('@')
    dep_name = dep_list[0]
    dep_ver = dep_list[1]
    user_email = args.email
    output = []
   

    if args.u:
        output.append(["name", "repo-link", "version", "version-satisfies", "update_pr"])
        for i in range(1,len(repo_list)):
            name = repo_list[i][0]
            repo_link = repo_list[i][1]
            repo_name = repo_link.split('/')[4]
            own_user = repo_link.split('/')[3]
            flag = 0

           
            f_res = create_fork(repo_name,own_user, username, token)
            if f_res:
                c_res,c_ver,msg = check_and_update_version(dep_name, dep_ver, username, repo_name, user_email, token, True)
                if c_res:
                    flag = 1
                    link = create_pr(own_user, username, repo_name, token, dep_name, dep_ver)
            if f_res and flag == 1:
                output.append([name, repo_link, c_ver, msg, link])
            elif f_res:
                output.append([name, repo_link, c_ver, msg])
    else:
        output.append(["name", "repo-link", "version", "version-satisfies"])
        for i in range(1,len(repo_list)):
            name = repo_list[i][0]
            repo_link = repo_list[i][1]
            repo_name = repo_link.split('/')[4]
            own_user = repo_link.split('/')[3]

           
            f_res = create_fork(repo_name,own_user, username, token)
            if f_res:
                c_res,c_ver,msg = check_and_update_version(dep_name, dep_ver, username, repo_name, user_email, token, False)

            if f_res:
                output.append([name, repo_link, c_ver, msg])
            
    
    f= open("./output.csv","w+")  
    wb = Workbook()  
    sheet = wb.active  

    for i in output:  
        sheet.append(i)  
    wb.save('./output.csv') 
    return "Output saved in output.csv file"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help="It is used for inputting a file")
    parser.add_argument('--u', '--foo', action='store_true', help="It is used for updating a file")
    parser.add_argument('--dep', type=str, help="It is used for inputting dependency version to check")
    parser.add_argument('--user', type=str, help="It is used for inputting github username")
    parser.add_argument('--auth', type=str, help="It is used for inputting github auth token")
    parser.add_argument('--email', type=str, help="It is used for inputting github email")


    args = parser.parse_args()
    sys.stdout.write(str(parse_file(args)))
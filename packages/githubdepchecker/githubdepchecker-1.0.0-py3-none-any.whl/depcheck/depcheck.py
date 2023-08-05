import argparse
import csv
import base64
import requests
import json
import getpass
import os
import subprocess
import shutil
import sys

def main(main_args=None):

    if main_args is None:
        main_args = sys.argv[1:]

    my_parser = argparse.ArgumentParser(prog='test', usage='%(prog)s [options] path', description="CLI Tool to check dependencies of github repositories and update them accordingly. Type -h for list of commands.")

    my_parser.add_argument('-i', nargs=2, type=str, help="Enter the path of the csv and package to check dependency.")
    my_parser.add_argument('--update', default=False, action=argparse.BooleanOptionalAction, help="Create PR for updating dependencies.")
    my_parser.add_argument('--getgitconfig', default=False, action=argparse.BooleanOptionalAction, help="Get Your Github Configurations")
    my_parser.add_argument("--setgitconfig",nargs=2,type=str, help="Set your git username and password")

    args = my_parser.parse_args(main_args)

    config_path = os.path.join(os.getcwd(), 'config.json')
    exist = os.path.exists(config_path)
    if not exist:
        temp_config_json = {"github_username": "", "github_password": ""}
        with open(config_path, "w") as outfile:
            outfile.write(json.dumps(temp_config_json))

    with open("config.json", "r") as f:
        variables = json.load(f)

    if args.getgitconfig:
        print("Username: " + variables["github_username"])
        print("Password: " + variables["github_password"])

    if args.setgitconfig:
        variables["github_username"] = args.setgitconfig[0]
        variables["github_password"] = args.setgitconfig[1]

        with open("config.json", "w") as f:
            json.dump(variables, f)

    if not variables["github_username"] or not variables["github_password"]:
        variables["github_username"] = input('Github Username: ')
        variables["github_password"] = getpass.getpass(prompt='Password: ')

        with open("config.json", "w") as f:
            json.dump(variables, f)


    rows = []
    header = []

    if args.i:
        file = open(args.i[0])
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:
            temp_dic = {}
            for i in range(len(header)):
                temp_dic[header[i]] = row[i]
            rows.append(temp_dic)

        dependency_arr = args.i[1].split("@")
        dependency_name = dependency_arr[0]
        dependency_version = dependency_arr[1]


    if args.update:
        result_header = ["name", "repo", "version", "version_satisfied", "update_pr"]
    else:
        result_header = ["name", "repo", "version", "version_satisfied"]
    result_rows = []

    for i in rows:
        if "repo" in i:
            repo_link = i["repo"]
            x = repo_link.split("/")
            url = 'https://api.github.com/repos/' + x[3] + '/' + x[4] + '/contents/package.json'
            req = requests.get(url,headers={"Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')})
            if req.status_code == requests.codes.ok:
                req = req.json()
                content = base64.b64decode(req['content'])
                raw_data = json.loads(content.decode())["dependencies"]
                if dependency_name in raw_data:
                    if raw_data[dependency_name][1:] >= dependency_version:
                        res = True
                    else:
                        res = False
                    
                if args.update and not res:
                    fork_url = 'https://api.github.com/repos/' + x[3] + '/' + x[4] + '/forks'
                    fork_req = requests.post(fork_url,headers={"Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')})
                    if fork_req.status_code == 202:
                        fork_req = fork_req.json()

                        forked_repo_url = fork_req["html_url"]
                        forked_repo_url_username = forked_repo_url.split('/')[-2]
                        forked_repo_url_name = forked_repo_url.split('/')[-1]

                        try:
                            os.system("git clone https://" + variables["github_username"] + ":" + variables["github_password"] + "@github.com/" + forked_repo_url_username + "/" + forked_repo_url_name + ".git")
                            original_dir = os.getcwd()
                            dir = original_dir + "/" + forked_repo_url_name

                            os.chdir(dir)
                            os.system("npm install " + args.i[1])
                            os.system("git add ./package.json ./package-lock.json")
                            os.system("git commit -m 'Dependencies updated'")
                            os.system("git push")

                            original_repo_pull_url = "https://api.github.com/repos/" + x[3] + '/' + x[4] + "/pulls"
                            repo_pull_req = requests.post(original_repo_pull_url,
                            json={
                                "title": "Dependency update: " + dependency_name + " updated to " + dependency_version,
                                "body": dependency_name + " updated from version " + raw_data[dependency_name][1:] + " to " + dependency_version,
                                "head": forked_repo_url_username + ":main",
                                "base": "main"
                            },
                            headers={"Authorization": "Basic " + base64.b64encode(("%s:%s" % (variables["github_username"], variables["github_password"])).encode('utf-8')).decode('utf-8')})

                            pr_url = repo_pull_req.json()["html_url"]

                            shutil.rmtree(dir)
                            os.chdir(original_dir)
                            
                        except:
                            print("Some error occured!")
                    else:
                        print("Some error occured while creating the fork!")

                    temp_row = [i["name"], i["repo"], raw_data[dependency_name][1:], res, pr_url]
                else:
                    temp_row = [i["name"], i["repo"], raw_data[dependency_name][1:], res]
                
                print(temp_row)
                result_rows.append(temp_row)    
            else:
                print('Content was not found.')

    if len(result_rows) != 0:
        with open(os.path.expanduser("~/output.csv"), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(result_header)

            # write the data
            writer.writerows(result_rows)
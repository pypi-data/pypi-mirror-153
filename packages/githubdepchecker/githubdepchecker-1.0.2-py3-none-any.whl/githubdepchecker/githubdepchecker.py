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

# Entry point of the cli tool
def main(main_args=None):

    if main_args is None:
        main_args = sys.argv[1:]

    # Initializing the argument parser
    my_parser = argparse.ArgumentParser(prog='githubdepcheck', usage='%(prog)s [options] path', description="CLI Tool to check dependencies of github repositories and update them accordingly. Type -h for list of commands.")

    # Adding the arguments 
    my_parser.add_argument('-i', nargs=2, type=str, help="Enter the path of the csv and package to check dependency.")
    my_parser.add_argument('--update', default=False, action=argparse.BooleanOptionalAction, help="Create PR for updating dependencies.")
    my_parser.add_argument('--getgitconfig', default=False, action=argparse.BooleanOptionalAction, help="Get Your Github Configurations")
    my_parser.add_argument("--setgitconfig",nargs=2,type=str, help="Set your git username and password")

    args = my_parser.parse_args(main_args)

    # Github username and password will be stored in
    # a file called config.json. If file is not created before,
    # it will be created with github_username and github_password
    # variables.
    config_path = os.path.join(os.getcwd(), 'config.json')
    exist = os.path.exists(config_path)
    if not exist:
        temp_config_json = {"github_username": "", "github_password": ""}
        with open(config_path, "w") as outfile:
            outfile.write(json.dumps(temp_config_json))

    with open("config.json", "r") as f:
        variables = json.load(f)


    # Getgitconfig is for getting the github configurations user has set
    if args.getgitconfig:
        print("Username: " + variables["github_username"])
        print("Password: " + variables["github_password"])

    # Setgitconfig is for setting or changing the github configurations
    if args.setgitconfig:
        variables["github_username"] = args.setgitconfig[0]
        variables["github_password"] = args.setgitconfig[1]

        with open("config.json", "w") as f:
            json.dump(variables, f)

    # If user has not set the github configurations yet then it will first
    # ask github username and password and configure it automatically.
    if not variables["github_username"] or not variables["github_password"]:
        variables["github_username"] = input('Github Username: ')
        variables["github_password"] = getpass.getpass(prompt='Password: ')

        with open("config.json", "w") as f:
            json.dump(variables, f)


    rows = []
    header = []

    # if --i command is used, get the file path and retrieve rows
    # of the csv files and dependency name and version
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

    # if --update argument is used, then reesult_header will have an extra field
    # of update_pr
    if args.update:
        result_header = ["name", "repo", "version", "version_satisfied", "update_pr"]
    else:
        result_header = ["name", "repo", "version", "version_satisfied"]
    result_rows = []

    for i in rows:
        if "repo" in i:
            repo_link = i["repo"]
            x = repo_link.split("/")

            # Get the package.json file of each repository and check the dependency_version for the
            # dependency passed in arguments
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

                
                # If --update argument is passed and dependency needs to updated in
                # the given repository, then following steps will be followed:
                # 1] Repository will be forked through user's account
                # 2] the forked repository will then get cloned into local Directory
                # 3] "npm install " + dependency will run which will automatically update the dependency 
                #     with specified version and will automatically update package.json and package-lock.json.
                # 4] Changes in file package.json and package-lock.json will then be committed and pushed into fork repository.
                # 5] Pull Request will be generated from fork repository to main repository for dependency update.
                # 6] The cloned repository on local will get deleted.
                    
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
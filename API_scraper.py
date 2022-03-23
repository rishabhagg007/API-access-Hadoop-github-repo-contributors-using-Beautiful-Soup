import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
from datetime import datetime
import re


time.sleep(60*60)
# url needed to get the most recent 100 contributors of hadoop
initial_url = "https://api.github.com/repos/apache/hadoop/contributors?per_page=100&page="
# access token to get the data with multiple requests
personal_access_token = "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"
header = {"Authorization": "token " + personal_access_token}

# go to the desired url for the api and return the data as a json object
def collect_data(url):
    api = requests.get(url, headers = header)
    doc = BeautifulSoup(api.content, 'html.parser')
    #remove these random emails at the end of the file
    doc = str(doc)
    if "https://api.github.com/repos/apache/hadoop/commits?per_page=100" in url:
        doc = doc.replace(str(re.findall("<\/.*@.*\..*>",doc)[0]), "")
    json_dict = json.loads(doc)
    return json_dict

# get the information on the repo
def get_repo(login_id):
    pages = 1
    repos= collect_data("https://api.github.com/users/"+ login_id + "/repos?per_page=100")
    num_cont = []
    repo_names = []
    while len(repos) == 100:
        # loop through the users repos
        for repo in repos:
            # get their contributions
            num_cont.append(repo_contributions(login_id, repo))
            repo_names.append(repo['name'])
        pages = pages + 1
        repos = collect_data("https://api.github.com/users/"+ login_id + "/repos?per_page=100&page=" + str(pages))
    # loop through the users repos
    for repo in repos:
        # get their contributions
        num_cont.append(repo_contributions(login_id, repo))
        repo_names.append(repo['name'])
    # get the number of repos the user has
    num_repo = len(repos) + 100 * (pages - 1)
    return login_id, num_repo, repo_names, num_cont

# get the number of  contributions made to the repo
def repo_contributions(id, repo):
    # check for issues in the data
    if repo['size'] == 0 or repo['language'] == None:
        if "message" in collect_data("https://api.github.com/repos/" + id + "/" + repo['name'] + "/contents"):
            return None
    # if there are no issues in the data collect the number of contributions and if they have contributed to the repo
    user_data = collect_data(repo["contributors_url"] + "?per_page=100")
    for user in user_data:
        if user['login'] == id:
            return user['contributions']
    return 0
# get the time data for the difference between the most recent and 100th commit
def get_time():
    time_data = collect_data("https://api.github.com/repos/apache/hadoop/commits?per_page=100")
    recent_data = time_data[0]['commit']['author']['date'].replace("Z", "")
    recent_data = recent_data.replace("T", " ")
    recent = datetime.strptime(recent_data, '%Y-%m-%d %H:%M:%S')
    old_data = time_data[-1]['commit']['author']['date'].replace("Z", "")
    old_data = old_data.replace("T", " ")
    old = datetime.strptime(old_data, '%Y-%m-%d %H:%M:%S')
    return abs(recent - old)

cont_data = []
#get the 100 users
data = collect_data(initial_url + str(1))
people_count = 1
#print the time difference
print(get_time())
# for each variable get the desired data
for person in range(0,len(data)):
    # print(people_count)
    people_count = people_count + 1
    num_repo = get_repo(data[person]['login'])
    cont_data.append(num_repo)
# put the data into a dataframe for pretty viewing
final_data = pd.DataFrame(cont_data, columns=['User', 'Number of Repos', 'Repo Names', 'Number of Contributions'])
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(final_data)

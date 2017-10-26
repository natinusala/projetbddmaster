#!/usr/bin/python3

import sys
import requests
from time import sleep
import json
from pathlib import Path

API_URL = ""
REPO_OWNER = ""
REPO_REPO = ""
DATA = {}
OAUTH_TOKEN = ""


def call_github_api(endpoint):
    url = API_URL + endpoint
    print("Calling URL " + url)
    request = requests.get(url, headers={'Authorization': 'token ' + OAUTH_TOKEN})

    if request.status_code == 202:
        print("Data is not available yet, waiting 10s before retrying...")
        sleep(10)
        return call_github_api(endpoint)

    response = request.json()

    if ("message" in response):
        print("API Error : " + response["message"])
        print("Help can be found here : " + response["documentation_url"])
        exit()

    return response


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : create_sql.py owner repo")
        exit()

    REPO_OWNER = sys.argv[1]
    REPO_REPO = sys.argv[2]
    OUTPUT_FILE = REPO_OWNER + "-" + REPO_REPO + ".json"

    if not Path("oauth_token.txt").is_file():
        print("Please write your GitHub OAUTH Token to oauth_token.txt and try again")
        exit()

    with open('oauth_token.txt', 'r') as f:
        OAUTH_TOKEN = f.read().replace('\n', '')

    API_URL = "https://api.github.com/repos/" + REPO_OWNER + "/" + REPO_REPO

    DATA["repo"] = {"owner": REPO_OWNER, "repo": REPO_REPO, "fullname": REPO_OWNER + "/" + REPO_REPO}
    DATA["weeks"] = {}

    print("Getting data for GitHub repository "
          + REPO_OWNER + "/"
          + REPO_REPO + "...")

    print("Getting repo informations")

    informations = call_github_api("")

    DATA["repo"]["description"] = informations["description"]
    DATA["repo"]["homepage"] = informations["homepage"]
    DATA["language"] = informations["language"]

    print("Getting commits count...")

    commit_activity = call_github_api("/stats/commit_activity")

    for week in commit_activity:
        week_timestamp = week["week"]
        print("Processing week " + str(week_timestamp))

        DATA["weeks"][week_timestamp] = {}
        DATA["weeks"][week_timestamp]["commits"] = {}
        DATA["weeks"][week_timestamp]["commits"]["total"] = week["total"]

    print("Getting additions and deletions...")
    code_frequency = call_github_api("/stats/code_frequency")

    for week in code_frequency:
        week_ts = week[0]
        week_additions = week[1]
        week_deletions = week[2]

        if week_ts in DATA["weeks"]:
            print("Processing week " + str(week_ts))
            DATA["weeks"][week_ts]["commits"]["additions"] = week_additions
            DATA["weeks"][week_ts]["commits"]["deletions"] = abs(week_deletions)
        else:
            print("Skipping week " + str(week_ts) + " because it was not present in commits count data")

    print("Getting issues...")

    for week in DATA["weeks"]:
        issues_opened = call_github_api("/issues?state=opened")

        page = 1
        while len(issues_opened) > 0:
            issues_opened = call_github_api("/issues?page=" + str(page) + "state=opened")
            page = page + 1

    print("Writing output...")

    f = open(OUTPUT_FILE, "w+")

    f.write(json.dumps(DATA))

    f.close()

    print("Success !")
    print("Output file : " + OUTPUT_FILE)

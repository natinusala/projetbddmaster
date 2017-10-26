#!/usr/bin/python3

import sys
import requests
from time import sleep
import json

API_URL = ""
REPO_OWNER = ""
REPO_REPO = ""


def call_github_api(endpoint):
    url = API_URL + endpoint
    print("Calling URL " + url)
    request = requests.get(url)

    if request.status_code == 202:
        print("Data is not available yet, waiting 10s before retrying...")
        sleep(10)
        return call_github_api(endpoint)

    return request.json()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : create_sql.py owner repo")
        exit()

    REPO_OWNER = sys.argv[1]
    REPO_REPO = sys.argv[2]
    OUTPUT_FILE = REPO_OWNER + "-" + REPO_REPO + ".json"

    API_URL = "https://api.github.com/repos/" + REPO_OWNER + "/" + REPO_REPO

    # Dict ontaining data for each day
    DATA = {}
    DATA["repo"] = {"owner": REPO_OWNER, "repo": REPO_REPO, "fullname": REPO_OWNER + "/" + REPO_REPO}
    DATA["weeks"] = {}

    print("Getting data for GitHub repository "
          + REPO_OWNER + "/"
          + REPO_REPO + "...")

    # TODO Check if the repo exists or not

    print("Getting repo informations")

    informations = call_github_api("")

    if ("message" in informations):
        print("Error : " + informations["message"])
        exit()

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

    f = open(OUTPUT_FILE, "w+")

    f.write(json.dumps(DATA))

    f.close()

    print("Success !")
    print("Output file : " + OUTPUT_FILE)

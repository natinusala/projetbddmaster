#!/usr/bin/python3

import sys
import requests
from time import sleep
import json
from pathlib import Path
import datetime
import dateutil.parser
import pytz

utc = pytz.UTC

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
    DATA["repo"]["language"] = informations["language"]

    print("Getting commits count...")

    commit_activity = call_github_api("/stats/commit_activity")

    for week in commit_activity:
        week_timestamp = week["week"]
        print("Processing week " + str(week_timestamp))

        DATA["weeks"][week_timestamp] = {}
        DATA["weeks"][week_timestamp]["issues"] = {}
        DATA["weeks"][week_timestamp]["issues"]["open"] = 0
        DATA["weeks"][week_timestamp]["issues"]["closed"] = 0
        DATA["weeks"][week_timestamp]["issues"]["total"] = 0
        DATA["weeks"][week_timestamp]["pull_requests"] = {}
        DATA["weeks"][week_timestamp]["pull_requests"]["open"] = 0
        DATA["weeks"][week_timestamp]["pull_requests"]["closed"] = 0
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
            print("Skipping week " + str(week_ts) + " because it is out of range")

    print("Getting issues...")

    page = 0

    while True:  # do-while loop
        print("Getting page " + str(page))
        issues = call_github_api("/issues?page=" + str(page) + "&state=all")

        if len(issues) <= 0:
            break

        # TODO Exclude pull requests

        for issue in issues:
            print("Processing issue " + str(issue["id"]))

            opened_count = 0
            closed_count = 0

            for week in DATA["weeks"]:
                issue_created_dt = dateutil.parser.parse(issue["created_at"])
                week_dt = utc.localize(datetime.datetime.fromtimestamp(int(week)))

                if issue_created_dt <= week_dt:
                    reopened = False

                    if issue["state"] == "closed":
                        closed_at_dt = dateutil.parser.parse(issue["closed_at"])
                        if (closed_at_dt > week_dt):
                            print("Issue was not closed yet, reopening it")
                            issue["state"] = "open"
                            reopened = True

                    DATA["weeks"][week]["issues"][issue["state"]] = DATA["weeks"][week]["issues"][issue["state"]] + 1
                    DATA["weeks"][week]["issues"]["total"] = DATA["weeks"][week]["issues"]["total"] + 1

                    if issue["state"] == "open":
                        opened_count = opened_count + 1
                    else:
                        closed_count = closed_count + 1

                    if reopened:
                        reopened = False
                        issue["state"] = "closed"

            count = opened_count + closed_count
            if count == 0:
                print("Issue not added, it was probably created more than a year ago or between last sunday and today (" + str(issue_created_dt) + ")")
            else:
                print("Issue added " + str(count) + " times, " + str(opened_count) + " times as an open issue and " + str(closed_count) + " times as a closed issue")

        print("Added " + str(len(issue)) + " issues for page " + str(page))

        page = page + 1

    print("Writing output...")

    f = open(OUTPUT_FILE, "w+")

    f.write(json.dumps(DATA))

    f.close()

    print("Success !")
    print("Output file : " + OUTPUT_FILE)

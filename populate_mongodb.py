#!/usr/bin/python3

# Use this script to populate your local mongodb database using mongoimport
# It will create or complete three collections, owner_repo_weeks, owner_repo_contributors and owner_repo_infos in projet_m1 db

import json
import sys
from subprocess import call
import os


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : populate_mongodb.py owner repo")
        exit()

    OWNER = sys.argv[1]
    REPO = sys.argv[2]

    try:
        with open(OWNER + '-' + REPO + '.json', 'r') as f:
            DATA = json.load(f)
    except FileNotFoundError:
        print("Could not find " + OWNER + '-' + REPO + '.json')
        exit()

    WEEKS = []
    INFOS = []
    CONTRIBUTORS = []

    for week in DATA["weeks"]:
        mongo_week = {}

        if DATA["weeks"][week]["commits"]["total"] == 0:
            # a week with 0 commits is for a uninitialized repo and should not be added yet
            continue

        mongo_week = DATA["weeks"][week]
        mongo_week["_id"] = week

        WEEKS.append(mongo_week)

    for contributor in DATA["contributors"]:
        mongo_contributor = DATA["contributors"][contributor]
        mongo_contributor["_id"] = DATA["contributors"][contributor]["id"]
        del mongo_contributor["id"]  # it's redundant because of _id

        CONTRIBUTORS.append(mongo_contributor)

    COLLECTION_WEEKS = OWNER + '_' + REPO + '_weeks'
    JSON_WEEKS = COLLECTION_WEEKS + '.json'

    f = open(JSON_WEEKS, 'w+')
    f.write(json.dumps(WEEKS))
    f.close()

    call(["mongoimport",
          '--db', 'projet_m1',
          '--collection', COLLECTION_WEEKS,
          '--file', JSON_WEEKS,
          '--mode', 'upsert',
          '--jsonArray'])

    os.remove(JSON_WEEKS)

    INFOS = DATA["repo"]
    INFOS["_id"] = "repo_infos"  # to prevent duplicates

    COLLECTION_INFOS = OWNER + '_' + REPO + '_infos'
    JSON_INFOS = COLLECTION_INFOS + '.json'

    f = open(JSON_INFOS, 'w+')
    f.write(json.dumps(INFOS))
    f.close()

    call(["mongoimport",
          '--db', 'projet_m1',
          '--collection', COLLECTION_INFOS,
          '--file', JSON_INFOS,
          '--mode', 'upsert'])

    os.remove(JSON_INFOS)

    COLLECTION_CONTRIBUTORS = OWNER + '_' + REPO + '_contributors'
    JSON_CONTRIBUTORS = COLLECTION_CONTRIBUTORS + '.json'

    f = open(JSON_CONTRIBUTORS, 'w+')
    f.write(json.dumps(CONTRIBUTORS))
    f.close()

    call(["mongoimport",
          '--db', 'projet_m1',
          '--collection', COLLECTION_CONTRIBUTORS,
          '--file', JSON_CONTRIBUTORS,
          '--jsonArray',
          '--mode', 'upsert'])

    os.remove(JSON_CONTRIBUTORS)

    print("Success!")

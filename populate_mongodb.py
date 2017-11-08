#!/usr/bin/python3

# Use this script to populate your local mongodb database using mongoimport
# It will create or complete two collections, owner_repo_weeks and owner_repo_infos in projet_m1 db

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

    for week in DATA["weeks"]:
        mongo_week = {}

        mongo_week = DATA["weeks"][week]
        mongo_week["_id"] = week

        WEEKS.append(mongo_week)

    COLLECTION_WEEKS = OWNER + '_' + REPO + '_weeks'
    JSON_WEEKS = COLLECTION_WEEKS + '.json'

    f = open(JSON_WEEKS, 'w+')
    f.write(json.dumps(WEEKS))
    f.close()

    call(["mongoimport",
          '--db', 'projet_m1',
          '--collection', COLLECTION_WEEKS,
          '--file', JSON_WEEKS,
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
          '--jsonArray'])

    os.remove(JSON_INFOS)

    print("Success!")

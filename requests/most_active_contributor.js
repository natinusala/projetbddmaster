#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

print("Getting most active contributor")

var result = db.getCollection('libretro_RetroArch_contributors')
  .find({}, {"total_commits":1, "login":1})
  .limit(1)
  .sort({"total_commits":-1})[0];

print("User " + result.login + " (#" + result._id + ") is the most active contributor on the repo, with a total of " + result.total_commits + " commits");

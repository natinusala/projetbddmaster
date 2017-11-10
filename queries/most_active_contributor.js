#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var owner = "libretro";
var repo = "Lakka-LibreELEC";

print("Getting most active contributor for repo " + repo)

var result = db.getCollection(owner + '_' + repo + '_contributors')
  .find({}, {"total_commits":1, "login":1})
  .limit(1)
  .sort({"total_commits":-1})[0];

print("User " + result.login + " (#" + result._id + ") is the most active contributor on the repo, with a total of " + result.total_commits + " commits");

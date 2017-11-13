#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

print("Loading ranking of contributors per repository");

var repos = db.getCollection("repos_list").find().map(function(e){
  print("Processing repo " + e.owner + "/" + e.repo);
  var contributors = db.getCollection(e.owner + "_" + e.repo + "_contributors").find().sort({"total_commits":-1}).toArray();
  return {"repo":e, "ranking":contributors};
});

printjson(repos);

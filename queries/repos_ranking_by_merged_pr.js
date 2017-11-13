#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var repos = db.getCollection("repos_list").find().map(function(r){
  return {"repo": r, "merged_pull_requests": db.getCollection(r.owner + "_" + r.repo + "_weeks").find({"pull_requests.closed_merged":{$gt:0}}).sort({_id:-1}).limit(1)[0].pull_requests.closed_merged}
});

repos = repos.sort(function(a, b){return b.merged_pull_requests - a.merged_pull_requests;});

printjson(repos);

#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var user = "twinaphex";

print("Getting most active week of all times for user " + user);

var max = {
  "repo": null,
  "stats": {
    "total" : 0,
    "additions" : 0,
    "deletions" : 0,
    "week" : 0
  }
}
var repos = db.getCollection("repos_list").find().forEach(function(r)
{
  var id = db.getCollection(r.owner + "_" + r.repo + "_contributors").find({"login":user}, {"_id":1})[0]._id;
  var key = "contributors." + id + ".total";
  var weeks = db.getCollection(r.owner + "_" + r.repo + "_weeks").find({[key]:{$gt:0}}, {"contributors":1}).forEach(function(w)
  {
    if (w.contributors[id].total > max.stats.total)
    {
      max.repo = r;
      max.stats.total = w.contributors[id].total;
      max.stats.additions = w.contributors[id].additions;
      max.stats.deletions = w.contributors[id].deletions;
      max.stats.week = w._id;
    }
  });
});

printjson(max);

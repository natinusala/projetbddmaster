#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var owner = "libretro";
var repo = "RetroArch";

print("Fetching the best week for repo " + owner + "/" + repo);

var max = {
  "contributor" : null,
  "stats":{
    "additions" : 0,
    "deletions" : 0,
    "total" : 0,
    "week" : 0
  }
}

db.getCollection(owner + "_" + repo + "_weeks").find({}, {"contributors":1}).forEach(function(w)
{
  for (contributor in w.contributors)
  {
    contributor = w.contributors[contributor];
    if (contributor.total > max.stats.total)
    {
      max.contributor = contributor.contributor;
      max.stats.additions = contributor.additions;
      max.stats.deletions = contributor.deletions;
      max.stats.total = contributor.total;
      max.stats.week = w._id;
    }
  }
});

printjson(max);

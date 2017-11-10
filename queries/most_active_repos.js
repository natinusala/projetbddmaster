#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

print("Getting sorted array of most active repos");

var repos = db.getCollection("repos_list").find().map(function(e)
{
  print("   Processing repo " + e.owner + "-" + e.repo);

  var weeks = db.getCollection(e.owner + "_" + e.repo + "_weeks").find({}, {"commits":1}).map(function(e)
  {
    var score  = e.commits.total;
    print("       Score for week " + e._id + " : " + score);
    return score;
  });

  var score = weeks.reduce(function(a, b) { return a + b; })/weeks.length;

  print("     Score for repo " + e.owner + "-" + e.repo + " : " + score);
  return {"repo": e, "score": score};
});

repos = repos.sort(function(a, b)
{
  return (a.score < b.score) ? 1 : -1;
});

print("Final result : sorted array of most active repos");
print("Based on the average count of commits per week")
printjson(repos);

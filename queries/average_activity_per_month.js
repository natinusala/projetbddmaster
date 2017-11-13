#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var repos = db.getCollection("repos_list").find().map(function(e)
{
  print("Processing repo " + e.owner + " " + e.repo);
  var weeks = db.getCollection(e.owner + "_" + e.repo + "_weeks").find({}, {"commits":1}).toArray();
  var months = [];
  var count = 0;
  for (var week in weeks)
  {
      week = weeks[week];
      if (count % 4 == 0)
      {
        if (months.length != 0)
        {
          months[months.length-1].deletions /= 4;
          months[months.length-1].additions /= 4;
          months[months.length-1].total /=4;
        }

        if (weeks.length - count < 4)
          break;

        months.push(week.commits);
      }
      else
      {
        months[months.length-1].deletions += week.commits.deletions;
        months[months.length-1].additions += week.commits.additions;
        months[months.length-1].total += week.commits.total;
      }
      count++;
  }
  var activity = months.reduce(function(a, b) {
    return {"total": a.total + b.total, "deletions" : a.deletions + b.deletions, "additions": a.additions + b.additions};
  });

  activity.total = activity.total /= months.length;
  activity.deletions = activity.deletions /= months.length;
  activity.additions = activity.additions /= months.length;

  return {"repo": e, "average_activity_per_month" : activity};
});

printjson(repos);

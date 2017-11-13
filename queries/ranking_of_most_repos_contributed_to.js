#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var mapping = {};

db.getCollection("repos_list").find().forEach(function(r)
{
  print("Processing repo " + r.owner + "/" + r.repo);

  db.getCollection(r.owner + "_" + r.repo + "_contributors").find().forEach(function(c){
    print("   User " + c.login + " contributed to repo " + r.owner + "/" + r.repo);

    if (mapping[c.login] != undefined)
      mapping[c.login]++;
    else
      mapping[c.login] = 1;
  });
});

var keysSorted = Object.keys(mapping).sort(function(a, b){return mapping[b]-mapping[a];})

for (key in keysSorted)
{
  keysSorted[key] = {"name": keysSorted[key], "contributed_repos": mapping[keysSorted[key]]};
}

printjson(keysSorted);

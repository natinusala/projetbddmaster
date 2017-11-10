#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var login = "Kivutar";

print("Getting all repos for user " + login)

var list = []

db.getCollection("repos_list").find().forEach(function(e)
{
  var id = db.getCollection(e.owner + '_' + e.repo + '_contributors')
    .find({"login":login}, {"_id":1})[0];

  if (id != undefined)
  {
    list.push(e);
  }
});

printjson(list);

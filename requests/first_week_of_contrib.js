#!/usr/bin/mongo

conn = new Mongo();
db = conn.getDB("projet_m1");

var login = "natinusala";

print("Searching first week of contributions for user " + login)

var id = db.getCollection('libretro_RetroArch_contributors')
  .find({"login":login}, {"id":1})[0]._id;

print("Found ID : " + id);

var key = "contributors." + id + ".total";

var result = db.getCollection('libretro_RetroArch_weeks')
  .find({[key]:{$gt:0}}, {_id:1})
  .limit(1)
  .sort({_id:1})[0]._id;

print("Found week " + result);

var date = new Date(result * 1000);
print("Result : " + date.toUTCString());

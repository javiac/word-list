import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.test
db.name
print(db)
print('hola')
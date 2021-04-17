import pymongo
import uuid
import datetime
import pprint

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
print(client.plytix.list_collection_names())
pprint.pprint(client.plytix.words.find_one({'value':'bbb'}))
result = client.plytix.words.insert_many([{'value': 'bbb', 'order':1, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()}])

words = client.plytix.words.find()

for word in words:
    print(word);
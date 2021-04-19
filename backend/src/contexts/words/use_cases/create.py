# coding=utf-8

import pymongo
import json
import datetime
            

def create(word):
    client = pymongo.MongoClient("localhost", 27017)
    collection = client.plytix.words

    words = []

    word['createdAt'] = datetime.datetime.now()
    word['updatedAt'] = datetime.datetime.now()
    word['order'] = -1

    collection.insert_one(word)

    index = 0 
    for word in collection.find({}).sort('order', 1):
      collection.update_one({'_id': word['_id']}, {'$set': {'order': index}})
      index+=1

    result = collection.find({}).sort('order', 1)
    for word in result:
        words.append(word)
      

    return words

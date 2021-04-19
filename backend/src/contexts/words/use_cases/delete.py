# coding=utf-8

import pymongo
from bson import ObjectId

def delete(wordId):
    client = pymongo.MongoClient("localhost", 27017)
    collection = client.plytix.words

    words = []

    collection.delete_one({ "_id": ObjectId(wordId)}) 
    index = 0 
    for word in collection.find({}).sort('order', 1):
      collection.update_one({'_id': word['_id']}, {'$set': {'order': index}})
      index+=1
    result = collection.find({}).sort('order', 1)
    for word in result:
        words.append(word)

    return words

# coding=utf-8

import pymongo
from bson.objectid import ObjectId
import datetime

def update(id, word):
    client = pymongo.MongoClient("localhost", 27017)
    collection = client.plytix.words

    collection.update_one({'_id': ObjectId(id)}, {'$set': {
      'value': word['value'],
      'updatedAt': datetime.datetime.now()
    }})
    result = collection.find({}).sort('order', 1)

    words = []
    for word in result:
      words.append(word)

    return words

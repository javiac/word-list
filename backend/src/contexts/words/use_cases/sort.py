# coding=utf-8

import pymongo

def sort(sorting_changes):
  client = pymongo.MongoClient("localhost", 27017)
  collection = client.plytix.words

  for sorting_change in sorting_changes:
    previous_index = sorting_change['previousIndex']
    current_index = sorting_change['currentIndex']
    words = []
    
    if previous_index < current_index:
      min_index = previous_index
      max_index = current_index
    elif previous_index > current_index:
      min_index = current_index
      max_index = previous_index

    result = collection.find({"order": { "$gte": min_index, "$lte": max_index}}).sort("order", 1)
    for word in result:
      words.append(word)

    if previous_index < current_index:
      index = -1
      for word in words:
        collection.update_one({ "_id": word["_id"] }, { "$set": { "order": words[index]["order"] } }) 
        index+=1
    elif previous_index > current_index:
      index = 1
      for word in words:
        collection.update_one({ "_id": word["_id"] }, { "$set": { "order": words[index%len(words)]["order"] } }) 
        index+=1

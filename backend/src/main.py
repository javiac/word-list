# coding=utf-8

import pymongo
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from bson.json_util import dumps
import json

# creating the Flask application
app = Flask(__name__,
            static_url_path='', 
            static_folder='./../public/dist/frontend',
            template_folder='./../public/dist/frontend')
            
CORS(app)

@app.route('/words')
def get_words():
    client = pymongo.MongoClient("localhost", 27017)
    words = []
    for word in client.plytix.words.find({}).sort('order', 1):
      words.append(word)

    return dumps(words)

@app.route('/words/sort', methods=['POST'])
def save_sorting():
  client = pymongo.MongoClient("localhost", 27017)
  collection = client.plytix.words;

  sorting_changes = json.loads(request.data)

  for sorting_change in sorting_changes:
    previous_index = sorting_change['previousIndex']
    current_index = sorting_change['currentIndex']

    #collection.update_one({ "order": previous_index }, { "$set": { "order": current_index } }) 
    print(previous_index, '->', current_index)
    words = []
    
    if previous_index < current_index:
      result = collection.find({"order": { "$gte": previous_index, "$lte": current_index}})
      for word in result:
        words.append(word)

    elif previous_index > current_index:
      words = collection.find({"order": { "$gte": current_index, "$lte": previous_index}})
      for word in result:
        words.append(word)

    if previous_index < current_index:
      index = -1
      for word in words:
        print(word)
        collection.update_one({ "value": word["value"] }, { "$set": { "order": words[index]["order"] } }) 
        index+=1
      #for index in range(previous_index+1, current_index):
       # collection.update_one({ "order": index }, { "$set": { "order": index - 1 } }) 
        #print(index, '->', index - 1)
    elif previous_index > current_index:
      for word in words:
        print(word)
      #for index in range(current_index, previous_index-1):
       # collection.update_one({ "order": index }, { "$set": { "order": index + 1 } }) 
        #print(index, '->', index + 1)
    
  return dumps({'success':True})

@app.route('/')
def root():
  return send_from_directory('./../public/dist/frontend', 'index.html')

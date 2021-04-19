# coding=utf-8

import pymongo
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from bson.json_util import dumps
import json
from bson.code import Code

app = Flask(__name__,
            static_url_path='', 
            static_folder='./../public/dist/frontend',
            template_folder='./../public/dist/frontend')
            
CORS(app)

@app.route('/words')
def get_words():
    client = pymongo.MongoClient("localhost", 27017)
    collection = client.plytix.words
    words = []

    if request.args.get('searchAnagram') is None:
      result = collection.find({}).sort('order', 1)
    else:
      pipeline = [
        { "$addFields":
          {
            "isAnagram":
                { "$function":
                  {
                      "body": Code("""
                          function(value, searchValue) {
                            function unaccent(str) {
                              const map = {
                                'a' : 'á|à|ã|â|ä|À|Á|Ã|Â|Ä',
                                'e' : 'é|è|ê|ë|É|È|Ê|Ë',
                                'i' : 'í|ì|î|ï|Í|Ì|Î|Ï',
                                'o' : 'ó|ò|ô|õ|ö|Ó|Ò|Ô|Õ|Ö',
                                'u' : 'ú|ù|û|ü|Ú|Ù|Û|Ü',
                              };

                              for (var pattern in map) {
                                str = str.replace(new RegExp(map[pattern], 'g'), pattern);
                              }

                              return str;
                            }

                            return unaccent(value).toLowerCase().split('').sort().join().replace(/,/g, '') == unaccent(searchValue).toLowerCase().split('').sort().join().replace(/,/g, '')
                      }
                      """),
                      "args": [ "$value",  request.args.get('searchAnagram')],
                      "lang": "js"
                  }
                },
          }
        },
        {
          "$match":{
            "isAnagram": True
          }
        }
      ]

      result = collection.aggregate(pipeline)

    for word in result:
        words.append(word)

    return dumps(words)

@app.route('/words/sort', methods=['POST'])
def save_sorting():
  client = pymongo.MongoClient("localhost", 27017)
  collection = client.plytix.words

  sorting_changes = json.loads(request.data)

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
    
  return dumps({'success':True})

@app.route('/words/search')

@app.route('/')
def root():
  return send_from_directory('./../public/dist/frontend', 'index.html')

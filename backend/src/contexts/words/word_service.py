import logging
from typing import Dict
from bson import ObjectId
import datetime


class WordService():

    def __init__(self, db_client, db_name) -> None:
        self.db = db_client[db_name]

    def get(self, searchText: str):
        collection = self.db.words

        words = []

        if searchText is None:
            result = collection.find({}).sort('order', 1)
        else:
            pipeline = [
                {"$addFields":
                 {
                     "isAnagram":
                     {"$function":
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
                          "args": ["$value",  searchText],
                          "lang": "js"
                      }
                      },
                 }
                 },
                {
                    "$match": {
                        "isAnagram": True
                    }
                }
            ]

            result = collection.aggregate(pipeline)

        for word in result:
            words.append(word)

        return words

    def delete(self, word_id):
        collection = self.db.words

        words = []

        collection.delete_one({"_id": ObjectId(word_id)})
        index = 0
        for word in collection.find({}).sort('order', 1):
            collection.update_one({'_id': word['_id']}, {'$set': {'order': index}})
        index += 1

        return self.get_all()

    def create(self, word):
        collection = self.db.words

        word['createdAt'] = datetime.datetime.now()
        word['updatedAt'] = datetime.datetime.now()
        word['order'] = 0

        collection.update_many({}, {'$inc': {'order': 1}})
        collection.insert_one(word)

        words = []

        return self.get_all()

    def sort(self, sorting_changes):
        collection = self.db.words

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

            result = collection.find({"order": {"$gte": min_index, "$lte": max_index}}).sort("order", 1)

            for word in result:
                words.append(word)

            if previous_index < current_index:
                index = -1
                for word in words:
                    collection.update_one({"_id": word["_id"]}, {
                        "$set": {"order": words[index]["order"]}})
                    index += 1
            elif previous_index > current_index:
                index = 1
                for word in words:
                    collection.update_one({"_id": word["_id"]}, {"$set": {"order": words[index % len(words)]["order"]}})
                    index += 1

    def update(self, id, word):
        collection = self.db.words

        collection.update_one({'_id': ObjectId(id)}, {'$set': {
            'value': word['value'],
            'updatedAt': datetime.datetime.now()
        }})

        return self.get_all()

    def get_all(self):
        collection = self.db.words
        result = collection.find({}).sort('order', 1)

        words = []
        for word in result:
            words.append(word)

        return words

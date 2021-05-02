import logging
from typing import Dict
from bson import ObjectId
import datetime
import unidecode


class WordService():

    def __init__(self, db_client, db_name) -> None:
        self.db = db_client[db_name]

    def get(self, searchText: str):
        collection = self.db.words

        words = []

        if searchText is None:
            result = collection.find({}).sort('order', 1)
        else:
            result = collection.find({'sortedValue': "".join(sorted(unidecode.unidecode(searchText.lower())))}).sort('order', 1)

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
        word['sortedValue'] = "".join(sorted(unidecode.unidecode(word['value'].lower())))

        collection.update_many({}, {'$inc': {'order': 1}})
        collection.insert_one(word)

        words = []

        return self.get_all()

    def sort(self, sorting_changes):
        collection = self.db.words

        for sorting_change in sorting_changes:
            previous_index = sorting_change['previousIndex']
            current_index = sorting_change['currentIndex']

            word_to_move = collection.find_one({'order': previous_index})

            if previous_index < current_index:
                collection.update_many({'order': {'$lte': current_index, '$gt': previous_index}}, {'$inc': {'order': -1}})
            elif previous_index > current_index:
                collection.update_many({'order': {'$gte': current_index, '$lt': previous_index}}, {'$inc': {'order': 1}})

            collection.update_one({'_id': word_to_move['_id']}, {'$set': {'order': current_index}})

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

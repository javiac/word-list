import pymongo
import uuid
import datetime
import pprint
import unidecode

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

client.plytix.words.delete_many({})

words = [
    {'value': 'Inglaterra', 'order': 0, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Conservadora', 'order': 1, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'conversadora', 'order': 2, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Irónicamente', 'order': 3, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Escandalizar', 'order': 4, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'zascandilear', 'order': 5, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Enfriamiento', 'order': 6, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Alegan', 'order': 7, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Ángela', 'order': 8, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Riesgo', 'order': 9, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Sergio', 'order': 10, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Amor', 'order': 11, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Roma', 'order': 12, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Nacionalista', 'order': 13, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'altisonancia', 'order': 14, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Frase', 'order': 15, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'fresa', 'order': 16, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'Integrarla', 'order': 17, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
    {'value': 'refinamiento', 'order': 18, 'createdAt': datetime.datetime.now(), 'updatedAt': datetime.datetime.now()},
]

for word in words:
    word['sortedValue'] = "".join(sorted(unidecode.unidecode(word['value'].lower())))

result = client.plytix.words.insert_many(words)

print('Inserted ', len(result.inserted_ids))

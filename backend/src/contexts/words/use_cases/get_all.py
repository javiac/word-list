# coding=utf-8

import pymongo
from bson.code import Code
import datetime

def get_all(searchText):
    client = pymongo.MongoClient("localhost", 27017)
    collection = client.plytix.words

    words = []

    if searchText is None:
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
                        "args": [ "$value",  searchText],
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

    return words

# coding=utf-8

import pymongo
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# creating the Flask application
app = Flask(__name__,
            static_url_path='', 
            static_folder='./../public/dist/frontend',
            template_folder='./../public/dist/frontend')
            
CORS(app)

@app.route('/words')
def get_words():
    client = pymongo.MongoClient("localhost", 27017)
    db = client.test
    db.name
    print(db)
    print('hola')
    return jsonify([{'value': 'word1', 'order':2}])

@app.route('/')
def root():
  return send_from_directory('./../public/dist/frontend', 'index.html')

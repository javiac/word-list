# coding=utf-8

import pymongo
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from bson.json_util import dumps
import json
from src.contexts.words.use_cases import get_all, delete, create, sort, update
from .containers import Container
import sys

container = Container()
container.init_resources()
container.wire(modules=[sys.modules[__name__]])

app = Flask(__name__,
            static_url_path='',
            static_folder='./../public/dist/frontend',
            template_folder='./../public/dist/frontend')

CORS(app)


@app.route('/words', methods=['GET', 'DELETE', 'POST'])
def words():
    words = []
    if(request.method == 'GET'):
        words = get_all(request.args.get('searchAnagram'))
    elif request.method == 'DELETE':
        words = delete(request.args.get('id'))
    elif request.method == 'POST':
        words = create(json.loads(request.data))

    return dumps(words)


@app.route('/words/sort', methods=['POST'])
def save_sorting():
    sort(json.loads(request.data))
    return dumps({'success': True})


@app.route('/words/<id>', methods=['POST'])
def update_word(id):
    words = update(id, json.loads(request.data))
    return dumps(words)


@app.route('/')
def root():
    return send_from_directory('./../public/dist/frontend', 'index.html')

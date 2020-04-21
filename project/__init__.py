# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import hashlib
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from google.cloud import datastore

app = Flask(__name__)
CORS(app)
datastore_client = datastore.Client()
kind_note = 'note'
kind_note_title = 'title'
kind_note_text = 'note_text'
kind_note_modified_date = 'last_modified_date'
kind_note_created_date = 'created_date'
kind_note_user = 'user'


@app.route('/json', methods=['GET'])
def simple_endpoint():
    testJson = {'one': 1, 'two': 2, 'three': 3}
    return app.response_class(
        response=json.dumps(testJson),
        status=200,
        mimetype='application/json'
    )


@app.route('/note/get', methods=['POST'])
def get_note():
    get_json = request.get_json()
    title_search_string = get_json.get(kind_note_title)
    user = get_json.get(kind_note_user)
    query = datastore_client.query(kind=kind_note)
    entities = list(query.add_filter(kind_note_user, '=', user).fetch())
    matches = []

    for entity in entities:
        entity_title = entity[kind_note_title]
        entity_note = entity[kind_note_text]
        entity_last_modified = entity[kind_note_modified_date]
        if title_search_string is None:
            matches.append({kind_note_title: entity_title,
                            kind_note_text: entity_note,
                            kind_note_modified_date: entity_last_modified})
        # search logic
        elif title_search_string.lower() in entity_title.lower():
            matches.append({kind_note_title: entity_title,
                            kind_note_text: entity_note})

    json_response = {"matches": matches}
    return jsonify(json_response)


def md5_hex(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


@app.route('/note', methods=['POST'])
def store_note():
    note_json = request.get_json()

    # format checks
    if len(note_json.get(kind_note_title)) >= 500:
        return error_response("Title has too many characters")
    if note_json.get(kind_note_title) is None:
        return error_response("Title cannot be null")

    # check if note already exists - create or update
    query = datastore_client.query(kind=kind_note)
    pre_existing_note = list(query.add_filter(kind_note_title, '=', note_json.get(kind_note_title)).fetch())
    already_exists = False
    if len(pre_existing_note) > 0:
        if md5_hex(pre_existing_note[0][kind_note_title]) == md5_hex(note_json.get(kind_note_title)):
            already_exists = True

    # create/ update entity
    entity = datastore.Entity(
        key=datastore_client.key(kind_note, md5_hex(note_json.get(kind_note_title))),
        # tuple with single value
        exclude_from_indexes=(kind_note_text,))
    current_time = datetime.datetime.now()
    entity.update({
        kind_note_title: note_json.get(kind_note_title),
        kind_note_text: note_json.get(kind_note_text),
        kind_note_user: note_json.get(kind_note_user),
        kind_note_modified_date: current_time,
        kind_note_created_date: pre_existing_note[0][kind_note_created_date] if already_exists else current_time
    })
    datastore_client.put(entity)
    return success_response()


@app.route('/note', methods=['DELETE'])
def delete_note():
    datastore_client.delete(datastore_client.key(kind_note, md5_hex(request.get_json().get(kind_note_title))))
    return success_response()


def success_response():
    return app.response_class(
        status=200,
        mimetype='application/json')


def error_response(string):
    return app.response_class(
        response=json.dumps(string),
        status=500)


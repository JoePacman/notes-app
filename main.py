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
from flask import Flask, json, request, jsonify
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()


@app.route('/')
def nothing_here():
    return 'nothing mapped'


@app.route('/json', methods=['GET'])
def return_json():
    testJson = {'one': 1, 'two' : 2, 'three': 3}
    return app.response_class(
        response=json.dumps(testJson),
        status=200,
        mimetype='application/json'
    )


@app.route('/note', methods=['POST'])
def store_note():
    json = request.get_json()
    title = json.get('title')
    note = json.get('note')
    print("Title: " + title)

    if not check_length(title, 100):
        return error_response("Title has too many characters")

    entity = datastore.Entity(key=datastore_client.key(title))
    entity.update({
        'note': note,
        'createdDate': datetime.datetime.now(),
        'modifiedDate': datetime.datetime.now()
    })
    print(entity)
    #datastore_client.put(entity)
    return success_response()


def check_length(string, size):
    return True if len(string) <= size else False


def success_response():
    return app.response_class(
        status=200,
        mimetype='application/json')


def error_response(string):
    return app.response_class(
        response=json.dumps(string),
        status=500)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]

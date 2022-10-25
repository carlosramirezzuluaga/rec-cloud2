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
import random

from flask import Flask, render_template, request

# [START gae_python38_datastore_store_and_fetch_times]
# [START gae_python3_datastore_store_and_fetch_times]
from google.cloud import datastore

datastore_client = datastore.Client()

# [END gae_python3_datastore_store_and_fetch_times]
# [END gae_python38_datastore_store_and_fetch_times]
app = Flask(__name__)


# [START gae_python38_datastore_store_and_fetch_times]
# [START gae_python3_datastore_store_and_fetch_times]
def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times
# [END gae_python3_datastore_store_and_fetch_times]
# [END gae_python38_datastore_store_and_fetch_times]

def store_student( document, first_name, last_name, major, birthyear):
    entity= datastore.Entity(key=datastore_client.key('student'))
    entity.update({
        'document': document,
        'first_name': first_name,
        'last_name': last_name,
        'major': major,
        'birthyear': birthyear
    })
    datastore_client.put(entity)

def fetch_students(limit):
    query= datastore_client.query(kind='student')
    students=query.fetch(limit=limit)
    print(students)
    return students


@app.route('/insert',methods = ['POST', 'GET'] )
def insert():
    if request.method == 'POST':
        result = request.form
        json_result = dict(result)
        print(json_result)
        store_student( json_result['document'],
                       json_result['first_name'],
                       json_result['last_name'],
                       'Computer Science',
                       json_result['birthyear'])
        students=fetch_students(12)
        return render_template("index.html", result=result, students=students)
    return render_template('insert.html')


# [START gae_python38_datastore_render_times]
# [START gae_python3_datastore_render_times]
@app.route('/')
def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now(tz=datetime.timezone.utc))

    # Fetch the most recent 1 access times from Datastore.
    times = fetch_times(1)

    first_names=['Isaac','Albert','Robert','Enrico','Fiodor','Emanuel','Carl']
    last_names=['Newton','Einstein','Hook','Tesla','Mendeliev','Kant','Sagan']


    store_student(random.randint(0,101000000),random.choice(first_names),random.choice(last_names),'Physics',random.randint(0,2000))
    students=fetch_students(12)

    return render_template(
        'index.html', times=times, students=students)
# [END gae_python3_datastore_render_times]
# [END gae_python38_datastore_render_times]


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

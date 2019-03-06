# Copyright 2019 Jacques Supcik
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

import flask
from io import BytesIO
from .envelopes import Envelopes
from .clas import Class

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def main():

    data = flask.request.get_json()
    e = Envelopes()
    for i in data:
        e.addClass(Class(
            name = i['name'],
            clas = i['clas'],
            table = i['table'],
            number = i['number']
        ))

    output = BytesIO()
    e.makePdf(output)
    response = flask.make_response(output.getvalue())
    output.close()

    response.headers.set('Content-Disposition', 'attachment', filename='envelopes.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

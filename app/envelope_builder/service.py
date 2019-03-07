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

"""This module implements the REST service"""


from io import BytesIO

import flask
import PyPDF2

from .clas import Clas
from .envelopes import Envelopes

# pylint: disable=invalid-name
app = flask.Flask(__name__)


@app.route('/check')
def check():
    """Check if service is working"""

    e = Envelopes()
    e.add_class(Clas(
        name='Prix Python',
        clas='Epreuve 1',
        table='Grand Prix',
        number=10
    ))
    output = BytesIO()
    e.make_pdf(output)
    output.seek(0)
    pdf = PyPDF2.PdfFileReader(output)
    info = pdf.getDocumentInfo()
    output.close()

    if info is None:
        raise Exception("ERROR")

    return "OK\n"

@app.route('/pdf', methods=['POST'])
def main():
    """Main endpoint of the service"""

    data = flask.request.get_json()
    e = Envelopes()
    for i in data:
        e.add_class(Clas(
            name=i['name'],
            clas=i['clas'],
            table=i['table'],
            number=i['number']
        ))

    output = BytesIO()
    e.make_pdf(output)
    response = flask.make_response(output.getvalue())
    output.close()

    response.headers.set('Content-Disposition',
                         'attachment', filename='envelopes.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

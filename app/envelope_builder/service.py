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

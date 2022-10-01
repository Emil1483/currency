import json
import sys

from flask import Flask, request
from flask_talisman import Talisman

sys.path.insert(0, '../')

from app.utils.catch_errors import catch_errors
from app.utils.helpers import path, read_json, write_json

app = Flask(__name__)
Talisman(app)

@app.route('/', methods=['GET'])
@catch_errors
def home():
    return 'hello world 👏'

@app.route('/write', methods=['POST'])
@catch_errors
def write():
    write_json('data/file.json', request.json, mpath=path(__file__))
    return request.json

@app.route('/read', methods=['GET'])
@catch_errors
def read():
    return json.dumps(read_json('data/file.json', mpath=path(__file__)))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

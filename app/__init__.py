import sys

from flask import Flask, request

sys.path.insert(0, '../')

from app.utils.catch_errors import catch_errors
from app.utils.helpers import path, write_json

app = Flask(__name__)

@app.route('/')
@catch_errors
def home():
    return 'hello world 🎅'

@app.route('/write', methods=['POST'])
@catch_errors
def write():
    mpath = path(__file__)
    write_json('file.json', request.json, mpath=f'{mpath}/data')
    return request.json

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

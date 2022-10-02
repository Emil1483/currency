import sys

from dotenv import load_dotenv
from flask import Flask
from flask_talisman import Talisman

sys.path.insert(0, '../')

from app.utils.catch_errors import catch_errors
from app.utils.helpers import env_is_true
from app.utils.xe import fetch_rates

load_dotenv()
prod = env_is_true('PROD')

app = Flask(__name__)
if prod: Talisman(app)

@app.route('/', methods=['GET'])
@catch_errors
def home():
    return 'Hello World 📦'

@app.route('/rates', methods=['GET'])
@catch_errors
def rates():
    return fetch_rates()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

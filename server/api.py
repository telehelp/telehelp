import time
from flask import Flask
from middlewares import login_required #Should maybe be properly relative

app = Flask(__name__)

@app.route('/time')
def current_time():
    return {'time': time.time()}

@app.route('/test', methods=["GET"])
@login_required
def test():
    return {'entry': 'test'}


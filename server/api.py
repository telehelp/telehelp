import time
from flask import Flask, request
from middlewares import login_required #Should maybe be properly relative
import json

app = Flask(__name__)

@app.route('/time')
def current_time():
    return {'time': time.time()}

@app.route('/test', methods=["GET"])
@login_required
def test():
    return {'entry': 'test'}

@app.route('/register', methods=["POST"])
def register():
    if request.json:
        creds = json.dumps(request.json)
        print(creds)
        return {'type': 'success'}
    return {'type': 'failure'}
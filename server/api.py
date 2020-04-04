import time
from flask import Flask, request
import requests
import os
from databaseIntegration import *
import pandas as pd
import json
from middlewares import login_required #Should maybe be properly relative

app = Flask(__name__)

API_USERNAME = os.environ.get('API_USERNAME')
API_PASSWORD = os.environ.get('API_PASSWORD')

databaseName = 'telehelp.db'
helpers = getHelpers(databaseName)
helper = list(helpers['phone'])[0]
customers = getCustomers(databaseName)
customer = list(customers['phone'])[0]


app = Flask(__name__, static_folder='../client/build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/time')
def current_time():
    return {'time': time.time()}

@app.route('/call')
def call():
	#from_sender = request.forms.get("from")
	auth = (API_USERNAME, API_PASSWORD)

	payload = '{"ivr": "https://46elks.com/static/sound/testcall.mp3"}'

	fields = {
	    'from': '+46766861551',
	    'to': helper,
	    'voice_start': payload}

	response = requests.post(
	    "https://api.46elks.com/a1/calls",
	    data=fields,
	    auth=auth
	    )

	print(response.text)
	return

@app.route('/handleNumberInput', methods = ['POST'])
def handleNumberInput():
	print(request.form.get("result"))
	number = request.form.get("result")
	payload = {"play": "https://46elks.com/static/sound/testcall.mp3"}
	return payload

@app.route('/receiveCall',methods = ['POST'])
def receiveCall():
	from_sender = request.form.get("from")
	print(from_sender)
	auth = (API_USERNAME, API_PASSWORD)

	#payload = '{"play": "https://46elks.com/static/sound/testcall.mp3"}'
	payload = {"ivr": "https://46elks.com/static/sound/testcall.mp3", "digits": 1, "next": "https://9a56e1aa.ngrok.io/handleNumberInput"}
	return json.dumps(payload)

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


import time
from flask import Flask, request
import requests
import os
from databaseIntegration import *
import pandas as pd
import json

app = Flask(__name__)

@app.route('/time')
def current_time():
    return {'time': time.time()}

API_USERNAME = os.environ.get('API_USERNAME')
API_PASSWORD = os.environ.get('API_PASSWORD')

databaseName = 'telehelp.db'
helpers = getHelpers(databaseName)
print(helpers['phone'])
helper = list(helpers['phone'])[0]
customers = getCustomers(databaseName)
customer = list(customers['phone'])[0]
print(customer)


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


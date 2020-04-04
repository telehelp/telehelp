import time
from flask import Flask, request
import requests
import os
from databaseIntegration import *
import pandas as pd
import json
from middlewares import login_required #Should maybe be properly relative
from schema import Schema, And, Use, Optional, Regex

app = Flask(__name__, static_folder='../client/build', static_url_path='/')

API_USERNAME = os.environ.get('API_USERNAME')
API_PASSWORD = os.environ.get('API_PASSWORD')
BASE_URL = "https://9a56e1aa.ngrok.io"
DATABASE = 'telehelp.db'

#helpers = getHelpers(DATABASE)
#helper = list(helpers['phone'])[0]
#customers = getCustomers(DATABASE)
#customer = list(customers['phone'])[0]

reg_schema = Schema({'helperName': str, 'zipCode':  Regex("^[0-9]{5}$"), 'phoneNumber': Regex("^(\d|\+){1}\d{9,12}$"), 'terms': bool })  

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

@app.route('/postcodeInput', methods = ['POST'])
def postcodeInput():
	zipcode = request.form.get("result")
	phone = request.form.get("from")
	flag = savePostcodeToDatabase(DATABASE, phone, zipcode, 'customer')
	return flag

@app.route('/handleNumberInput', methods = ['POST'])
def handleNumberInput():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		payload = {"play": "https://46elks.com/static/sound/testcall.mp3"}
		return json.dumps(payload)
	elif number == 2:
		print('Write your zipcode')
		payload = {"ivr": "https://46elks.com/static/sound/testcall.mp3", "digits": 5, "next": BASE_URL+"/postcodeInput"}
		return json.dumps(payload)


@app.route('/receiveCall',methods = ['POST'])
def receiveCall():
	from_sender = request.form.get("from")
	print(from_sender)
	auth = (API_USERNAME, API_PASSWORD)

	#payload = '{"play": "https://46elks.com/static/sound/testcall.mp3"}'
	#data = {'data': 'info.mp3'}
	#response = requests.post(BASE_URL+"/media",data=data)
	payload = {"ivr": "https://files.telehelp.se/info.mp3", "digits": 1, "next": BASE_URL+"/handleNumberInput"}
	return json.dumps(payload)

# @app.route('/media/*')
# def media():
# 	return app.send_static_file('/media/*')

@app.route('/test', methods=["GET"])
@login_required
def test():
    return {'entry': 'test'}

@app.route('/register', methods=["POST"])
def register():
    if request.json:
        creds = json.dumps(request.json)
        print(request.json)
        try:
            reg_schema.validate(request.json)
            print("valid data")
            return {'type': 'success'}
        except schema.SchemaUnexpectedTypeError as err:
            #print(err.message)
            return {'type': 'failure'}
    return {'type': 'failure'}


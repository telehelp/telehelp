import time
from flask import Flask, request
import requests
import os
from databaseIntegration import *
import pandas as pd
from middlewares import login_required #Should maybe be properly relative
import json

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

	json = '{"ivr": "https://46elks.com/static/sound/testcall.mp3","digits": 1,"next": {"connect":"%s"}}'%customer
	print(json)

	fields = {
	    'from': '+46766861551',
	    'to': helper,
	    'voice_start': json}

	response = requests.post(
	    "https://api.46elks.com/a1/calls",
	    data=fields,
	    auth=auth
	    )

	print(response.text)



# @app.post('/smsDemo')
# def demo_start():
#     from_sender = request.forms.get("from")
#     response = requests.post(
#     'https://api.46elks.com/a1/conversations',
#     auth = (config.elks_user, config.elks_pass),
#     data = {
#             "to": from_sender,
#             "message":startingPoint(),
#             "token":id_generator(),
#             "reply_url": currentServer+"smsStart"
#             }
#     )
#     print(response)

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


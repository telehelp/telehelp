import time
from flask import Flask
import requests
import os
from databaseIntegration import *
import pandas as pd

app = Flask(__name__, static_folder='../client/build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

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
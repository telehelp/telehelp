import time
from flask import Flask, request
import requests
import os
from databaseIntegration import *
import pandas as pd
import json
from middlewares import login_required #Should maybe be properly relative
from schema import Schema, And, Use, Optional, Regex
from zipcode_utils import *
#from text2speech_utils import generateCustomSoundByte

app = Flask(__name__, static_folder='../client/build', static_url_path='/')

dev = False

if dev:
	BASE_URL = "https://59408f3f.ngrok.io"
	elkNumber = '+46766862446'
	API_USERNAME = os.environ.get('API_USERNAME_DEV')
	API_PASSWORD = os.environ.get('API_PASSWORD_DEV')
else:
	BASE_URL = "https://telehelp.se"
	elkNumber = '+46766861551'
	API_USERNAME = os.environ.get('API_USERNAME')
	API_PASSWORD = os.environ.get('API_PASSWORD')
DATABASE = 'telehelp.db'
DATABASE_KEY = os.environ.get('DATABASE_KEY')
ZIPDATA = 'SE.txt'
mediaFolder = '../../media'
callHistory = {}

reg_schema = Schema({'helperName': str, 'zipCode':  Regex("^[0-9]{5}$"), 'phoneNumber': Regex("^(\d|\+){1}\d{9,12}$"), 'terms': bool })
location_dict, district_dict = readZipCodeData(ZIPDATA)


@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/time')
def current_time():
	return {'time': time.time()}

@app.route('/call', methods = ['POST'])
def call():
	#from_sender = request.forms.get("from")
	callId = request.form.get("callid")
	helperNumber = callHistory[callId]['helperNumber']
	closestHelpers = callHistory[callId]['closestHelpers']
	auth = (API_USERNAME, API_PASSWORD)

	payload = {"play": "https://files.telehelp.se/hjalte.mp3",
				"next": {"play": "https://files.telehelp.se/tryck.mp3",
				"next": {"play": "https://files.telehelp.se/1.mp3",
				"next": {"play": "https://files.telehelp.se/tryck.mp3",
				"next": {"ivr": "https://files.telehelp.se/2.mp3",
				"1": BASE_URL+"/connectUsers", "2":BASE_URL+"/call"}}}}}


	print(closestHelpers[helperNumber])
	print(elkNumber)
	fields = {
		'from': elkNumber,
		'to': closestHelpers[helperNumber],
		'voice_start': json.dumps(payload)}

	helperNumber += 1
	callHistory[callId]['helperNumber'] = helperNumber
	response = requests.post(
		"https://api.46elks.com/a1/calls",
		data=fields,
		auth=auth
		)

	print(response.text)
	return ""


@app.route('/checkZipcode', methods = ['POST'])
def checkZipcode():
	zipcode = request.form.get("result")
	callId = request.form.get("callid")
	callHistory[callId]['zipcode'] = zipcode

	phone = request.form.get("from")
	district = getDistrict(int(zipcode), district_dict)
	#generateCustomSoundByte(district, district+'.mp3', mediaFolder)
	payload = {"play": "https://files.telehelp.se/du_befinner.mp3",
				"next": {"play": "https://files.telehelp.se/stammer_det.mp3",
				"next": {"play": "https://files.telehelp.se/tryck.mp3",
				"next": {"play": "https://files.telehelp.se/1.mp3",
				"next": {"play": "https://files.telehelp.se/andra_postnr.mp3",
				"next": {"play": "https://files.telehelp.se/tryck.mp3",
				"next": {"ivr": "https://files.telehelp.se/2.mp3",
				"1": BASE_URL+'/postcodeInput', 
				"2": {"play": "https://files.telehelp.se/post_nr.mp3", "skippable":"true", 
					"next": {"ivr": "https://files.telehelp.se/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"} }}}}}}}}

	return json.dumps(payload)

@app.route('/postcodeInput', methods = ['POST'])
def postcodeInput():
	callId = request.form.get("callid")
	zipcode = callHistory[callId]['zipcode']
	phone = request.form.get("from")
	currentCustomer = phone
	district = getDistrict(int(zipcode), district_dict)
	# TODO: Add sound if zipcode is invalid (n/a)
	saveCustomerToDatabase(DATABASE, DATABASE_KEY, phone, zipcode, district)
	closestHelpers = fetchHelper(DATABASE, DATABASE_KEY, district, zipcode, location_dict)
	callHistory[callId]['closestHelpers'] = closestHelpers
	callHistory[callId]['currentCustomer'] = currentCustomer

	if closestHelpers is None:
		# TODO: Fix this sound clip
		payload = {"play": "https://files.telehelp.se/finns_ingen.mp3"}
		return json.dumps(payload)
	else:

		# TODO: add "en volontär ringer upp dig snart"
		payload = {"play": "https://files.telehelp.se/ringer_tillbaka.mp3", "skippable":"true", 
						"next": BASE_URL+"/call"}
		helperNumber = 0
		callHistory[callId]['helperNumber'] = helperNumber

		return json.dumps(payload)

@app.route('/connectUsers', methods = ['POST'])
def connectUsers():
	callId = request.form.get("callid")
	currentCustomer = callHistory[callId]['currentCustomer']
	payload = {"connect":currentCustomer, "callerid": elkNumber, "timeout":"15"}
	return json.dumps(payload)

@app.route('/handleReturningUser', methods = ['POST'])
def handleReturningUser():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		# TODO: fetch customer from database
		payload = {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}
		return json.dumps(payload)

	if number == 2:
		# TODO: fetch customer from database
		payload = {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}
		return json.dumps(payload)
	
	if number == 3:
		payload = {"play": "https://files.telehelp.se/avreg_confirmed.mp3", "next": BASE_URL+"/removeCustomer"}
		return json.dumps(payload)

@app.route('/removeHelper', methods = ['POST'])
def removeHelper():
	from_sender = request.form.get("from")
	deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, 'helper')
	return ""

@app.route('/removeCustomer', methods = ['POST'])
def removeCustomer():
	from_sender = request.form.get("from")
	deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, 'customer')
	return ""

@app.route('/handleReturningHelper', methods = ['POST'])
def handleReturningHelper():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		# TODO: fetch customer from database
		payload = {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}
		return json.dumps(payload)
	
	elif number == 2:
		payload = {"play": "https://files.telehelp.se/avreg_confirmed.mp3", "next": BASE_URL+"/removeCustomer"}
		return json.dumps(payload)


@app.route('/handleNumberInput', methods = ['POST'])
def handleNumberInput():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		print('Write your zipcode')
		payload = {"play": "https://files.telehelp.se/post_nr.mp3", "skippable":"true", 
					"next": {"ivr": "https://files.telehelp.se/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"}}

		return json.dumps(payload)

	elif number == 2:
		# TODO: this is broken, fix it
		payload = {BASE_URL+'/receiveCall'}
		return json.dumps(payload)

	elif number == 3:
		payload = payload = {"play": "https://files.telehelp.se/6.mp3",
				"next": {"play":"https://files.telehelp.se/igen.mp3",
				"next": {"play":"https://files.telehelp.se/om_inte.mp3"}}}
		return json.dumps(payload)


@app.route('/receiveCall',methods = ['POST'])
def receiveCall():
	callId = request.form.get("callid")
	callHistory[callId] = {}
	from_sender = request.form.get("from")
	print(from_sender)
	auth = (API_USERNAME, API_PASSWORD)
	#from_sender = request.form.get("from")

	# For registered helpers
	if userExists(DATABASE, DATABASE_KEY, from_sender, 'helper'):
		# TODO: Fix sound
		print("Registered helper")
		payload = {"play":"https://files.telehelp.se/registrerad_volontar.mp3",
				"next":{"play":"https://files.telehelp.se/ring_upp_riskgrupp.mp3", 
			   "next":{"play":"https://files.telehelp.se/tryck.mp3",
			   "next":{"play":"https://files.telehelp.se/1.mp3",
			   "next":{"play": "https://files.telehelp.se/avreg.mp3",
			   "next":{"play": "https://files.telehelp.se/tryck.mp3",
			   "next":{"ivr": "https://files.telehelp.se/2.mp3", "digits": 1, "next":BASE_URL+"/handleReturningHelper"} }}}}}}
		return json.dumps(payload)

	# For registered customers
	elif userExists(DATABASE, DATABASE_KEY, from_sender, 'customer'):
		payload = {"play":"https://files.telehelp.se/behover_hjalp.mp3", 
				"next":{"play":"https://files.telehelp.se/kontakta.mp3",
				"next":{"play":"https://files.telehelp.se/igen.mp3",
			   "next":{"play":"https://files.telehelp.se/tryck.mp3",
			   "next":{"play":"https://files.telehelp.se/1.mp3",
			   "next":{"play":"https://files.telehelp.se/nagon_annan.mp3",
			   "next":{"play": "https://files.telehelp.se/tryck.mp3",
			   "next":{"play": "https://files.telehelp.se/2.mp3",
			   "next":{"play": "https://files.telehelp.se/avreg.mp3",
			   "next":{"play": "https://files.telehelp.se/tryck.mp3",
			   "next":{"ivr": "https://files.telehelp.se/3.mp3", "digits": 1, "next":BASE_URL+"/handleReturningUser"} }}}}}}}}}}
		return json.dumps(payload)

	# New customer
	payload = {"play": "https://files.telehelp.se/info.mp3", "skippable":"true", 
				"next":{"play":"https://files.telehelp.se/behover_hjalp.mp3", 
				"next":{"play":"https://files.telehelp.se/1.mp3",
				"next":{"play":"https://files.telehelp.se/info_igen.mp3",
				"next":{"ivr":"https://files.telehelp.se/2.mp3",
				"digits": 1, "2":BASE_URL+"/receiveCall", "next": BASE_URL+"/handleNumberInput"}}}}}
	return json.dumps(payload)

@app.route('/test', methods=["GET"])
@login_required
def test():
	return {'entry': 'test'}

@app.route('/register', methods=["POST"])
def register():
	if request.json:
		print(request.json)
		try:
			reg_schema.validate(request.json)
			print("valid data")
			city = getDistrict(int(request.json['zipCode']), district_dict)
			if city == "n/a":
				return {'type': 'failure', 'message': 'Invalid Zip'}
			if request.json['phoneNumber'][0] == '0':
				request.json['phoneNumber'] = '+46' + request.json['phoneNumber'][1:]
			if userExists(DATABASE, DATABASE_KEY, request.json['phoneNumber'], 'helper'):
				return {'type': 'failure', 'message': 'User already exists'}
			saveHelperToDatabase(DATABASE, DATABASE_KEY, request.json['helperName'], request.json['phoneNumber'], request.json['zipCode'], city)
			return {'type': 'success'}
		except Exception as err:
			print(err)
			print('Invalid Data')
			return {'type': 'failure'}
	return {'type': 'failure'}

@app.route('/getVolunteerLocations', methods=["GET"])
def getVolunteerLocations():
    # Fetch all ZIP codes for volunteer users:
    query = "SELECT zipcode FROM user_helpers"
    zip_pd_dict = fetchData(DATABASE, DATABASE_KEY, query, params=None)
    zip_list = zip_pd_dict.values.tolist()

    # Use ZIPs to get GPS coordinates (lat, long):
    latlongs = []

    print(zip_list)
    for zip in zip_list:
        latlongs.append(getLatLong(zip[0], location_dict))

    payload = {'coordinates' : latlongs }
    return json.dumps(payload)


import time
from flask import Flask, request, session
from flask_session import Session
import requests
import os
from .databaseIntegration import *
import pandas as pd
import json
from .middlewares import login_required
from schema import Schema, And, Use, Optional, Regex
from .zipcode_utils import *
import logging
import time
import secrets

#from text2speech_utils import generateCustomSoundByte

app = Flask(__name__, static_folder='../client/build', static_url_path='/')
SESSION_TYPE = 'redis'
SECRET_KEY = os.getenv('SECRET_KEY')
app.config.from_object(__name__)
#app.config["SECRET_KEY"] = os.getenv('SECRET')
Session(app)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.FileHandler('flask.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

BASE_URL = os.getenv('BASE_URL')
ELK_NUMBER = os.getenv('ELK_NUMBER')
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')
DATABASE = os.getenv('DATABASE')

DATABASE_KEY = os.getenv('DATABASE_KEY')
ZIPDATA = 'SE.txt'
MEDIA_FOLDER = '../../media'
#callHistory = {}

VERIFICATION_EXPIRY_TIME = 120_000_000_000 # Nanoseconds

reg_schema = Schema({'helperName': str, 'zipCode':  Regex("^[0-9]{5}$"), 'phoneNumber': Regex("^(\d|\+){1}\d{9,12}$"), 'terms': bool })
verification_schema = Schema({'verificationCode':  Regex("^[0-9]{6}$"), 'number': Regex("^(\d|\+){1}\d{9,12}$")})
location_dict, district_dict = readZipCodeData(ZIPDATA)

def canonicalize_number(phone_number):
	if phone_number[0] == '0':
		phone_number = '+46' + phone_number[1:]
	return phone_number

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/call', methods = ['POST'])
def call():
	from_sender = request.form.get("from")
	callId = request.form.get("callid")

	helperNumber = readCallHistory(DATABASE, DATABASE_KEY, callId, 'helper_number')
	closestHelpers = json.loads(readCallHistory(DATABASE, DATABASE_KEY, callId, 'closest_helpers'))
	print(closestHelpers)
	auth = (API_USERNAME, API_PASSWORD)

	print(closestHelpers[helperNumber])
	print(ELK_NUMBER)
	writeActiveCustomer(DATABASE, DATABASE_KEY, closestHelpers[helperNumber], from_sender)
	fields = {
		'from': ELK_NUMBER,
		'to': closestHelpers[helperNumber],
		'voice_start': {"play": "https://files.telehelp.se/hjalte.mp3",
				"next": {"play": "https://files.telehelp.se/1.mp3",
				"next": {"ivr": "https://files.telehelp.se/2.mp3",
				"1": BASE_URL+"/connectUsers", "2":BASE_URL+"/call"}}}}

	helperNumber += 1
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'helper_number', helperNumber)
	#callHistory[callId]['helperNumber'] = helperNumber
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
	print('zipcode: ', zipcode)
	print('callId: ', callId)
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'zipcode', zipcode)
	print('Added to database')
	#callHistory[callId]['zipcode'] = zipcode

	phone = request.form.get("from")
	district = getDistrict(int(zipcode), district_dict)
	#generateCustomSoundByte(district, district+'.mp3', MEDIA_FOLDER)
	return {"play": "https://files.telehelp.se/du_befinner.mp3",
				"next": {"play": "https://files.telehelp.se/stammer_det.mp3",
				"next": {"play": "https://files.telehelp.se/1.mp3",
				"next": {"play": "https://files.telehelp.se/andra_postnr.mp3",
				"next": {"ivr": "https://files.telehelp.se/2.mp3",
				"1": BASE_URL+'/postcodeInput', 
				"2": {"play": "https://files.telehelp.se/post_nr.mp3", "skippable":"true", 
					"next": {"ivr": "https://files.telehelp.se/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"} }}}}}}


@app.route('/postcodeInput', methods = ['POST'])
def postcodeInput():
	callId = request.form.get("callid")
	zipcode = readCallHistory(DATABASE, DATABASE_KEY, callId, 'zipcode')
	phone = request.form.get("from")
	currentCustomer = phone
	district = getDistrict(int(zipcode), district_dict)
	# TODO: Add sound if zipcode is invalid (n/a)
	print('zipcode: ', zipcode)
	saveCustomerToDatabase(DATABASE, DATABASE_KEY, phone, str(zipcode), district)
	closestHelpers = fetchHelper(DATABASE, DATABASE_KEY, district, zipcode, location_dict)
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'closest_helpers', json.dumps(closestHelpers))
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'current_customer', currentCustomer)
	#callHistory[callId]['closestHelpers'] = closestHelpers
	#callHistory[callId]['currentCustomer'] = currentCustomer

	if closestHelpers is None:
		# TODO: Fix this sound clip
		return {"play": "https://files.telehelp.se/finns_ingen.mp3"}
	else:

		# TODO: add "en volontär ringer upp dig snart"
		helperNumber = 0
		addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'helper_number', helperNumber)
		#callHistory[callId]['helperNumber'] = helperNumber

		return {"play": "https://files.telehelp.se/ringer_tillbaka.mp3", "skippable":"true", 
						"next": BASE_URL+"/call"}

@app.route('/connectUsers', methods = ['POST'])
def connectUsers():
	print('Connecting users')
	callId = request.form.get("callid")
	fromUser = request.form.get("from")
	print('fromUser: ', fromUser)
	helperPhone = request.form.get("to")
	print('helper: ', helperPhone)
	currentCustomer = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)
	print('customer:', currentCustomer)
	return {"connect":currentCustomer, "callerid": ELK_NUMBER, "timeout":"15"}

@app.route('/handleReturningUser', methods = ['POST'])
def handleReturningUser():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		# TODO: fetch customer from database
		return {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}

	if number == 2:
		# TODO: fetch customer from database
		return {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}
	
	if number == 3:
		return {"play": "https://files.telehelp.se/avreg_confirmed.mp3", "next": BASE_URL+"/removeCustomer"}

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
		return {"play": "https://files.telehelp.se/du_kopplas.mp3", "skippable":"true"}
	
	elif number == 2:
		return {"play": "https://files.telehelp.se/avreg_confirmed.mp3", "next": BASE_URL+"/removeCustomer"}


@app.route('/handleNumberInput', methods = ['POST'])
def handleNumberInput():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	print('number: ', number)
	if number == 1:
		print('Write your zipcode')
		return {"play": "https://files.telehelp.se/post_nr.mp3", "skippable":"true", 
					"next": {"ivr": "https://files.telehelp.se/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"}}

	elif number == 2:
		# TODO: this is broken, fix it
		return {BASE_URL+'/receiveCall'}

	elif number == 3:
		return {"play": "https://files.telehelp.se/6.mp3",
				"next": {"play":"https://files.telehelp.se/igen.mp3",
				"next": {"play":"https://files.telehelp.se/om_inte.mp3"}}}

@app.route('/receiveCall',methods = ['POST'])
def receiveCall():
	callId = request.form.get("callid")
	createNewCallHistory(DATABASE, DATABASE_KEY, callId)
	#callHistory[callId] = {}
	from_sender = request.form.get("from")
	print(from_sender)
	auth = (API_USERNAME, API_PASSWORD)
	#from_sender = request.form.get("from")

	# For registered helpers
	if userExists(DATABASE, DATABASE_KEY, from_sender, 'helper'):
		# TODO: Fix sound
		print("Registered helper")
		return {"play":"https://files.telehelp.se/registrerad_volontar.mp3",
				"next":{"play":"https://files.telehelp.se/ring_upp_riskgrupp.mp3", 
			   "next":{"play":"https://files.telehelp.se/1.mp3",
			   "next":{"play": "https://files.telehelp.se/avreg.mp3",
			   "next":{"ivr": "https://files.telehelp.se/2.mp3", "digits": 1, "next":BASE_URL+"/handleReturningHelper"} }}}}

	# For registered customers
	elif userExists(DATABASE, DATABASE_KEY, from_sender, 'customer'):
		return {"play":"https://files.telehelp.se/behover_hjalp.mp3", 
				"next":{"play":"https://files.telehelp.se/kontakta.mp3",
				"next":{"play":"https://files.telehelp.se/igen.mp3",
			   "next":{"play":"https://files.telehelp.se/1.mp3",
			   "next":{"play":"https://files.telehelp.se/nagon_annan.mp3",
			   "next":{"play": "https://files.telehelp.se/2.mp3",
			   "next":{"play": "https://files.telehelp.se/avreg.mp3",
			   "next":{"ivr": "https://files.telehelp.se/3.mp3", "digits": 1, "next":BASE_URL+"/handleReturningUser"} }}}}}}}

	# New customer
	return {"play": "https://files.telehelp.se/info.mp3", "skippable":"true", 
				"next":{"play":"https://files.telehelp.se/behover_hjalp.mp3", 
				"next":{"play":"https://files.telehelp.se/1.mp3",
				"next":{"play":"https://files.telehelp.se/info_igen.mp3",
				"next":{"ivr":"https://files.telehelp.se/2.mp3",
				"digits": 1, "2":BASE_URL+"/receiveCall", "next": BASE_URL+"/handleNumberInput"}}}}}

@app.route('/test', methods=["GET"])
@login_required
def test():
	return {'entry': 'test'}

@app.route('/register', methods=["POST"])
def register():
	if request.json:
		data = request.json
		print(data)
		try:
			log.info("Trying")
			reg_schema.validate(data)
			zipcode = int(data['zipCode'])
			phone_number = canonicalize_number(data['phoneNumber'])
			name = data['helperName']
			city = getDistrict(zipcode, district_dict)
			if city == "n/a":
				return {'type': 'failure', 'message': 'Invalid Zip'}
			if userExists(DATABASE, DATABASE_KEY, phone_number, 'helper'):
				return {'type': 'failure', 'message': 'User already exists'}
			ts = time.time_ns()
			## TODO SEND THIS BY SMS
			code = secrets.randbelow(1_000_000)
			print(code)
			## ==========
			session[phone_number] = {"phoneNumber": phone_number, "zipCode": zipcode, "name": name, "city": city, "timestamp": ts, "code": code}
			return {'type': 'success'}
		except Exception as err:
			log.exception('Got invalid data when registering user {request.json}', err)
		return {'type': 'failure'}
	return {'type': 'failure'}

@app.route('/verify', methods=["POST"])
def verify():
	if request.json:
		data = request.json
		print(data)
		try:
			verification_schema.validate(data)
			phone_number = canonicalize_number(data['number'])
			code = int(data['verificationCode'])
			if phone_number in session \
				and time.time_ns() - session[phone_number]["timestamp"] < VERIFICATION_EXPIRY_TIME \
				and code == session[phone_number]["code"]:

				name = session[phone_number]["name"]
				zipcode = session[phone_number]["zipCode"]
				city = session[phone_number]["city"]

				log.info(f"Saving helper to database {name}, {phone_number}, {zipcode}, {city}")
				saveHelperToDatabase(DATABASE, DATABASE_KEY, name, phone_number, zipcode, city)
				return {'type': 'success'}
			else:
				return {'type': 'failure'}
		except Exception as err:
			log.exception('Got invalid data when verifying user', request, err)
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

	return {'coordinates' : latlongs }


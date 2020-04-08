import time

from flask import Flask, request, session, redirect
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import requests
import os
from .databaseIntegration import *
import pandas as pd
import json
from .middlewares import login_required
from .schemas import VERIFICATION_SCHEMA, REGISTRATION_SCHEMA
from .zipcode_utils import *
import logging
import time
import secrets
import string

#from text2speech_utils import generateCustomSoundByte

app = Flask(__name__, static_folder='../client/build', static_url_path='/')

SESSION_TYPE = 'redis'
SECRET_KEY = os.getenv('SECRET_KEY')
app.config.from_object(__name__)
Session(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["15 per minute", "1 per second"],
)

@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"

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


VERIFICATION_EXPIRY_TIME = 5 * 60 * 1_000_000_000 # 5 minutes


location_dict, district_dict = readZipCodeData(ZIPDATA)

def canonicalize_number(phone_number):
	if phone_number[0] == '0':
		phone_number = '+46' + phone_number[1:]
	return phone_number

@app.route('/')
def index():
	return app.send_static_file('index.html')


@app.route('/time')
def current_time():
	return {'time': time.time()}

#------------------------------ PHONE API ----------------------------------------------------


@app.route('/receiveCall',methods = ['POST'])
def receiveCall():
	callId = request.form.get("callid")
	createNewCallHistory(DATABASE, DATABASE_KEY, callId)
	from_sender = request.form.get("from")
	print(from_sender)
	auth = (API_USERNAME, API_PASSWORD)

	# For registered helpers
	if userExists(DATABASE, DATABASE_KEY, from_sender, 'helper'):
		print("Registered helper")
		activeCustomer = readActiveCustomer(DATABASE, DATABASE_KEY, from_sender)
		print(activeCustomer)
		if activeCustomer is None:
			payload = {"ivr": filePath+"/hjalper_ingen.mp3", "skippable":"true", "digits": 1,
			"1":{"play": filePath+"/avreg_confirmed.mp3", "next": BASE_URL+"/removeHelper"}}
		else:
			payload = {"ivr":filePath+"/registrerad_volontar.mp3", "digits": 1, 
						"next":BASE_URL+"/handleReturningHelper"}
		return json.dumps(payload)

	# For registered customers
	elif userExists(DATABASE, DATABASE_KEY, from_sender, 'customer'):
		print("Registered customer")
		#TODO: Add name.mp3 from generated file
		payload = {"play":filePath+"/behover_hjalp.mp3", 
			   "next":{"ivr":filePath+"/pratade_sist.mp3", 
			   "digits": 1,"next":BASE_URL+"/handleReturningCustomer"} }
		return json.dumps(payload)

	# New customer
	payload = {"ivr": filePath+"/info.mp3", "skippable":"true", 
				"digits": 1, "2":BASE_URL+"/receiveCall", "next": BASE_URL+"/handleNumberInput"}
	return json.dumps(payload)


@app.route('/hangup', methods = ['POST'])
def hangup():

	print('hangup')
	return ""

@app.route('/handleReturningHelper', methods = ['POST'])
def handleReturningHelper():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		helperPhone = request.form.get("from")
		activeCustomer = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)

		payload = {"ivr": filePath+"/du_kopplas.mp3", "skippable":"true",
					"next":BASE_URL+"/callExistingCustomer"}
		return json.dumps(payload)
	
	elif number == 2:
		payload = {"play": filePath+"/avreg_confirmed.mp3", "next": BASE_URL+"/removeHelper"}
		return json.dumps(payload)


@app.route('/callExistingCustomer', methods = ['POST'])
def callExistingCustomer():
	helperPhone = request.form.get("from")
	customerPhone = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)
	payload = {
			  "connect": customerPhone,
			  "callerid": elkNumber
			}
	return json.dumps(payload)

@app.route('/removeHelper', methods = ['POST'])
def removeHelper():
	from_sender = request.form.get("from")
	deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, 'helper')
	return ""

@app.route('/handleReturningCustomer', methods = ['POST'])
def handleReturningCustomer():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:

		payload = {"play": filePath+"/du_kopplas.mp3", "skippable":"true", "next": BASE_URL+"/callExistingHelper"}
		return json.dumps(payload)

	if number == 2:
		payload = {"play": filePath+"/vi_letar.mp3", "skippable":"true", "next": BASE_URL+"/postcodeInput"}
		return json.dumps(payload)


	if number == 3:
		payload = {"play": filePath+"/avreg_confirmed.mp3", "next": BASE_URL+"/removeCustomer"}
		return json.dumps(payload)

	return ""

@app.route('/callExistingHelper', methods = ['POST'])
def callExistingHelper():
	customerPhone = request.form.get("from")
	helperPhone = readActiveHelper(DATABASE, DATABASE_KEY, customerPhone)
	payload = {
			  "connect": helperPhone,
			  "callerid": elkNumber
			}
	return json.dumps(payload)



@app.route('/postcodeInput', methods = ['POST'])
def postcodeInput():
	callId = request.form.get("callid")
	phone = request.form.get("from")
	# TODO: Add sound if zipcode is invalid (n/a)
	zipcode = readZipcodeFromDatabase(DATABASE, DATABASE_KEY, phone, 'customer')
	district = getDistrict(int(zipcode), district_dict)
	print('zipcode: ', zipcode)

	closestHelpers = fetchHelper(DATABASE, DATABASE_KEY, district, zipcode, location_dict)
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'closest_helpers', json.dumps(closestHelpers))
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'current_customer', phone)


	if closestHelpers is None:
		# TODO: Fix this sound clip

		payload = {"play": filePath+"/finns_ingen.mp3"}
		return json.dumps(payload)
	else:

		payload = {"play": filePath+"/ringer_tillbaka.mp3", "skippable":"true", 
						"next": BASE_URL+"/call/0/%s/%s"%(callId, phone)}
		helperNumber = 0
		addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'helper_number', helperNumber)
		return json.dumps(payload)


@app.route('/call/<int:helperIndex>/<string:customerCallId>/<string:customerPhone>', methods = ['POST'])
def call(helperIndex, customerCallId, customerPhone):
	print('helperIndex:', helperIndex)
	callId = request.form.get("callid")

	print('Customer callId: ', customerCallId)


	closestHelpers = json.loads(readCallHistory(DATABASE, DATABASE_KEY, customerCallId, 'closest_helpers'))
	print('closest helpers: ', closestHelpers)

	auth = (API_USERNAME, API_PASSWORD)

	if helperIndex >= len(closestHelpers):
		return redirect('/callBackToCustomer/%s'%customerPhone)


	# TODO: Handle if call is not picked up
	payload = {"ivr": filePath+"/hjalte.mp3", "timeout":"30", "whenhangup": BASE_URL+"/call/%s/%s/%s"%(str(helperIndex+1), customerCallId, customerPhone),
				"1": BASE_URL+"/connectUsers", "2":BASE_URL+"/call/%s/%s/%s"%(str(helperIndex+1), customerCallId, customerPhone)}


	print(closestHelpers[helperIndex])
	print(elkNumber)
	writeActiveCustomer(DATABASE, DATABASE_KEY, closestHelpers[helperIndex], customerPhone)
	print("Calling: ", closestHelpers[helperIndex])
	fields = {
		'from': elkNumber,
		'to': closestHelpers[helperIndex],
		'voice_start': json.dumps(payload)}

	response = requests.post(
		"https://api.46elks.com/a1/calls",
		data=fields,
		auth=auth
		)

	# print(json.loads(response.text))
	# state = json.loads(response.text)["state"]
	# print('state: ', state)
	# result = request.form.get("result")
	# print('result', result)

	print(response.text)
	return ""

@app.route('/callBackToCustomer/<string:customerPhone>', methods = ['POST', 'GET'])
def callBackToCustomer(customerPhone):

	print('No one found')
	auth = (API_USERNAME, API_PASSWORD)
	payload = {"play": filePath+"/ingen_hittad.mp3"}

	fields = {
		'from': elkNumber,
		'to': customerPhone,
		'voice_start': json.dumps(payload)}

	response = requests.post(
		"https://api.46elks.com/a1/calls",
		data=fields,
		auth=auth)


	return ""

@app.route('/removeCustomer', methods = ['POST'])
def removeCustomer():
	from_sender = request.form.get("from")
	deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, 'customer')
	return ""

@app.route('/handleNumberInput', methods = ['POST'])
def handleNumberInput():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	print('number: ', number)
	if number == 1:
		print('Write your zipcode')

		payload = {"play": filePath+"/post_nr.mp3", 
					"next": {"ivr": filePath+"/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"}}

		return json.dumps(payload)


@app.route('/checkZipcode', methods = ['POST'])
def checkZipcode():
	zipcode = request.form.get("result")
	callId = request.form.get("callid")
	print('zipcode: ', zipcode)
	print('callId: ', callId)
	addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'zipcode', zipcode)
	print('Added to zipcode to call history database')

	phone = request.form.get("from")
	currentCustomer = phone
	district = getDistrict(int(zipcode), district_dict)
	# TODO: Add sound if zipcode is invalid (n/a)
	print('zipcode: ', zipcode)
	saveCustomerToDatabase(DATABASE, DATABASE_KEY, phone, str(zipcode), district)


	# TODO: add district file
	payload = {"play": filePath+"/du_befinner.mp3",
				"next": {"ivr": filePath+"/stammer_det.mp3",
				"1": BASE_URL+'/postcodeInput', 
				"2": {"play": filePath+"/post_nr.mp3", "skippable":"true", 
					"next": {"ivr": filePath+"/bep.mp3", "digits": 5, 
					"next": BASE_URL+"/checkZipcode"} }}}

	return json.dumps(payload)

@app.route('/connectUsers', methods = ['POST'])
def connectUsers():

	helperPhone = request.form.get("to")
	print('helper: ', helperPhone)
	callId = request.form.get("callid")
	customerPhone = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)

	print('Saving customer -> helper connection to database')
	writeActiveHelper(DATABASE, DATABASE_KEY, customerPhone, helperPhone)
	print('Connecting users')

	print('customer:', customerPhone)
	payload = {"connect":customerPhone, "callerid": elkNumber, "timeout":"15"}
	return json.dumps(payload)

#-----------------------------------------------------------------------------------------------



@app.route('/test', methods=["GET"])
@login_required
def test():
	return {'entry': 'test'}

@app.route('/register', methods=['POST'])
def register():
	data = request.json
	if REGISTRATION_SCHEMA.is_valid(data):
		validated = REGISTRATION_SCHEMA.validate(data)

		city = getDistrict(validated['zipCode'], district_dict)
		phone_number = canonicalize_number(validated['phoneNumber'])

		if city == 'n/a':
			return {'type': 'failure', 'message': 'Invalid zip'}
		if userExists(DATABASE, DATABASE_KEY, phone_number, 'helper'):
			return {'type': 'failure', 'message': 'User already exists'}
		
		## ========== TODO SEND THIS BY SMS
		code = ''.join(secrets.choice(string.digits) for _ in range(6))
		print(code)
		## ==========

		session[phone_number] = {"zipCode": validated['zipCode'], "name": validated['helperName'], 'city': city, 'timestamp': time.time_ns(), 'code': code}
		return {'type': 'success'}
	return {'type': 'failure'}

@app.route('/verify', methods=["POST"])
def verify():
	data = request.json
	if VERIFICATION_SCHEMA.is_valid(data):
		validated = VERIFICATION_SCHEMA.validate(data)
		phone_number = canonicalize_number(validated['number'])
		code = validated['verificationCode']
		if phone_number in session \
			and time.time_ns() - session[phone_number]["timestamp"] < VERIFICATION_EXPIRY_TIME \
			and code == session[phone_number]['code']:

			sess = session[phone_number]

			name = sess['name']
			zipcode = sess['zipCode']
			city = sess['city']

			log.info(f'Saving helper to database {name}, {phone_number}, {zipcode}, {city}')
			saveHelperToDatabase(DATABASE, DATABASE_KEY, name, phone_number, zipcode, city)
			return {'type': 'success'}
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


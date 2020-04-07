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

dev = True
if dev:
	BASE_URL = "http://4628548d.ngrok.io"
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
filePath = 'https://files.telehelp.se/new'
#callHistory = {}

reg_schema = Schema({'helperName': str, 'zipCode':  Regex("^[0-9]{5}$"), 'phoneNumber': Regex("^(\d|\+){1}\d{9,12}$"), 'terms': bool })
location_dict, district_dict = readZipCodeData(ZIPDATA)


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
			   "digits": 1, "next":BASE_URL+"/handleReturningCustomer"} }
		return json.dumps(payload)

	# New customer
	payload = {"ivr": filePath+"/info.mp3", "skippable":"true", 
				"digits": 1, "2":BASE_URL+"/receiveCall", "next": BASE_URL+"/handleNumberInput"}
	return json.dumps(payload)

@app.route('/handleReturningHelper', methods = ['POST'])
def handleReturningHelper():
	print(request.form.get("result"))
	number = int(request.form.get("result"))
	if number == 1:
		helperPhone = request.form.get("from")
		activeCustomer = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)
		# This helper does not have an active customer
		
		# The helper gets connected to its active customer
		#else:
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
	# TODO: Remove active_helper from customer database
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
						"next": BASE_URL+"/call"}
		helperNumber = 0
		addCallHistoryToDB(DATABASE, DATABASE_KEY, callId, 'helper_number', helperNumber)
		return json.dumps(payload)

@app.route('/call', methods = ['POST'])
def call():
	from_sender = request.form.get("from")
	callId = request.form.get("callid")

	helperNumber = readCallHistory(DATABASE, DATABASE_KEY, callId, 'helper_number')
	closestHelpers = json.loads(readCallHistory(DATABASE, DATABASE_KEY, callId, 'closest_helpers'))
	print(closestHelpers)
	auth = (API_USERNAME, API_PASSWORD)

	# TODO: Handle when user hangs up
	# TODO: Handle if call is not picked up
	# TODO: Handle when end of helper list is reached
	payload = {"ivr": filePath+"/hjalte.mp3",
				"1": BASE_URL+"/connectUsers", "2":BASE_URL+"/call"}


	print(closestHelpers[helperNumber])
	print(elkNumber)
	writeActiveCustomer(DATABASE, DATABASE_KEY, closestHelpers[helperNumber], from_sender)
	fields = {
		'from': elkNumber,
		'to': closestHelpers[helperNumber],
		'voice_start': json.dumps(payload)}

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

@app.route('/removeCustomer', methods = ['POST'])
def removeCustomer():
	# TODO: Remove active_helper from customer database
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
	#callHistory[callId]['zipcode'] = zipcode
	#generateCustomSoundByte(district, district+'.mp3', mediaFolder)
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


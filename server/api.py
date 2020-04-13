import json
import logging
import os
import random
import secrets
import socket
import string
import time
import urllib.parse

import pandas as pd
import requests
from flask import abort
from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_session import Session

from .databaseIntegration import createNewCallHistory
from .databaseIntegration import deleteFromDatabase
from .databaseIntegration import fetchData
from .databaseIntegration import fetchHelper
from .databaseIntegration import readActiveCustomer
from .databaseIntegration import readActiveHelper
from .databaseIntegration import readCallHistory
from .databaseIntegration import readNameByNumber
from .databaseIntegration import readZipcodeFromDatabase
from .databaseIntegration import saveCustomerToDatabase
from .databaseIntegration import saveHelperToDatabase
from .databaseIntegration import userExists
from .databaseIntegration import writeActiveCustomer
from .databaseIntegration import writeActiveHelper
from .databaseIntegration import writeCallHistory
from .schemas import REGISTRATION_SCHEMA
from .schemas import VERIFICATION_SCHEMA
from .text2speech_utils import generateNameSoundByte
from .zipcode_utils import getCity
from .zipcode_utils import getDistanceApart
from .zipcode_utils import getDistrict
from .zipcode_utils import getLatLong
from .zipcode_utils import readZipCodeData

app = Flask(__name__, static_folder="../client/build", static_url_path="/")

SESSION_TYPE = "redis"
SECRET_KEY = os.getenv("SECRET_KEY")
app.config.from_object(__name__)
Session(app)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.FileHandler("flask.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
startTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
log.info(f"New log entry {startTime}")

BASE_URL = os.getenv("BASE_URL")
ELK_NUMBER = os.getenv("ELK_NUMBER")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
DATABASE = os.getenv("DATABASE")
DATABASE_KEY = os.getenv("DATABASE_KEY")


def checkEnv(envVar, envStr):
    if envVar is None:
        print(f"Warning! An environmental variable is not set {envStr}")
        log.info(f"Warning! An environmental variable is not set {envStr}")


# Checks if the environmental variables are set
checkEnv(BASE_URL, "BASE_URL")
checkEnv(ELK_NUMBER, "ELK_NUMBER")
checkEnv(API_USERNAME, "API_USERNAME")
checkEnv(API_PASSWORD, "API_PASSWORD")
checkEnv(DATABASE, "DATABASE")
checkEnv(DATABASE_KEY, "DATABASE_KEY")
checkEnv(SECRET_KEY, "SECRET_KEY")

ZIPDATA = "SE.txt"
MEDIA_FOLDER = "media"
MEDIA_URL = "https://media.telehelp.se/sv"
ELK_BASE = "https://api.46elks.com"
TRUSTED_PROXY = ["127.0.0.1"]
ELK_USER_AGENT = "46elks/0.2"
ELK_URL = "api.46elks.com"

VERIFICATION_EXPIRY_TIME = 5 * 60  # 5 minutes

location_dict, district_dict, city_dict = readZipCodeData(ZIPDATA)

print("Site phone number: " + ELK_NUMBER)


def canonicalize_number(phone_number):
    if phone_number[0] == "0":
        phone_number = "+46" + phone_number[1:]
    return phone_number


# Checks that header field User Agent and ip address.
def checkRequest(request, agent, white_url):
    white_ip = socket.getaddrinfo(white_url, 443)[0][-1][0]
    if "X-Forwarded-For" in request.headers:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0]
        if "," in remote_addr:
            remote_addr = remote_addr.split(",")[0]
    else:
        remote_addr = request.remote_addr or "untrackable"
    if "User-Agent" in request.headers:
        userAgent = request.headers.getlist("User-Agent")[0]
        if userAgent != agent or remote_addr != white_ip:
            print(
                f"Invalid user connecting to 46 ELK endpoint with User-Agent: {userAgent} from ip: {remote_addr}"
            )
            log.info(
                f"Invalid user connecting to 46 ELK endpoint with User-Agent: {userAgent} from ip: {remote_addr}"
            )
            abort(403)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/time")
def current_time():
    return {"time": time.time()}


# ------------------------------ PHONE API ----------------------------------------------------


@app.route("/receiveCall", methods=["POST"])
def receiveCall():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    callId = request.form.get("callid")
    createNewCallHistory(DATABASE, DATABASE_KEY, callId)
    from_sender = request.form.get("from")
    print(from_sender)

    # For registered helpers
    if userExists(DATABASE, DATABASE_KEY, from_sender, "helper"):
        print("Registered helper")
        activeCustomer = readActiveCustomer(DATABASE, DATABASE_KEY, from_sender)
        print(activeCustomer)
        if activeCustomer is None:
            payload = {
                "ivr": MEDIA_URL + "/ivr/hjalper_ingen.mp3",
                "skippable": "true",
                "digits": 1,
                "2": BASE_URL + "/support",
                "1": {"play": MEDIA_URL + "/ivr/avreg_confirmed.mp3", "next": BASE_URL + "/removeHelper",},
                "next": BASE_URL + "/receiveCall",
            }
        else:
            payload = {
                "ivr": MEDIA_URL + "/ivr/registrerad_volontar.mp3",
                "digits": 1,
                "1": BASE_URL + "/handleReturningHelper",
                "3": BASE_URL + "/support",
                "next": BASE_URL + "/receiveCall",
            }
        return json.dumps(payload)

    # For registered customers
    elif userExists(DATABASE, DATABASE_KEY, from_sender, "customer"):
        print("Registered customer")

        # Get name of person to suggest call to from DB
        helperNumber = readActiveHelper(DATABASE, DATABASE_KEY, from_sender)
        name = readNameByNumber(DATABASE, DATABASE_KEY, helperNumber)

        if name is None:
            payload = {
                "ivr": MEDIA_URL + "/ivr/ensam_gamling.mp3",
                "digits": 1,
                "1": BASE_URL + "/handleLonelyCustomer",
                "3": BASE_URL + "/support",
                "next": BASE_URL + "/receiveCall",
            }
            return json.dumps(payload)

        else:
            nameEncoded = urllib.parse.quote(name)  # åäö etc not handled well as URL -> crash

            # Make sure name already exists (generate if somehow missing, for example early volunteers)
            if not os.path.isfile("/media/name/" + nameEncoded + ".mp3"):
                generateNameSoundByte(name)

            payload = {
                "play": MEDIA_URL + "/ivr/behover_hjalp.mp3",
                "next": {
                    "play": MEDIA_URL + "/name/" + nameEncoded + ".mp3",
                    "next": {
                        "ivr": MEDIA_URL + "/ivr/pratade_sist.mp3",
                        "digits": 1,
                        "1": BASE_URL + "/handleReturningCustomer",
                        "2": BASE_URL + "/handleReturningCustomer",
                        "3": BASE_URL + "/handleReturningCustomer",
                        "4": BASE_URL + "/support",
                        "next": BASE_URL + "/receiveCall",
                    },
                },
            }
            return json.dumps(payload)

    # New customer
    payload = {
        "ivr": MEDIA_URL + "/ivr/info.mp3",
        "skippable": "true",
        "digits": 1,
        "1": BASE_URL + "/handleNumberInput",
        "2": BASE_URL + "/receiveCall",
        "3": BASE_URL + "/support",
        "next": BASE_URL + "/receiveCall",
    }
    return json.dumps(payload)


@app.route("/hangup", methods=["POST"])
def hangup():

    print("hangup")
    return ""


@app.route("/handleReturningHelper", methods=["POST"])
def handleReturningHelper():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    if number == 1:
        payload = {
            "play": MEDIA_URL + "/ivr/du_kopplas.mp3",
            "next": BASE_URL + "/callExistingCustomer",
        }
        return json.dumps(payload)

    elif number == 2:
        payload = {
            "play": MEDIA_URL + "/ivr/avreg_confirmed.mp3",
            "next": BASE_URL + "/removeHelper",
        }
        return json.dumps(payload)


@app.route("/callExistingCustomer", methods=["POST"])
def callExistingCustomer():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    helperPhone = request.form.get("from")
    customerPhone = readActiveCustomer(DATABASE, DATABASE_KEY, helperPhone)
    payload = {"connect": customerPhone, "callerid": ELK_NUMBER}
    return json.dumps(payload)


@app.route("/removeHelper", methods=["POST"])
def removeHelper():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    from_sender = request.form.get("from")
    deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, "helper")
    return ""


@app.route("/handleReturningCustomer", methods=["POST"])
def handleReturningCustomer():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    phone = request.form.get("from")
    if number == 1:

        payload = {
            "play": MEDIA_URL + "/ivr/du_kopplas.mp3",
            "skippable": "true",
            "next": BASE_URL + "/callExistingHelper",
        }
        return json.dumps(payload)

    if number == 2:
        zipcode = readZipcodeFromDatabase(DATABASE, DATABASE_KEY, phone, "customer")
        payload = {
            "play": MEDIA_URL + "/ivr/vi_letar.mp3",
            "skippable": "true",
            "next": BASE_URL + "/postcodeInput/%s" % zipcode,
        }
        return json.dumps(payload)

    if number == 3:
        payload = {
            "play": MEDIA_URL + "/ivr/avreg_confirmed.mp3",
            "next": BASE_URL + "/removeCustomer",
        }
        return json.dumps(payload)

    return ""


@app.route("/handleLonelyCustomer", methods=["POST"])
def handleLonelyCustomer():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    phone = request.form.get("from")

    if number == 1:
        zipcode = readZipcodeFromDatabase(DATABASE, DATABASE_KEY, phone, "customer")
        payload = {
            "play": MEDIA_URL + "/ivr/vi_letar.mp3",
            "skippable": "true",
            "next": BASE_URL + "/postcodeInput/%s" % zipcode,
        }
        return json.dumps(payload)

    if number == 2:
        payload = {
            "play": MEDIA_URL + "/ivr/avreg_confirmed.mp3",
            "next": BASE_URL + "/removeCustomer",
        }
        return json.dumps(payload)

    return ""


@app.route("/callExistingHelper", methods=["POST"])
def callExistingHelper():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    customerPhone = request.form.get("from")
    helperPhone = readActiveHelper(DATABASE, DATABASE_KEY, customerPhone)
    payload = {"connect": helperPhone, "callerid": ELK_NUMBER}
    return json.dumps(payload)


@app.route("/postcodeInput/<string:zipcode>", methods=["POST"])
def postcodeInput(zipcode):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    callId = request.form.get("callid")
    phone = request.form.get("from")

    # TODO: Add sound if zipcode is invalid (n/a)
    district = getDistrict(int(zipcode), district_dict)
    timestr = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    saveCustomerToDatabase(DATABASE, DATABASE_KEY, phone, str(zipcode), district, timestr)
    print("zipcode: ", zipcode)

    closestHelpers = fetchHelper(DATABASE, DATABASE_KEY, district, zipcode, location_dict)

    # Reads if the customer has a current helper and if so it will delete the current helper from closestHelpers
    # since the customer have choosen a new helper.
    # closestHelpers
    helperPhone = readActiveHelper(DATABASE, DATABASE_KEY, phone)
    print(f"Helperphone: {helperPhone}")
    print(f"closestHelpers: {closestHelpers}")
    if helperPhone is not None:
        if closestHelpers is not None and helperPhone in closestHelpers:
            closestHelpers.remove(helperPhone)
        writeActiveHelper(DATABASE, DATABASE_KEY, None, helperPhone)

    writeCallHistory(DATABASE, DATABASE_KEY, callId, "closest_helpers", json.dumps(closestHelpers))

    if closestHelpers is None:
        payload = {"play": MEDIA_URL + "/ivr/finns_ingen.mp3"}
        return json.dumps(payload)
    else:
        writeCallHistory(DATABASE, DATABASE_KEY, callId, "hangup", "False")
        payload = {
            "play": MEDIA_URL + "/ivr/ringer_tillbaka.mp3",
            "skippable": "true",
            "next": BASE_URL + "/call/0/%s/%s" % (callId, phone),
        }
        return json.dumps(payload)


@app.route("/call/<int:helperIndex>/<string:customerCallId>/<string:customerPhone>", methods=["POST"])
def call(helperIndex, customerCallId, customerPhone):
    # NOTE: When making changes here, also update /callSupport :)
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    stopCalling = readCallHistory(DATABASE, DATABASE_KEY, customerCallId, "hangup")
    if stopCalling == "True":
        return ""
    else:
        print("helperIndex:", helperIndex)

        print("Customer callId: ", customerCallId)

        closestHelpers = json.loads(readCallHistory(DATABASE, DATABASE_KEY, customerCallId, "closest_helpers"))
        print("closest helpers: ", closestHelpers)

        auth = (API_USERNAME, API_PASSWORD)

        if helperIndex >= len(closestHelpers):
            writeCallHistory(DATABASE, DATABASE_KEY, customerCallId, "hangup", "True")
            return redirect(url_for("callBackToCustomer", customerPhone=customerPhone))

        print(closestHelpers[helperIndex])
        print(ELK_NUMBER)

        # TODO: Handle if call is not picked up
        payload = {
            "ivr": MEDIA_URL + "/ivr/hjalte.mp3",
            "timeout": "30",
            "whenhangup": BASE_URL + "/call/%s/%s/%s" % (str(helperIndex + 1), customerCallId, customerPhone),
            "1": BASE_URL + "/connectUsers/%s/%s" % (customerPhone, customerCallId),
            "2": BASE_URL + "/call/%s/%s/%s" % (str(helperIndex + 1), customerCallId, customerPhone),
        }

        print("Calling: ", closestHelpers[helperIndex])
        fields = {"from": ELK_NUMBER, "to": closestHelpers[helperIndex], "voice_start": json.dumps(payload)}

        response = requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)

        print(json.loads(response.text)["state"])
        print(json.loads(response.text)["state"] == "ongoing")
        # while json.loads(response.text)["state"] == 'ongoing':
        #     pass
        print(json.loads(response.text))
        state = json.loads(response.text)["state"]
        print("state: ", state)
        result = request.form.get("result")
        print("result", result)

        print(response.text)
        return ""


@app.route("/callBackToCustomer/<string:customerPhone>", methods=["POST", "GET"])
def callBackToCustomer(customerPhone):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print("No one found")
    auth = (API_USERNAME, API_PASSWORD)
    payload = {"play": MEDIA_URL + "/ivr/ingen_hittad.mp3"}

    fields = {"from": ELK_NUMBER, "to": customerPhone, "voice_start": json.dumps(payload)}

    requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)
    return ""


@app.route("/removeCustomer", methods=["POST"])
def removeCustomer():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    from_sender = request.form.get("from")
    deleteFromDatabase(DATABASE, DATABASE_KEY, from_sender, "customer")
    return ""


@app.route("/handleNumberInput", methods=["POST"])
def handleNumberInput():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    print("number: ", number)
    print("Write your zipcode")

    payload = {
        "play": MEDIA_URL + "/ivr/post_nr.mp3",
        "next": {"ivr": MEDIA_URL + "/ivr/bep.mp3", "digits": 5, "next": BASE_URL + "/checkZipcode"},
    }

    return json.dumps(payload)


@app.route("/checkZipcode", methods=["POST"])
def checkZipcode():
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    zipcode = request.form.get("result")
    callId = request.form.get("callid")
    city = getCity(int(zipcode), city_dict)
    cityEncoded = urllib.parse.quote(city)
    print("zipcode: ", zipcode)
    print("callId: ", callId)
    print("city: ", city)
    print("cityEnc: ", cityEncoded)

    payload = {
        "play": MEDIA_URL + "/ivr/du_befinner.mp3",
        "next": {
            "play": MEDIA_URL + "/city/" + cityEncoded + ".mp3",
            "next": {
                "ivr": MEDIA_URL + "/ivr/stammer_det.mp3",
                "1": BASE_URL + f"/postcodeInput/{zipcode}",
                "2": BASE_URL + "/handleNumberInput",
                "next": BASE_URL + "/handleNumberInput",
            },
        },
    }

    return json.dumps(payload)


@app.route("/connectUsers/<string:customerPhone>/<string:customerCallId>", methods=["POST"])
def connectUsers(customerPhone, customerCallId):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)

    helperPhone = request.form.get("to")
    print("helper: ", helperPhone)

    print("Saving customer -> helper connection to database")
    # TODO: check current active customer/helper and move to previous
    writeActiveCustomer(DATABASE, DATABASE_KEY, helperPhone, customerPhone)
    writeActiveHelper(DATABASE, DATABASE_KEY, customerPhone, helperPhone)
    writeCallHistory(DATABASE, DATABASE_KEY, customerCallId, "hangup", "True")
    print("Connecting users")
    print("customer:", customerPhone)
    payload = {"connect": customerPhone, "callerid": ELK_NUMBER, "timeout": "15"}
    return json.dumps(payload)


# -------------------------------------------------------------------------------------------------


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if REGISTRATION_SCHEMA.is_valid(data):
        validated = REGISTRATION_SCHEMA.validate(data)

        city = getDistrict(validated["zipCode"], district_dict)
        phone_number = canonicalize_number(validated["phoneNumber"])

        if city == "n/a":
            return {"type": "failure", "message": "Invalid zip"}
        if userExists(DATABASE, DATABASE_KEY, phone_number, "helper"):
            return {"type": "failure", "message": "User already exists"}

        code = "".join(secrets.choice(string.digits) for _ in range(6))
        auth = (API_USERNAME, API_PASSWORD)
        fields = {"from": "Telehelp", "to": phone_number, "message": code}
        requests.post(ELK_BASE + "/a1/sms", auth=auth, data=fields)

        session[phone_number] = {
            "zipCode": validated["zipCode"],
            "name": validated["helperName"],
            "city": city,
            "timestamp": int(time.time()),
            "code": code,
        }

        # Generate sound byte of name: (TODO: Remove if user quits?)
        nameEncoded = urllib.parse.quote(validated["helperName"])  # åäö etc not handled well as URL -> crash
        if not os.path.isfile("/media/name/" + nameEncoded + ".mp3"):
            generateNameSoundByte(validated["helperName"])

        return {"type": "success"}
    return {"type": "failure"}


@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    if VERIFICATION_SCHEMA.is_valid(data):
        validated = VERIFICATION_SCHEMA.validate(data)
        phone_number = canonicalize_number(validated["number"])
        code = validated["verificationCode"]
        if (
            phone_number in session
            and int(time.time()) - session[phone_number]["timestamp"] < VERIFICATION_EXPIRY_TIME
            and code == session[phone_number]["code"]
        ):

            sess = session[phone_number]

            name = sess["name"]
            zipcode = sess["zipCode"]
            city = sess["city"]

            log.info(f"Saving helper to database {name}, {phone_number}, {zipcode}, {city}")
            timestr = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
            saveHelperToDatabase(DATABASE, DATABASE_KEY, name, phone_number, zipcode, city, timestr)
            return {"type": "success"}
    return {"type": "failure"}


@app.route("/getVolunteerLocations", methods=["GET"])
def getVolunteerLocations():
    # Fetch all ZIP codes for volunteer users:
    query = "SELECT zipcode FROM user_helpers"
    zip_pd_dict = fetchData(DATABASE, DATABASE_KEY, query, params=None)
    zip_list = zip_pd_dict.values.tolist()

    # Use ZIPs to get GPS coordinates (lat, long):
    latlongs = []

    print(zip_list)
    for zipcode in zip_list:
        latlongs.append(getLatLong(zipcode[0], location_dict))

    return {"coordinates": latlongs}


#################### TELEHELP SUPPORT FUNCTIONS ###########################


@app.route("/support", methods=["POST"])
def support():
    # Call the Telehelp team in randomized order

    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    callId = request.form.get("callid")
    phone = request.form.get("from")

    # J, T, DEr
    supportTeam = ["+46737600282", "+46707812741", "+46761423456"]
    random.shuffle(supportTeam)  # Randomize order to spread load
    writeCallHistory(DATABASE, DATABASE_KEY, callId, "closest_helpers", json.dumps(supportTeam))
    writeCallHistory(DATABASE, DATABASE_KEY, callId, "hangup", "False")
    payload = {
        "play": MEDIA_URL + "/ivr/ringer_tillbaka_support.mp3",
        "skippable": "true",
        "next": BASE_URL + "/callSupport/0/%s/%s" % (callId, phone),
    }
    return json.dumps(payload)


@app.route("/callSupport/<int:helperIndex>/<string:supportCallId>/<string:supportPhone>", methods=["POST"])
def callSupport(helperIndex, supportCallId, supportPhone):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    stopCalling = readCallHistory(DATABASE, DATABASE_KEY, supportCallId, "hangup")
    if stopCalling == "True":
        return ""
    else:
        print("supportTeamIndex:", helperIndex)

        print("Support customer callId: ", supportCallId)

        supportTeamList = json.loads(readCallHistory(DATABASE, DATABASE_KEY, supportCallId, "closest_helpers"))
        print("closest helpers: ", supportTeamList)

        auth = (API_USERNAME, API_PASSWORD)

        if helperIndex >= len(supportTeamList):
            writeCallHistory(DATABASE, DATABASE_KEY, supportCallId, "hangup", "True")
            return redirect(url_for("callBackToSupportCustomer", supportPhone=supportPhone))

        print(supportTeamList[helperIndex])
        print(ELK_NUMBER)

        # TODO: Handle if call is not picked up
        payload = {
            "ivr": MEDIA_URL + "/ivr/hjalte_support.mp3",
            "timeout": "30",
            "whenhangup": BASE_URL + "/call/%s/%s/%s" % (str(helperIndex + 1), supportCallId, supportPhone),
            "1": BASE_URL + "/connectUsersSupport/%s/%s" % (supportPhone, supportCallId),
            "2": BASE_URL + "/callSupport/%s/%s/%s" % (str(helperIndex + 1), supportCallId, supportPhone),
        }

        print("Calling: ", supportTeamList[helperIndex])
        fields = {"from": ELK_NUMBER, "to": supportTeamList[helperIndex], "voice_start": json.dumps(payload)}

        response = requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)

        print(response.text)
        return ""


@app.route("/callBackToSupportCustomer/<string:customerPhone>", methods=["POST", "GET"])
def callBackToSupportCustomer(customerPhone):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)
    print("No support team person found")
    auth = (API_USERNAME, API_PASSWORD)
    payload = {"play": MEDIA_URL + "/ivr/ingen_hittad_support.mp3"}

    fields = {"from": ELK_NUMBER, "to": customerPhone, "voice_start": json.dumps(payload)}

    requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)
    return ""


@app.route("/connectUsersSupport/<string:customerPhone>/<string:customerCallId>", methods=["POST"])
def connectUsersSupport(customerPhone, customerCallId):
    checkRequest(request, ELK_USER_AGENT, ELK_URL)

    helperPhone = request.form.get("to")
    print("support from: ", helperPhone)

    writeCallHistory(DATABASE, DATABASE_KEY, customerCallId, "hangup", "True")
    print("Connecting users")
    print("customer:", customerPhone)
    payload = {"connect": customerPhone, "callerid": ELK_NUMBER, "timeout": "15"}
    return json.dumps(payload)


# -----------------------------------Test Functions-------------------------------------------------
@app.route("/testredirect/<int:numb>", methods=["POST", "GET"])
def testredirect(numb):
    print(f"Redirect works:{numb}")
    return "Redirect works"


@app.route("/testendpoint", methods=["GET"])
def testendpoint():
    return redirect(url_for("testredirect", numb=1))


# --------------------------------------------------------------------------------------------------

import json
import logging
import os
import random
import secrets
import socket
import string
import threading
import time
import urllib.parse
import uuid
from collections import Counter
from collections import defaultdict
from pprint import pprint

import pandas as pd
import requests
from flask import abort
from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_session import Session
from redis import Redis

from checkMedia import checkPayload
from databaseIntegration import DatabaseConnection

from schemas import REGISTRATION_SCHEMA
from schemas import VERIFICATION_SCHEMA
from text2speech_utils import generateNameSoundByte
from zipcode_utils import getCity
from zipcode_utils import getDistanceApart
from zipcode_utils import getDistrict
from zipcode_utils import readZipCodeData
from databaseIntegration import DatabaseConnection


def setup_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    handler = logging.FileHandler("flask.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    startTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    log.info(f"New log entry {startTime}")
    return log


env_vars = (
    "BASE_URL",
    "ELK_NUMBER",
    "ELK_USERNAME",
    "ELK_PASSWORD",
    "DB_HOST",
    "HOOK_URL",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "SECRET_KEY",
    "REDIS_HOST",
    "GOOGLE_APPLICATION_CREDENTIALS",
)

missing = set(env_vars) - set(os.environ)
if missing:
    print("[W] WARNING: Some environment variables are not set: %s" % missing)

BASE_URL = os.getenv("BASE_URL")
ELK_NUMBER = os.getenv("ELK_NUMBER")
ELK_USERNAME = os.getenv("ELK_USERNAME")
ELK_PASSWORD = os.getenv("ELK_PASSWORD")
HOOK_URL = os.getenv("HOOK_URL")


app = Flask(__name__, static_folder="../client/build", static_url_path="/")

# Flask-Redis setup
SESSION_TYPE = "redis"
SECRET_KEY = os.getenv("SECRET_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
SESSION_REDIS = Redis(host=REDIS_HOST)
app.config.from_object(__name__)
Session(app)

log = setup_logger()

db = DatabaseConnection()

ZIPDATA = "resources/SE.tsv"
MEDIA_URL = "https://files.telehelp.se/sv"
ELK_BASE = "https://api.46elks.com"
VERIFICATION_EXPIRY_TIME = 5 * 60  # 5 minutes

LOCATION_DICT, DISTRICT_DICT, CITY_DICT = readZipCodeData(ZIPDATA)

print("Site phone number: " + ELK_NUMBER)


def canonicalize_number(phone_number):
    if phone_number[0] == "0":
        phone_number = "+46" + phone_number[1:]
    return phone_number


def ivr(action):
    # TODO: Use an enum for static checking
    return f"{MEDIA_URL}/ivr/{action}.mp3"


def api(action):
    return f"{BASE_URL}/api/{action}"


@app.route("/")
def index():
    return app.send_static_file("index.html")


# ------------------------------ PHONE API ----------------------------------------------------


@app.route("/api/receiveCall", methods=["POST"])
def receiveCall():
    callId = request.form.get("callid")
    startTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    telehelpCallId = str(uuid.uuid1())
    db.createNewCallHistory(callId)

    from_sender = request.form.get("from")
    print(from_sender)

    # For registered helpers
    if db.helperExists(from_sender):
        print("Registered helper")
        db.writeHelperAnalytics(
            telehelpCallId,
            ["telehelp_callid", "elks_callid", "call_start_time"],
            (telehelpCallId, callId, startTime),
        )
        activeCustomer = db.readActiveCustomer(from_sender)
        print(activeCustomer)
        if activeCustomer is None:
            payload = {
                "ivr": ivr("hjalper_ingen"),
                "skippable": "true",
                "digits": 1,
                "2": api("support"),
                "1": {
                    "play": ivr("avreg_confirmed"),
                    "next": api("removeHelper/%s" % telehelpCallId),
                },
                "next": api("receiveCall"),
            }
        else:
            payload = {
                "ivr": ivr("registrerad_volontar"),
                "digits": 1,
                "1": api("handleReturningHelper/%s" % telehelpCallId),
                "2": {
                    "play": ivr("avreg_confirmed"),
                    "next": api("removeHelper/%s" % telehelpCallId),
                },
                "3": api("support"),
                "next": api("receiveCall"),
            }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    # For registered customers
    elif db.customerExists(from_sender):
        print("Registered customer")
        db.writeCustomerAnalytics(
            telehelpCallId,
            ["telehelp_callid", "elks_callid", "call_start_time", "new_customer"],
            (telehelpCallId, callId, startTime, "False"),
        )

        # Get name of person to suggest call to from DB
        helperNumber = db.readActiveHelper(from_sender)
        name = db.readNameByNumber(helperNumber)

        if name is None:
            payload = {
                "ivr": ivr("ensam_gamling"),
                "digits": 1,
                "1": api("handleLonelyCustomer/%s" % telehelpCallId),
                "2": api("removeCustomer"),
                "3": api("support"),
                "next": api("receiveCall"),
            }
            checkPayload(payload, MEDIA_URL, log=log)
            return payload

        else:
            nameEncoded = urllib.parse.quote(name)  # åäö etc not handled well as URL -> crash

            # Make sure name already exists (generate if somehow missing, for example early volunteers)
            if not os.path.isfile("/media/name/" + nameEncoded + ".mp3"):
                generateNameSoundByte(name)

            payload = {
                "play": ivr("behover_hjalp"),
                "next": {
                    "play": MEDIA_URL + "/name/" + nameEncoded + ".mp3",
                    "next": {
                        "ivr": ivr("pratade_sist"),
                        "digits": 1,
                        "1": api("handleReturningCustomer/%s" % telehelpCallId),
                        "2": api("handleReturningCustomer/%s" % telehelpCallId),
                        "3": api("handleReturningCustomer/%s" % telehelpCallId),
                        "4": api("support"),
                        "next": api("receiveCall"),
                    },
                },
            }
            checkPayload(payload, MEDIA_URL, log=log)
            return payload

    # New customer
    db.writeCustomerAnalytics(
        telehelpCallId,
        ["telehelp_callid", "elks_callid", "call_start_time", "new_customer"],
        (telehelpCallId, callId, startTime, "True"),
    )

    payload = {
        "ivr": ivr("info"),
        "skippable": "true",
        "digits": 1,
        "1": api("handleNumberInput/%s" % telehelpCallId),
        "2": api("receiveCall"),
        "3": api("support"),
        "next": api("receiveCall"),
    }
    checkPayload(payload, MEDIA_URL, log=log)
    return payload


@app.route("/api/customerHangup/<string:telehelpCallId>", methods=["POST", "GET"])
def customerHangup(telehelpCallId):
    print("hangup")
    endTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    db.writeCustomerAnalytics(telehelpCallId, ["call_end_time"], (endTime, telehelpCallId))
    return ""


@app.route("/api/helperHangup/<string:telehelpCallId>", methods=["POST", "GET"])
def helperHangup(telehelpCallId):
    print("hangup")
    endTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    db.writeHelperAnalytics(telehelpCallId, ["call_end_time"], (endTime, telehelpCallId))
    return ""


@app.route("/api/handleReturningHelper/<string:telehelpCallId>", methods=["POST"])
def handleReturningHelper(telehelpCallId):
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    if number == 1:
        db.writeHelperAnalytics(
            telehelpCallId,
            ["contacted_prev_customer", "deregistered"],
            ("True", "False", telehelpCallId),
        )
        payload = {
            "play": ivr("du_kopplas"),
            "next": api("callExistingCustomer/%s" % telehelpCallId),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    elif number == 2:
        payload = {
            "play": ivr("avreg_confirmed"),
            "next": api("removeHelper/%s" % telehelpCallId),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload


@app.route("/api/callExistingCustomer/<string:telehelpCallId>", methods=["POST"])
def callExistingCustomer(telehelpCallId):
    helperPhone = request.form.get("from")
    customerPhone = db.readActiveCustomer(helperPhone)
    payload = {
        "connect": customerPhone,
        "callerid": ELK_NUMBER,
        "whenhangup": api("helperHangup/%s" % telehelpCallId),
    }
    return payload


@app.route("/api/removeHelper/<string:telehelpCallId>", methods=["POST"])
def removeHelper(telehelpCallId):
    from_sender = request.form.get("from")
    endTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    db.writeHelperAnalytics(
        telehelpCallId,
        ["call_end_time", "contacted_prev_customer", "deregistered"],
        (endTime, "False", "True", telehelpCallId),
    )
    db.deleteFromDatabase(from_sender, "helper")
    return ""


@app.route("/api/handleReturningCustomer/<string:telehelpCallId>", methods=["POST"])
def handleReturningCustomer(telehelpCallId):
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    phone = request.form.get("from")
    if number == 1:

        payload = {
            "play": ivr("du_kopplas"),
            "skippable": "true",
            "next": api("callExistingHelper/%s" % telehelpCallId),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    if number == 2:
        db.writeCustomerAnalytics(
            telehelpCallId,
            ["used_prev_helper", "deregistered"],
            ("False", "False", telehelpCallId),
        )
        zipcode = db.readZipcodeFromDatabase(phone, "customer")
        payload = {
            "play": ivr("vi_letar"),
            "skippable": "true",
            "next": api("postcodeInput/%s/%s" % (zipcode, telehelpCallId)),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    if number == 3:
        db.writeCustomerAnalytics(
            telehelpCallId,
            ["used_prev_helper", "deregistered"],
            ("False", "True", telehelpCallId),
        )
        payload = {
            "play": ivr("avreg_confirmed"),
            "next": api("removeCustomer"),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    return ""


@app.route("/api/handleLonelyCustomer/<string:telehelpCallId>", methods=["POST"])
def handleLonelyCustomer(telehelpCallId):
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    phone = request.form.get("from")

    if number == 1:
        zipcode = db.readZipcodeFromDatabase(phone, "customer")
        payload = {
            "play": ivr("vi_letar"),
            "skippable": "true",
            "next": api("postcodeInput/%s/%s" % (zipcode, telehelpCallId)),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    if number == 2:
        db.writeCustomerAnalytics(telehelpCallId, ["deregistered"], ("True", telehelpCallId))
        payload = {
            "play": ivr("avreg_confirmed"),
            "next": api("removeCustomer"),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload

    return ""


@app.route("/api/callExistingHelper/<string:telehelpCallId>", methods=["POST"])
def callExistingHelper(telehelpCallId):
    customerPhone = request.form.get("from")
    helperPhone = db.readActiveHelper(customerPhone)
    db.writeCustomerAnalytics(
        telehelpCallId,
        ["used_prev_helper", "deregistered"],
        ("True", "False", telehelpCallId),
    )
    payload = {
        "connect": helperPhone,
        "callerid": ELK_NUMBER,
        "whenhangup": api("customerHangup/%s" % telehelpCallId),
    }
    return payload


@app.route("/api/postcodeInput/<string:zipcode>/<string:telehelpCallId>", methods=["POST"])
def postcodeInput(zipcode, telehelpCallId):
    callId = request.form.get("callid")
    phone = request.form.get("from")

    # TODO: Add sound if zipcode is invalid (n/a)
    district = getDistrict(int(zipcode), DISTRICT_DICT)
    timestr = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    db.saveCustomerToDatabase(phone, str(zipcode), district, timestr)
    print("zipcode: ", zipcode)

    closestHelpers = db.fetchHelper(district, zipcode, LOCATION_DICT)

    # Reads if the customer has a current helper and if so it will delete the current helper from closestHelpers
    # since the customer have choosen a new helper.
    # closestHelpers
    helperPhone = db.readActiveHelper(phone)
    print(f"Helperphone: {helperPhone}")
    print(f"closestHelpers: {closestHelpers}")
    if helperPhone is not None:
        if closestHelpers is not None and helperPhone in closestHelpers:
            closestHelpers.remove(helperPhone)
        db.writeActiveCustomer(helperPhone, None)

    db.writeCallHistory(callId, "closest_helpers", json.dumps(closestHelpers))

    if closestHelpers is None:
        db.writeCustomerAnalytics(telehelpCallId, ["n_helpers_contacted"], ("0", telehelpCallId))
        payload = {"play": ivr("finns_ingen")}

        checkPayload(payload, MEDIA_URL, log=log)
        return payload
    else:
        db.writeCallHistory(callId, "hangup", "False")
        payload = {
            "play": ivr("ringer_tillbaka"),
            "skippable": "true",
            "next": api("call/0/%s/%s/%s" % (callId, phone, telehelpCallId)),
        }
        checkPayload(payload, MEDIA_URL, log=log)
        return payload


@app.route(
    "/api/call/<int:helperIndex>/<string:customerCallId>/<string:customerPhone>/<string:telehelpCallId>",
    methods=["POST"],
)
def call(helperIndex, customerCallId, customerPhone, telehelpCallId):
    # NOTE: When making changes here, also update /callSupport :)

    stopCalling = db.readCallHistory(customerCallId, "hangup")
    if stopCalling == "True":
        endTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
        db.writeCustomerAnalytics(
            telehelpCallId,
            ["call_end_time", "n_helpers_contacted"],
            (endTime, str(helperIndex), telehelpCallId),
        )
        return ""
    else:
        print("helperIndex:", helperIndex)

        print("Customer callId: ", customerCallId)

        closestHelpers = json.loads(db.readCallHistory(customerCallId, "closest_helpers"))
        print("closest helpers: ", closestHelpers)

        auth = (ELK_USERNAME, ELK_PASSWORD)

        if helperIndex >= len(closestHelpers):
            db.writeCallHistory(customerCallId, "hangup", "True")
            db.writeCustomerAnalytics(
                telehelpCallId,
                ["n_helpers_contacted"],
                (str(helperIndex), telehelpCallId),
            )
            return redirect(
                url_for("callBackToCustomer", customerPhone=customerPhone, telehelpCallId=telehelpCallId)
            )

        print(closestHelpers[helperIndex])
        print(ELK_NUMBER)

        payload = {
            "ivr": ivr("hjalte"),
            "timeout": "30",
            "1": api("connectUsers/%s/%s/%s" % (customerPhone, customerCallId, telehelpCallId)),
            "2": api(
                "call/%s/%s/%s/%s" % (str(helperIndex + 1), customerCallId, customerPhone, telehelpCallId)
            ),
            "next": api(
                "call/%s/%s/%s/%s" % (str(helperIndex + 1), customerCallId, customerPhone, telehelpCallId)
            ),
        }

        checkPayload(payload, MEDIA_URL, log=log)

        print("Calling: ", closestHelpers[helperIndex])
        fields = {
            "from": ELK_NUMBER,
            "to": closestHelpers[helperIndex],
            "voice_start": json.dumps(payload),
            "whenhangup": api(
                "call/%s/%s/%s/%s" % (str(helperIndex + 1), customerCallId, customerPhone, telehelpCallId)
            ),
        }

        response = requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)
        print(response.text)
        return ""


@app.route("/api/callBackToCustomer/<string:customerPhone>/<string:telehelpCallId>", methods=["POST", "GET"])
def callBackToCustomer(customerPhone, telehelpCallId):
    print("No one found")
    auth = (ELK_USERNAME, ELK_PASSWORD)
    payload = {"play": ivr("ingen_hittad")}

    fields = {"from": ELK_NUMBER, "to": customerPhone, "voice_start": json.dumps(payload)}

    requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)
    endTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
    db.writeCustomerAnalytics(
        telehelpCallId,
        ["call_end_time", "match_found"],
        (endTime, "False", telehelpCallId),
    )

    return ""


@app.route("/api/removeCustomer", methods=["POST"])
def removeCustomer():
    from_sender = request.form.get("from")
    db.deleteFromDatabase(from_sender, "customer")
    return ""


@app.route("/api/handleNumberInput/<string:telehelpCallId>", methods=["POST"])
def handleNumberInput(telehelpCallId):
    print(request.form.get("result"))
    number = int(request.form.get("result"))
    print("number: ", number)
    print("Write your zipcode")
    payload = {
        "play": ivr("post_nr"),
        "next": {
            "ivr": ivr("bep"),
            "digits": 5,
            "next": api("checkZipcode/%s" % telehelpCallId),
        },
    }
    checkPayload(payload, MEDIA_URL, log=log)
    return payload
    return ""


@app.route("/api/checkZipcode/<string:telehelpCallId>", methods=["POST"])
def checkZipcode(telehelpCallId):
    zipcode = request.form.get("result")
    callId = request.form.get("callid")
    city = getCity(int(zipcode), CITY_DICT)
    cityEncoded = urllib.parse.quote(city)
    print("zipcode: ", zipcode)
    print("callId: ", callId)
    print("city: ", city)
    print("cityEnc: ", cityEncoded)

    payload = {
        "play": ivr("du_befinner"),
        "next": {
            "play": MEDIA_URL + "/city/" + cityEncoded + ".mp3",
            "next": {
                "ivr": ivr("stammer_det"),
                "1": api(f"/api/postcodeInput/{zipcode}/{telehelpCallId}"),
                "2": api("handleNumberInput/%s" % telehelpCallId),
                "next": api("handleNumberInput/%s" % telehelpCallId),
            },
        },
    }
    checkPayload(payload, MEDIA_URL, log=log)
    return payload


@app.route(
    "/api/connectUsers/<string:customerPhone>/<string:customerCallId>/<string:telehelpCallId>",
    methods=["POST"],
)
def connectUsers(customerPhone, customerCallId, telehelpCallId):
    helperPhone = request.form.get("to")
    print("helper: ", helperPhone)

    print("Saving customer -> helper connection to database")
    # TODO: check current active customer/helper and move to previous
    db.writeCustomerAnalytics(telehelpCallId, ["match_found"], ("True", telehelpCallId))
    # writeCustomerAnalytics(DATABASE, DATABASE_KEY, telehelpCallId, match_found="True")
    db.writeActiveCustomer(helperPhone, customerPhone)
    db.writeActiveHelper(customerPhone, helperPhone)
    db.writeCallHistory(customerCallId, "hangup", "True")
    print("Connecting users")
    print("customer:", customerPhone)

    if HOOK_URL is not None:
        res = db.readNewConnectionInfo(helperPhone)[0]
        requests.post(
            HOOK_URL, {"content": f"{res[0]} från {res[1]} har fått kontakt med någon som behöver hjälp!"}
        )

    payload = {"connect": customerPhone, "callerid": ELK_NUMBER, "timeout": "15"}

    # Send a delayed SMS asking for a response on whether assignment accepted
    print("Preparing to send SMS to connected volunteer.")
    smsThread = threading.Thread(target=sendAskIfHelpingSms, args=(helperPhone,))
    smsThread.start()

    return payload


def sendAskIfHelpingSms(volunteerNumber):
    time.sleep(60)
    msg = "Förhoppningsvis kan du hjälpa personen du precis pratade med. \
Ring till Telehelp på 0766861551 för att nå personen igen vid behov. \
Svara TILLGÄNGLIG om du inte kunde hjälpa till eller är klar med uppgiften, så gör \
vi dig tillgänglig för nya uppdrag. Observera att varken du eller den \
du hjälpt kommer kunna nå varandra igen om du gör detta. Tack för din insats!"
    auth = (ELK_USERNAME, ELK_PASSWORD)
    fields = {"from": ELK_NUMBER, "to": volunteerNumber, "message": msg}
    requests.post(ELK_BASE + "/a1/sms", auth=auth, data=fields)

    print("Sent confirmation SMS to volunteer: " + volunteerNumber)


@app.route("/api/receiveSms", methods=["POST"])
def receiveSms():
    volunteerNumber = request.form.get("from")
    response = request.form.get("message").strip().upper()
    print("SMS received: " + response + " from " + volunteerNumber)

    if response == "TILLGÄNGLIG":
        # Clear database pairing to make volunteer available again. Remove volunteer from customer side too.
        db.clearCustomerHelperPairing(volunteerNumber)

    # Your webhook code must respond with a HTTP status in the range 200-204.
    return ""


# -------------------------------------------------------------------------------------------------


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if REGISTRATION_SCHEMA.is_valid(data):
        validated = REGISTRATION_SCHEMA.validate(data)

        city = getDistrict(validated["zipCode"], DISTRICT_DICT)
        phone_number = canonicalize_number(validated["phoneNumber"])

        if city == "n/a":
            return {"type": "failure", "message": "Invalid zip"}
        if db.helperExists(phone_number):
            return {"type": "failure", "message": "User already exists"}

        code = "".join(secrets.choice(string.digits) for _ in range(6))
        auth = (ELK_USERNAME, ELK_PASSWORD)
        fields = {"from": "Telehelp", "to": phone_number, "message": code}
        requests.post(ELK_BASE + "/a1/sms", auth=auth, data=fields)
        session[phone_number] = {
            "zipCode": validated["zipCode"],
            "name": validated["helperName"],
            "city": city,
            "timestamp": int(time.time()),
            "code": code,
        }

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

            if HOOK_URL is not None:
                requests.post(HOOK_URL, {"content": f"{name} från {city} har registrerat sig som volontär!"})
            log.info(f"Saving helper to database {name}, {phone_number}, {zipcode}, {city}")
            timestr = time.strftime("%Y-%m-%d:%H-%M-%S", time.gmtime())
            db.saveHelperToDatabase(name, phone_number, zipcode, city, timestr)

            #  TODO: Remove soundbyte if user quits?
            urlEscapedName = urllib.parse.quote(name)
            mediaPath = os.path.join("/", "media", f"{urlEscapedName}.mp3")
            if not os.path.isfile(mediaPath) and os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None:
                generateNameSoundByte(name)

            return {"type": "success"}
    return {"type": "failure"}


@app.route("/getVolunteerLocations", methods=["GET"])
def getVolunteerLocations():
    query = "SELECT zipcode FROM user_helpers"
    volunteer_zipcodes_df = db.fetchData(query, params=None)["zipcode"]

    district_data = defaultdict(list)
    c = Counter(volunteer_zipcodes_df)

    for zipCode, count in c.most_common():
        z = int(zipCode)  # Should change this to use string if we have the time
        district = DISTRICT_DICT.get(z)

        entry = {
            "coordinates": LOCATION_DICT.get(z),
            "city": CITY_DICT.get(z),
            "zipcode": zipCode,
            "count": count,
        }
        district_data[district].append(entry)

    return {
        "total": sum(c.values()),
        "locations": [{"district": key, "data": val} for key, val in district_data.items()],
    }


#################### TELEHELP SUPPORT FUNCTIONS ###########################


@app.route("/api/support", methods=["POST"])
def support():
    # Call the Telehelp team in randomized order
    callId = request.form.get("callid")
    phone = request.form.get("from")

    # J, T, DEr
    supportTeam = ["+46737600282", "+46707812741"]
    random.shuffle(supportTeam)  # Randomize order to spread load
    db.writeCallHistory(callId, "closest_helpers", json.dumps(supportTeam))
    db.writeCallHistory(callId, "hangup", "False")
    payload = {
        "play": ivr("ringer_tillbaka_support"),
        "skippable": "true",
        "next": api("callSupport/0/%s/%s" % (callId, phone)),
    }
    return payload


@app.route("/api/callSupport/<int:helperIndex>/<string:supportCallId>/<string:supportPhone>", methods=["POST"])
def callSupport(helperIndex, supportCallId, supportPhone):
    stopCalling = db.readCallHistory(supportCallId, "hangup")
    if stopCalling == "True":
        return ""
    else:
        print("supportTeamIndex:", helperIndex)

        print("Support customer callId: ", supportCallId)

        supportTeamList = json.loads(db.readCallHistory(supportCallId, "closest_helpers"))
        print("closest helpers: ", supportTeamList)

        auth = (ELK_USERNAME, ELK_PASSWORD)

        if helperIndex >= len(supportTeamList):
            db.writeCallHistory(supportCallId, "hangup", "True")
            return redirect(url_for("callBackToSupportCustomer", supportPhone=supportPhone))

        print(supportTeamList[helperIndex])
        print(ELK_NUMBER)

        # TODO: Handle if call is not picked up
        payload = {
            "ivr": ivr("hjalte_support"),
            "timeout": "30",
            "1": api("connectUsersSupport/%s/%s" % (supportPhone, supportCallId)),
            "2": api("callSupport/%s/%s/%s" % (str(helperIndex + 1), supportCallId, supportPhone)),
            "next": api("callSupport/%s/%s/%s" % (str(helperIndex + 1), supportCallId, supportPhone)),
        }

        print("Calling: ", supportTeamList[helperIndex])
        fields = {
            "from": ELK_NUMBER,
            "to": supportTeamList[helperIndex],
            "voice_start": json.dumps(payload),
            "whenhangup": api("callSupport/%s/%s/%s" % (str(helperIndex + 1), supportCallId, supportPhone)),
        }

        response = requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)

        print(response.text)
        return ""


@app.route("/api/callBackToSupportCustomer/<string:supportPhone>", methods=["POST", "GET"])
def callBackToSupportCustomer(supportPhone):
    print("No support team person found")
    auth = (ELK_USERNAME, ELK_PASSWORD)
    payload = {"play": ivr("ingen_hittad_support")}

    fields = {"from": ELK_NUMBER, "to": supportPhone, "voice_start": json.dumps(payload)}

    requests.post(ELK_BASE + "/a1/calls", data=fields, auth=auth)
    return ""


@app.route("/api/connectUsersSupport/<string:customerPhone>/<string:customerCallId>", methods=["POST"])
def connectUsersSupport(customerPhone, customerCallId):
    helperPhone = request.form.get("to")
    print("support from: ", helperPhone)

    db.writeCallHistory(customerCallId, "hangup", "True")
    print("Connecting users")
    print("customer:", customerPhone)
    payload = {"connect": customerPhone, "callerid": ELK_NUMBER, "timeout": "15"}
    return payload


# -----------------------------------Test Functions-------------------------------------------------
@app.route("/testredirect/<int:numb>", methods=["POST", "GET"])
def testredirect(numb):
    print(f"Redirect works:{numb}")
    return "Redirect works"


@app.route("/testendpoint", methods=["GET"])
def testendpoint():
    return redirect(url_for("testredirect", numb=1))


@app.route("/helloworld", methods=["GET"])
def testhelloworld():
    return "Hello World!!!!"


# --------------------------------------------------------------------------------------------------

import os
import random

import pandas as pd
from pysqlcipher3 import dbapi2 as sqlite3

from .zipcode_utils import getDistanceApart
from .zipcode_utils import getDistrict
from .zipcode_utils import readZipCodeData

# from dotenv import load_dotenv
# load_dotenv()


def create_connection(db_file, key):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key = \"x'" + key + "'\"")

    return conn, cursor


def fetchData(db, key, query, params=None):
    conn, cursor = create_connection(db, key)
    if params is None:
        execute = cursor.execute(query)
    else:
        execute = cursor.execute(query, params)
    data = cursor.fetchall()
    cols = [column[0] for column in execute.description]
    data = pd.DataFrame(data=data, columns=cols)
    conn.close()
    return data


def writeToDatabase(db, key, query, params):
    # try:
    print("Connecting")
    conn, cursor = create_connection(db, key)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return "Success"
    # except Exception as err:
    # 	print(err)
    # 	return 'Failure'


def readDatabase(db, key, query, params=None):
    # try:
    conn, cursor = create_connection(db, key)
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    res = cursor.fetchall()
    conn.close()
    return res
    # except Exception as err:
    # 	print(Exception, err)
    # 	return 'Failure'


def readZipcodeFromDatabase(db, key, phone, userType):
    if userType == "customer":
        query = """ SELECT zipcode FROM user_customers where phone=? """
    if userType == "helper":
        query = """ SELECT zipcode FROM user_helpers where phone=? """
    params = [phone]
    res = readDatabase(db, key, query, params)
    return res[0][0]


def saveHelperToDatabase(db, key, name, phone, zipcode, district, timestr):
    print("Writing phone and postcode to database")
    print(
        "\nname: ", name, "\nzipcode:", zipcode, "\nphone: ", phone, "\ndistrict:", district,
    )

    query = """ INSERT INTO user_helpers (phone, name, zipcode, district, signup_time)
                                    values(?, ?, ?, ?, ?) """
    params = (phone, name, zipcode, district, timestr)
    flag = writeToDatabase(db, key, query, params)
    print(flag)
    return flag


def clearCustomerHelperPairing(db, key, helperPhone):
    customerPhone = readActiveCustomer(db, key, helperPhone)
    if customerPhone is not None:
        writeActiveCustomer(db, key, helperPhone, None)
    writeActiveHelper(db, key, customerPhone, None)


def writeActiveCustomer(db, key, helperPhone, customerPhone):
    query = """ UPDATE user_helpers set active_customers=? where phone=? """
    params = (customerPhone, helperPhone)
    flag = writeToDatabase(db, key, query, params)
    return flag


def writeActiveHelper(db, key, customerPhone, helperPhone):
    query = """ UPDATE user_customers set active_helpers=? where phone=? """
    params = (helperPhone, customerPhone)
    flag = writeToDatabase(db, key, query, params)
    return flag


def readActiveCustomer(db, key, helperPhone):
    query = """ SELECT active_customers FROM user_helpers where phone=? """
    params = [helperPhone]
    res = readDatabase(db, key, query, params)
    if res == []:
        return None
    return res[0][0]


def readActiveHelper(db, key, customerPhone):
    query = """ SELECT active_helpers FROM user_customers where phone=? """
    params = [customerPhone]
    res = readDatabase(db, key, query, params)
    return res[0][0]


def readNewConnectionInfo(db, key, helperPhone):
    query = """ SELECT name, district FROM user_helpers where phone=? """
    params = [helperPhone]
    res = readDatabase(db, key, query, params)
    return res


def readNameByNumber(db, key, helperPhone):
    query = """ SELECT name FROM user_helpers WHERE phone=? """
    res = readDatabase(db, key, query, [helperPhone])
    if res == []:
        return None
    return res[0][0]


def saveCustomerToDatabase(db, key, phone, zipcode, district, timestr):
    print("Writing phone and postcode to database")
    print("zipcode:", zipcode, "\nphone: ", phone)

    if userExists(db, key, phone, "customer"):
        query = """ UPDATE user_customers set district=? where phone=? """
        params = (district, phone)
    else:
        query = """ INSERT INTO user_customers (phone, zipcode, district, signup_time)
                                            values(?, ?, ?, ?) """
        params = (phone, zipcode, district, timestr)
    flag = writeToDatabase(db, key, query, params)

    print(flag)
    return flag


def userExists(db, key, phone, userType):
    if userType == "customer":
        query = """SELECT * FROM user_customers WHERE phone = ?"""
    elif userType == "helper":
        query = """SELECT * FROM user_helpers WHERE phone = ?"""
    else:
        print("Invalid userType")
        return None

    params = [phone]
    ans = readDatabase(db, key, query, params)
    print(ans)
    if ans == []:
        return False
    else:
        return True
    return


def deleteFromDatabase(db, key, phone, userType):
    if userType == "customer":
        userQuery = """DELETE FROM user_customers WHERE phone = ?"""
        linkQuery = """UPDATE user_helpers set active_customers=null where active_customers=?"""
    elif userType == "helper":
        userQuery = """DELETE FROM user_helpers WHERE phone = ?"""
        linkQuery = """UPDATE user_customers set active_helpers=null where active_helpers=?"""
    else:
        print("Invalid userType")
        return
    userParams = [phone]
    linkParams = [phone]
    flag1 = writeToDatabase(db, key, userQuery, userParams)
    flag2 = writeToDatabase(db, key, linkQuery, linkParams)
    return flag1, flag2


def getHelpers(db, key):
    query = "SELECT * FROM user_helpers"
    return fetchData(db, key, query)


def getCustomers(db, key):
    query = "SELECT * FROM user_customers"
    return fetchData(db, key, query)


def writeCallHistory(db, key, callid, columnName, data):
    print(data)
    if columnName == "hangup":
        query = """ UPDATE call_variables set hangup=? where callid=? """
    elif columnName == "closest_helpers":
        query = """ UPDATE call_variables set closest_helpers=? where callid=? """

    params = (data, callid)
    writeToDatabase(db, key, query, params)


"""
Fetch a list of helpers based on a given district, and selecting the
closest unassigned helpers (with some noise to randomize order within zipcodes).
The output list is limited to maxDist km and maxQueue numbers.
"""


def fetchHelper(db, key, district, zipcode, location_dict):
    query = """SELECT * FROM user_helpers where district=?"""
    params = [district]
    helperData = fetchData(db, key, query, params)
    distances = []
    phoneNumbers = []
    if helperData.empty:
        print("No helpers registered in area")
        return None
    for i in range(len(helperData)):
        phoneNumbers.append(helperData.loc[i, "phone"])
        # In the case that multiple helpers live in the same postal code, add noise to randomize calling order
        noisyDistance = (
            getDistanceApart(zipcode, helperData.loc[i, "zipcode"], location_dict) + random.random()
        )
        distances.append(noisyDistance)
    zipped = list(zip(phoneNumbers, distances))
    zipped.sort(key=lambda t: t[1])

    # Filter out numbers that are less than maxDist km from caller, and call up to maxQueue numbers
    maxDist = 20.0
    maxQueue = 10
    sortedNumbersFinal = []
    sortedDistancesFinal = []

    for number, distance in zipped:
        if (distance <= maxDist) and (readActiveCustomer(db, key, number) is None):
            sortedNumbersFinal.append(number)
            sortedDistancesFinal.append(distance)

    sortedDistancesFinal = sortedDistancesFinal[:maxQueue]
    sortedNumbersFinal = sortedNumbersFinal[:maxQueue]
    print(list(sortedDistancesFinal))
    print(list(sortedNumbersFinal))
    if len(sortedNumbersFinal) == 0:
        print("No unassigned helpers available in area")
        return None

    return list(sortedNumbersFinal)


def readCallHistory(db, key, callid, columnName):
    if columnName == "hangup":
        query = """ SELECT hangup FROM call_variables WHERE callid=? """
    elif columnName == "closest_helpers":
        query = """ SELECT closest_helpers FROM call_variables WHERE callid=? """
    params = [callid]
    res = readDatabase(db, key, query, params)
    print("result readCallHistory: ", res)
    # print(res[columnName])
    # result = res[columnName].to_string()
    # print(result)
    return res[0][0]


def callExists(db, key, callid, tableName):
    if tableName == "call_variables":
        query = """ SELECT * FROM call_variables WHERE callid=?"""
    elif tableName == "call_analytics_customer":
        query = """ SELECT * FROM call_analytics_customer WHERE telehelp_callid=?"""
    elif tableName == "call_analytics_helper":
        query = """ SELECT * FROM call_analytics_helper WHERE telehelp_callid=?"""
    params = [callid]
    ans = readDatabase(db, key, query, params)
    print(ans)
    if ans == []:
        return False
    else:
        return True
    return


def createNewCallHistory(db, key, callid):
    if not callExists(db, key, callid, "call_variables"):
        query = """ INSERT INTO call_variables (callid) values(?) """
        params = [callid]
        writeToDatabase(db, key, query, params)


def writeCustomerAnalytics(db, key, telehelp_callid, columns, params):

    if not callExists(db, key, telehelp_callid, "call_analytics_customer"):
        columnStr = "(" + ",".join(columns) + ")"
        valuesStr = "values(" + "?," * (len(columns) - 1) + "?)"

        query = """ INSERT INTO call_analytics_customer %s %s """ % (columnStr, valuesStr)

        print(query)
        print(params)

    else:
        columnStr = ""
        for i in range(len(columns) - 1):
            columnStr += columns[i] + "=?,"
        columnStr += columns[-1] + "=?"
        query = """ UPDATE call_analytics_customer SET %s
                        where telehelp_callid=?""" % (
            columnStr
        )
        print(query)
        print(params)

    writeToDatabase(db, key, query, params)


def writeHelperAnalytics(db, key, telehelp_callid, columns, params):

    if not callExists(db, key, telehelp_callid, "call_analytics_helper"):
        columnStr = "(" + ",".join(columns) + ")"
        valuesStr = "values(" + "?," * (len(columns) - 1) + "?)"

        query = """ INSERT INTO call_analytics_helper %s %s """ % (columnStr, valuesStr)

        print(query)
        print(params)

    else:
        columnStr = ""
        for i in range(len(columns) - 1):
            columnStr += columns[i] + "=?,"
        columnStr += columns[-1] + "=?"
        query = """ UPDATE call_analytics_helper SET %s
                        where telehelp_callid=?""" % (
            columnStr
        )
        print(query)
        print(params)

    writeToDatabase(db, key, query, params)


if __name__ == "__main__":
    DATABASE_KEY = os.environ.get("DATABASE_KEY")
    # result = readCallHistory(
    #     "telehelp.db", DATABASE_KEY, "c978d94b07cef017b39f4e4b42332b8e6", "current_customer",
    # )

    writeCustomerAnalytics(
        "test.db",
        DATABASE_KEY,
        "b260239e-7d80-11ea-8607-9cb6d098d723",
        ["match_found"],
        ("True", "b260239e-7d80-11ea-8607-9cb6d098d723"),
    )
    # print(result)

    # conn, cursor = create_connection('telehelp.db', DATABASE_KEY)
    # # print(savePostcodeToDatabase('telehelp.db', DATABASSE_KEY, '125', '17070', 'customer'))
    # # print(getCustomers('telehelp.db', DATABASE_KEY)
    # print(userExists('telehelp.db', DATABASE_KEY,'+45674623456', 'helper'))

    # ZIPDATA = 'SE.txt'
    # location_dict, district_dict = readZipCodeData(ZIPDATA)
    # # fetchHelper('telehelp.db', DATABASE_KEY, 'Stockholm', 17070, location_dict)
    # # print(getCustomers('telehelp.db', DATABASE_KEY))

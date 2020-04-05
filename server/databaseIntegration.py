from pysqlcipher3 import dbapi2 as sqlite3
import pandas as pd
from zipcode_utils import *
import os

def create_connection(db_file, key):
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		cursor.execute("PRAGMA key = \"x\'"+key+"\'\"")
	except Error as e:
		print(e)
 
	return conn, cursor


def fetchData(db, key, query, params=None):
	conn, cursor = create_connection(db, key)
	if params==None:
		execute = cursor.execute(query)
	else:
		execute = cursor.execute(query, params)
	data = cursor.fetchall()
	cols = [column[0] for column in execute.description]
	data = pd.DataFrame(data=data, columns = cols)
	conn.close()
	return data

def writeToDatabase(db, key, query, params):
	#try:
	print('Connecting')
	conn, cursor = create_connection(db, key)
	cursor.execute(query, params)
	conn.commit()
	conn.close()
	return 'Success'
	# except Exception as err:
	# 	print(err)
	# 	return 'Failure'  

def readDatabase(db, key, query, params):
	#try:
	conn, cursor = create_connection(db, key)
	cursor.execute(query, params)
	res = cursor.fetchall()
	conn.close()
	return res
	# except Exception as err:
	# 	print(Exception, err)
	# 	return 'Failure'  

def saveHelperToDatabase(db, key, name, phone, zipcode, district):
	print("Writing phone and postcode to database")
	print('\nname: ', name, '\nzipcode:', zipcode, '\nphone: ', phone, '\ndistrict:', district)

	query = ''' INSERT INTO user_helpers (phone, name, zipcode, district) 
									values(?, ?, ?, ?) '''		
	params = (phone, name, zipcode, district)
	flag = writeToDatabase(db, key, query, params)
	print(flag)
	return flag

def saveCustomerToDatabase(db, key, phone, zipcode, district):
	print("Writing phone and postcode to database")
	print('zipcode:', zipcode, '\nphone: ', phone)

	if userExists(db, key, phone, 'customer'):
		query = ''' UPDATE user_customers set district=? where phone=?) '''
		params = (district, phone)
	else:
		query = ''' INSERT INTO user_customers (phone, zipcode, district) 
											values(?, ?, ?) '''		
		params = (phone, zipcode, district)
	flag = writeToDatabase(db, key, query, params)

	print(flag)
	return flag

def userExists(db, key, phone, userType):
	
	if userType == 'customer':
		query = '''SELECT * FROM user_customers WHERE phone = ?'''
	elif userType == 'helper':
		query = '''SELECT * FROM user_helpers WHERE phone = ?'''
	else:
		print('Invalid userType')
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
	if userType == 'customer':
		query = '''DELETE FROM user_customers WHERE phone = ?'''
	elif userType == 'helper':
		query = '''DELETE FROM user_helpers WHERE phone = ?'''
	else:
		print('Invalid userType')
		return
	params = [phone]
	flag = writeToDatabase(db, key, query, params)
	return flag

def getHelpers(db, key):
	query = "SELECT * FROM user_helpers" 
	return fetchData(db, key, query)

def getCustomers(db, key):
	query = "SELECT * FROM user_customers"   
	return fetchData(db, key, query)

def fetchHelper(db, key, district, zipcode, location_dict):
	query = '''SELECT * FROM user_helpers where district=?'''
	params = [district]
	helperData = fetchData(db, key, query, params)
	minDist = None
	distances = []
	phoneNumbers = []
	if helperData.empty:
		print("No helpers found in area")
		return None
	for i in range(len(helperData)):
		phoneNumbers.append(helperData.loc[i, 'phone'])
		distances.append(getDistanceApart(zipcode, helperData.loc[i, 'zipcode'], location_dict))
	zipped = list(zip(phoneNumbers, distances))
	zipped.sort(key = lambda t: t[1])
	sortedNumbers, sortedDistances = zip(*zipped)
	print(list(sortedDistances))
	print(list(sortedNumbers))
	return list(sortedNumbers)


if __name__ == '__main__':
	DATABASE_KEY = os.environ.get('DATABASE_KEY')
	conn, cursor = create_connection('telehelp.db', DATABASE_KEY)
	# print(savePostcodeToDatabase('telehelp.db', DATABASSE_KEY, '125', '17070', 'customer'))
	# print(getCustomers('telehelp.db', DATABASE_KEY)
	print(userExists('telehelp.db', DATABASE_KEY,'+46761423456', 'helper'))
	print(userExists('telehelp.db', DATABASE_KEY,'+45674623456', 'helper'))


	ZIPDATA = 'SE.txt'
	location_dict, district_dict = readZipCodeData(ZIPDATA)
	# fetchHelper('telehelp.db', DATABASE_KEY, 'Stockholm', 17070, location_dict)
	# print(getCustomers('telehelp.db', DATABASE_KEY))

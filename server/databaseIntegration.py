import sqlite3
import pandas as pd

def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
 
	return conn


def fetchData(db, query):
	conn = create_connection(db)
	#cur = conn.cursor() 
	data = pd.read_sql_query(query, conn)
	conn.close()
	return data

def writeToDatabase(db, query, params):
	try:
		conn = create_connection(db)
		cursor = conn.cursor()
		cursor.execute(query, params)
		conn.commit()
		conn.close()
		return 'Success'
	except Exception as err:
		print(err)
		return 'Failure'  

def readDatabase(db, query, params):
	try:
		conn = create_connection(db)
		cursor = conn.cursor()
		cursor.execute(query, params)
		res = cursor.fetchall()
		conn.close()
		return res
	except Exception as err:
		print(Exception, err)
		return 'Failure'  

def saveHelperToDatabase(db, name, phone, zipcode, city):
	print("Writing phone and postcode to database")
	print('\nname: ', name, '\nzipcode:', zipcode, '\nphone: ', phone, '\ncity:', city)

	query = ''' INSERT INTO user_helpers (phone, name, zipcode, city) 
									values(?, ?, ?, ?) '''		
	params = (phone, name, zipcode, city)
	flag = writeToDatabase(db, query, params)
	print(flag)
	return flag

def savePostcodeToDatabase(db, phone, zipcode, userType):
	print("Writing phone and postcode to database")
	print('zipcode:', zipcode, '\nphone: ', phone)
	if userType == 'customer':
		query = ''' INSERT INTO user_customers (phone, zipcode) 
										values(?, ?) '''
	elif userType == 'helper':
		query = ''' INSERT INTO user_helpers (phone, zipcode) 
										values(?, ?) '''		
	params = (phone, zipcode)
	flag = writeToDatabase(db, query, params)
	print(flag)
	return flag

def userExists(db, phone, userType):
	
	if userType == 'customer':
		query = '''SELECT * FROM user_customer WHERE phone = ?'''
	elif userType == 'helper':
		query = '''SELECT * FROM user_helpers WHERE phone = ?'''
	else:
		print('Inavlid userType')
		return
	
	params = [phone]
	ans = readDatabase(db, query, params)
	if ans == []:
		return False
	else:
		return True
	return 
	
	
	
def getHelpers(db='telehelp.db'):
	query = "SELECT * FROM user_helpers"   
	return fetchData(db, query)

def getCustomers(db='telehelp.db'):
	query = "SELECT * FROM user_customers"   
	return fetchData(db, query)


if __name__ == '__main__':
	# print(savePostcodeToDatabase('telehelp.db', '125', '17070', 'customer'))
	# print(getCustomers(db='telehelp.db'))
	print(userExists('telehelp.db', '+46761423456', 'helper'))
	print(userExists('telehelp.db', '+45674623456', 'helper'))


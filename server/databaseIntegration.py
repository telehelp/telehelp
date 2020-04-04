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


def fetchData(query, db):
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
	except:
		return 'Failure'    

def saveHelperToDatabase(db, name, phone, zipcode):
	print("Writing phone and postcode to database")
	print('\nname: ', name, '\nzipcode:', zipcode, '\nphone: ', phone)

	query = ''' INSERT INTO user_helpers (phone, name, zipcode) 
									values(?, ?, ?) '''		
	params = (phone, name, zipcode)
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
	
	
def getHelpers(db='telehelp.db'):
	query = "SELECT * FROM user_helpers"   
	return fetchData(query, db)

def getCustomers(db='telehelp.db'):
	query = "SELECT * FROM user_customers"   
	return fetchData(query, db)


if __name__ == '__main__':
	print(savePostcodeToDatabase('telehelp.db', '125', '17070', 'customer'))
	print(getCustomers(db='telehelp.db'))

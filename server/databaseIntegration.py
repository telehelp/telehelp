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
	except Exception as err:
		print(err)
		return 'Failure'    

def saveHelperToDatabase(db, name, phone, zipcode, district):
	print("Writing phone and postcode to database")
	print('\nname: ', name, '\nzipcode:', zipcode, '\nphone: ', phone, '\ndistrict:', district)

	query = ''' INSERT INTO user_helpers (phone, name, zipcode, district) 
									values(?, ?, ?, ?) '''		
	params = (phone, name, zipcode, district)
	flag = writeToDatabase(db, query, params)
	print(flag)
	return flag

def saveCustomerToDatabase(db, phone, zipcode, district):
	print("Writing phone and postcode to database")
	print('zipcode:', zipcode, '\nphone: ', phone)
	query = ''' INSERT INTO user_customers (phone, zipcode, district) 
										values(?, ?, ?) '''		
	params = (phone, zipcode, district)
	flag = writeToDatabase(db, query, params)
	# if flag == 'Failure':
	# 	query = "update user_customers set district=? where phone=?"
	# 	params = (district, phone)
	# 	flag = writeToDatabase(db, query, params)
	print(flag)
	return flag
	
	
def getHelpers(db='telehelp.db'):
	query = "SELECT * FROM user_helpers"   
	return fetchData(query, db)

def getCustomers(db='telehelp.db'):
	query = "SELECT * FROM user_customers"   
	return fetchData(query, db)

def fetchHelper():
	pass


if __name__ == '__main__':
	print(savePostcodeToDatabase('telehelp.db', '125', '17070', 'customer'))
	print(getCustomers(db='telehelp.db'))

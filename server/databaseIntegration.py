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
    
def getHelpers(db='telehelp.db'):
    query = "SELECT * FROM user_helpers"   
    return fetchData(query, db)

def getCustomers(db='telehelp.db'):
    query = "SELECT * FROM user_customers"   
    return fetchData(query, db)

if __name__ == '__main__':
    getHelpers()

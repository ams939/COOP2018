import psycopg2
import sys

'''Script with functions that provide information or functionalities of a PostgeSQL database.
   This script is used by TableCreator and TableSchemaCreator scripts
'''



def connectDB():
    '''Function for connecting to PostgreSQL database. Database details for the
       whole program can be defined here as other scripts use this function to
       connect to the database. Returns a psycopg2 "connection" object
    '''
    
    #Connect to database, credentials & info seen below
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")
    return connection


def tableExists(table_name):
    '''Function for checking if table exists in database. Table name in DB given
       as argument to function, returns True or False
    '''
    
    #Connect to DB
    connection = connectDB()
    
    #Initialize cursor
    cursor = connection.cursor()
    
    #Create query string for DB query
    query = ("SELECT EXISTS (SELECT 1 AS result FROM pg_tables"
                             " WHERE tablename = '" + table_name + 
                             "')")
    
    #Perform query in database
    cursor.execute(query)
    
    #Access results from query
    tableExists = cursor.fetchone()[0]
    
    #Operations with DB complete, commit changes & close conenction to server
    cursor.close()
    connection.close()
    
    return tableExists



def main():
    '''Main function for testing purposes only
    '''
    #Database table name used for getting info
    table_name = "records2"
    
    if tableExists(table_name):
        print("Table '" + table_name + "' exists.\n")
    else:
        print("Table '" + table_name + "' does not exist")
        sys.exit(0)
    
    
if __name__ == "__main__":
    main()
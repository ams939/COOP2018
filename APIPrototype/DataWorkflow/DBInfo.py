import psycopg2
import sys

'''
    Script with functions that provide information or functionalities of PostgeSQL database.
    This script is used by TableCreator and TableSchemaCreator scripts
'''


'''
    Function for connecting to PostgreSQL database, returns connection object
'''
def connectDB():
    #Connect to database, db name is testdb
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")
    return connection


'''
    Function for checking if table exists in database, returns True or False
'''
def tableExists(table_name):
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


'''
    Main function for testing purposes
'''
def main():
    #Database table name used for getting info
    table_name = "records2"
    
    if tableExists(table_name):
        print("Table '" + table_name + "' exists.\n")
    else:
        print("Table '" + table_name + "' does not exist")
        sys.exit(0)
    
    table_fields = getFields(table_name)
    print(table_fields)
    
    
if __name__ == "__main__":
    main()
import psycopg2
import sys


'''
    Function for connecting to PostgreSQL database
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
    Function that returns list of fields in database table given
''' 
def fieldList(table_name):
    #Connect to DB
    connection = connectDB()
    
    #Initialize DB cursor
    cursor = connection.cursor()
    
    #Query database to find columns it currently contains
    select_command = "SELECT * FROM " + table_name + " LIMIT 0"
    cursor.execute(select_command)
        
    #Make a list if fields in database currently
    table_fields = [desc[0] for desc in cursor.description]
    
    return table_fields


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
    
    table_fields = fieldList(table_name)
    print(table_fields)
    
    
if __name__ == "__main__":
    main()
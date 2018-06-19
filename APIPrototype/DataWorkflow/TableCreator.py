import idigbio
import json
import TableSchemaCreator
from DBInfo import connectDB

'''Program that populates pre-existing database table in a PostgreSQL DB
   with data from an idigbio query, this module is used after the TableSchemaCreator.py
   script on the same idigbio query data to complete the process of inputting the
   data into the database.
'''

def populateTable(result, table_name):
    '''Function that takes idigbio query in dictionary format as argument variable "result"
    and inputs data contained within it into a database table, table name is passed
    to function as argument. Goes through each record in the query, extracts its
    field names & values, then builds them into an insert command, and finally
    executes the command.
    '''
    #Connect to database using DBInfo.py script (Database defined in this script)
    connection = connectDB()
    #Initialize cursor (psycopg2 connection object attribute)
    cursor = connection.cursor()
    
    #Iterate through records in query
    for record in result["items"]:
        #Insert command base string
        insert_base = "INSERT INTO " + table_name + " "
        
        #Command string of list of keys (table field names) to be inserted into database
        insert_keys = "("
        #Command string of list of values (table field values) to be inserted into database
        insert_values = "("
        
        #Create a list of key-value pair tuples from query data
        keys_values = list(record["indexTerms"].items())
        
        #For each pair, append to appropriate command list string 
        for i in range(0, len(keys_values)):
            #Data key, same as database field name
            key = keys_values[i][0]
            
            #Convert values to string format, indexData & geopoint dictionaries stored as json string
            if key == "indexData":
                value = json.dumps(keys_values[i][1])
            elif key == "geopoint":
                value = json.dumps(keys_values[i][1])
            else:
                value = str(keys_values[i][1])
                
            #Replacing single quotes with double single quotes to escape them
            #in query command (avoid mismatching single quotes)
            value = value.replace("'", "''")
            
            #Standardize dates (eliminate timezone & time)
            if key == "datecollected" or key == "datemodified":
                value = value[:10]
            
            #If last entry, leave seperating comma out
            if i == (len(keys_values) - 1):
                insert_keys += "\"" + key + "\")"
                insert_values += "'" + value + "')"
            else:
                insert_keys += "\"" + key + "\", "
                insert_values += "'" + value + "', "
                
        #Build entire command from command strings        
        insert_command = insert_base + insert_keys + " VALUES " + insert_values
        
        #Attempt to execute command in database
        try:
            cursor.execute(insert_command)
        #If command fails, rollback the query and omit given record
        except connection.DataError as e:
            connection.rollback()
            print("There was an error inputting data of record " + record["indexTerms"]["uuid"])
            print("Reason: Field value length out of range. Ommitting record.\n")
            continue
        
        #Commit record to database
        connection.commit()
        
        #Move on to next record
        
    #At this point all records have been processed and inserted into DB    
    print("Database table " + table_name + " has been populated successfully.")
    
    #Operations with DB complete, commit changes & close conenction to server
    cursor.close()
    connection.close()
        

def main():
    '''Main function for testing purposes only
    '''
    #Initialize idigbio API
    api = idigbio.json()
    
    #Define query dictionary
    rq = {"genus":"himantura"}
    
    #Assign query results
    result = api.search_records(rq, limit=5000)
    
    table_name = "stingrays"
    
    #Use query results to create database table with all needed fields
    TableSchemaCreator.createSchema(result, table_name)
    
    #Populate database table with values in query
    populateTable(result, table_name)
    
    
if __name__ == "__main__":
    main()
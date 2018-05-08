import idigbio
import psycopg2
import TableSchemaCreator

'''
    Program that populates database table called "test" (that contains needed fields
    which are created by TableSchemaCreator.py) with data from an idigbio query
'''


'''
    Function that takes idigbio query in dictionary format and inputs data contained
    within it into a database "testdb" table "test"
'''
def createTable(result):
    #Connect to database, db name is testdb
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")
    #Initialize cursor
    cursor = connection.cursor()
    
    #Iterate through records in query
    for record in result["items"]:
        #Inserting values into table 'test'
        insert_base = "INSERT INTO test "
        
        #Command string of list of keys (query field names) to be inserted into database
        insert_keys = "("
        #Command string of list of values (query field values) to be inserted into database
        insert_values = "("
        
        #Create a list of key-value pair tuples from query data
        keys_values = list(record["indexTerms"].items())
        
        #For each pair, append to appropriate command list string 
        for i in range(0, len(keys_values)):
            #Data key, same as database field name
            key = keys_values[i][0]
            
            #Unstandardized data value
            raw_value = str(keys_values[i][1])
            
            #Standardize value data by replacing single quotes with doubles
            value = raw_value.replace("'", '"')
            
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
    print("Database table 'test' has been populated successfully.")
    
    #Operations with DB complete, commit changes & close conenction to server
    cursor.close()
    connection.close()
        

'''
    Main function for testing purposes only
'''
def main():
    #Initialize idigbio API
    api = idigbio.json()
    
    #Define query dictionary
    rq = {"family":"tyrannosauridae"}
    
    #Assign query results
    result = api.search_records(rq, limit=5000)
    
    #Use query results to create database table with all needed fields
    TableSchemaCreator.createSchema(result)
    
    #Populate database table with values in query
    createTable(result)
    
    
if __name__ == "__main__":
    main()
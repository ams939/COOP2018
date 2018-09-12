import urllib.request
import json
import psycopg2
import idigbio
import sys
from DBInfo import connectDB, tableExists

'''Python script for building a table schema for a PostgreSQL database based
on a query result from idigbio. Database details defined in DBInfo.py script's
connectDB() function.
'''


def createSchema(result, table_name):
    '''Function that takes an idigbio query in dict format as argument "result" 
       and creates a database table schema based on based on the fields
       (dictionary keys) present in the query. 
       Goes through field names in each record in the query and adds distinct ones to table
    '''
    #Check that table does not already exist in database
    if tableExists(table_name):
        print("Table '" + table_name + "' already exists.")
        sys.exit(0)
    
    #Connect to database, DB info can be set in DBInfo.py file
    connection = connectDB()

    #Initialize cursor, attribute of psycopg2 "connection" object
    cursor = connection.cursor()
    
    create_command = "CREATE TABLE " + table_name + "()"
    
    #Create a new table in the database
    try:
        cursor.execute(create_command)
        connection.commit()
    except psycopg2.ProgrammingError as e:
        print("Table not created successfully.")
        print(e.pgerror)
        sys.exit()

    #Extract record type data from idigbio API endpoint
    raw_data = urllib.request.urlopen("http://search.idigbio.org/v2/meta/fields/records")

    #Decode data and convert to JSON/ Python dictionary
    record_types_dict = json.loads(raw_data.read().decode())

    #Fields that require special treatment (longer than 200 chars, special type etc.)
    special_fields = ["typestatus", "data", "datecollected", "datemodified", 
                      "indexData", "flags", "recordids", "locality", 
                      "verbatimlocality", "collector", "commonnames", 
                      "mediarecords", "highertaxon", "geopoint"]


    #Iterate through each record in idigbio query result dictionary 
    for record in result["items"]:
        #Query database to find columns it currently contains
        select_command = "SELECT * FROM " + table_name + " LIMIT 0"
        cursor.execute(select_command)
        
        #Make a list of the fields in database currently
        table_fields = [desc[0] for desc in cursor.description]
        
        #Iterate through fields in current record
        for field in record["indexTerms"]:
            #Base string for PSQL column addition command
            add_col = "ALTER TABLE " + table_name + " ADD COLUMN \""
            
            #Handle special case fields (defined in special_fields list)
            if field in special_fields and field not in table_fields:
                '''
                TODO: Change below fields with JSON data type to jsonb type in database
                '''
                #Special case: data field with JSON datastructure (Change later)
                if field == "indexData":
                    add_col += field + "\" TEXT"
                    
                #Special case: Date fields
                elif field == "datecollected":
                    add_col += field + "\" DATE"
                        
                elif field == "datemodified":
                    add_col += field + "\" DATE"
                            
                #Special case: data field with JSON structure (Change to JSON type later)
                elif field == "data":
                    add_col += field + "\" TEXT"
                
                #Other cases treated as strings of unknown length (TEXT)
                else:
                    add_col += field + "\" TEXT"
                
                #Execute command built
                cursor.execute(add_col)
                continue
            
            
            #Handle remaining fields. Check that field doesn't already exist in DB
            if field not in special_fields and field not in table_fields:
                #Extract field's designated type from API data
                field_type = record_types_dict[field]["type"]
            
                #Construct appropriate add command
                if field_type == "string":
                    #CREATE COLUMN VARCHAR 200
                    add_col += field + "\" VARCHAR(200)"
                elif field_type == "float":
                    #CREATE COLUMN DECIMAL
                    add_col += field + "\" DECIMAL"
                elif field_type == "integer":
                    #CREATE COLUMN INTEGER
                    add_col += field + "\" INTEGER"
                elif field_type == "boolean":
                    #CREATE COLUMN BOOLEAN
                    add_col += field + "\" BOOLEAN"
               
                #Handles special types like geopoint etc.
                else:
                    #CREATE COLUMN VARCHAR 200
                    add_col += field + "\" VARCHAR(200)"
            
                #Execute column addition command and save changes to DB
                cursor.execute(add_col)
                continue
        
    
    #Close connection to DB
    connection.commit()
    cursor.close()
    connection.close()
    
    print("Database table " + table_name + " has been created successfully.")
    

   
def main():
    '''Main function for testing purposes only
    ''' 
    #Initialize idigbio API
    api = idigbio.json()
    
    #Define query dictionary
    rq = {"genus":"panthera"}
    
    #Assign query results
    result = api.search_records(rq, limit=30)
    
    table_name = "records1"
    
    #Create database table
    createSchema(result, table_name)
    

if __name__=="__main__":
    main()
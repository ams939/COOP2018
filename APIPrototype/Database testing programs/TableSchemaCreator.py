import urllib.request
import json
import psycopg2
import idigbio

'''
Function that takes an idigbio query result as input and creates a database table
table called "test" based on the fields (dictionary keys) present in the query.
Table created in a PostgreSQL database called testdb
'''
def createSchema(result):
    #Connect to database, db name is testdb
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")

    #Initialize cursor
    cursor = connection.cursor()

    #Create a new table in the database called "test"
    cursor.execute("CREATE TABLE test()")

    #Extract record type data from idigbio API endpoint
    raw_data = urllib.request.urlopen("http://search.idigbio.org/v2/meta/fields/records")

    #Decode data and convert to JSON/ Python dictionary
    record_types_dict = json.loads(raw_data.read().decode())

    #Fields that require special treatment
    special_fields = ["typestatus", "data", "datecollected", "datemodified", 
                      "indexData", "flags", "recordids", "locality", 
                      "verbatimlocality", "collector", "commonnames", 
                      "mediarecords", "highertaxon"]


    #Iterate through each record in query result 
    for record in result["items"]:
        #Query database to find columns it currently contains
        cursor.execute("SELECT * FROM test LIMIT 0")
        
        #Make a list if fields in database currently
        table_fields = [desc[0] for desc in cursor.description]
        
        #Iterate through fields in current record
        for field in record["indexTerms"]:
            #Base string for PSQL column addition command
            add_col = "ALTER TABLE test ADD COLUMN \""
            
            #Handle special case fields (defined in special_fields list)
            if field in special_fields and field not in table_fields:
                '''
                TODO: Change below field to JSON data type
                '''
                #Special case: data field with JSON datastructure (Change later)
                if field == "indexData":
                    add_col += field + "\" TEXT"
                    
                #Special case: Date fields
                elif field == "datecollected":
                    add_col += field + "\" DATE"
                        
                elif field == "datemodified":
                    add_col += field + "\" DATE"
                            
                #Special case: data field with JSON structure (Change later)
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
            
                #Execute column addition command
                cursor.execute(add_col)
                continue
        
        
    print("Database table 'test' has been created successfully.")
    
    #Save changes to DB and close connection
    connection.commit()
    cursor.close()
    connection.close()


'''
    Main function for testing purposes only
'''    
def main():
    #Initialize idigbio API
    api = idigbio.json()
    
    #Define query dictionary
    rq = {"scientificname":"panthera pardus", "country":"india"}
    
    #Assign query results
    result = api.search_records(rq, limit=30)
    
    #Create database table
    createSchema(result)
    

if __name__=="__main__":
    main()
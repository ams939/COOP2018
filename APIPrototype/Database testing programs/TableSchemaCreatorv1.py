import urllib.request
import json
import idigbio
import psycopg2

#Connect to database
connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")

#Initialize cursor
cursor = connection.cursor()

#Create a new table in the database called "test"
cursor.execute("CREATE TABLE test()")

#Initialize JSON version of API
api = idigbio.json()

#Extract record type data from idigbio API endpoint
raw_data = urllib.request.urlopen("http://search.idigbio.org/v2/meta/fields/records")

#Decode data and convert to JSON/ Python dictionary
record_types_dict = json.loads(raw_data.read().decode())

#Query parameters & query
rq = {"scientificname":"panthera pardus", "country":"india"}
result = api.search_records(rq)

#Fields being ignored for the time being
special_fields = ["data", "datecollected", "datemodified", "indexData"]


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
        
        if field in special_fields and field not in table_fields:
            #Special case: Store indexData contents in JSON format within DB
            if field == "indexData":
                add_col += field + "\" JSONB"
        
            #Special case: Date fields
            if field == "datecollected":
                add_col += field + "\" DATE"
            
            if field == "datemodified":
                add_col += field + "\" DATE"
                
            #Special case: data field with JSON datastructure    
            if field == "data":
                add_col += field + "\" JSONB"
            
            #Execute command built
            cursor.execute(add_col)
            continue
            
            
                
        
        #Check that field doesn't already exist in DB
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
               
            #Handles special types like date, geopoint etc.
            else:
               #CREATE COLUMN VARCHAR 200
               add_col += field + "\" VARCHAR(200)"
            
            #Execute column addition command
            cursor.execute(add_col)
            continue
        
        
        
#Save changes to DB and close connection
connection.commit()
cursor.close()
connection.close()
               
        
        
#print(field + " type: " + record_types_dict[field]["type"] + " data length: " + str(len(str(record["indexTerms"][field])))
        





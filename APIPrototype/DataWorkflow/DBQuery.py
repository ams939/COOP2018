import records
import json


'''A module with functions that constructs a query to a PostgreSQL database based on search
   terms defined in a dictionary called "rq", returns results in JSON format.
   This script is used by the APIServer script.
'''


def psqlQuery(rq, limit, table_name):
    '''Returns dict of records from database matching query given in rq dictionary.
       Returned dictionary has keys "itemCount" for record count and "items" for
       list of records returned from query
    '''
    #Connect to the database using URI of form "scheme://username:password@host/dbname
    #Current database name is testdb, username postgres with pw idigbio123
    db = records.Database("postgresql://postgres:idigbio123@localhost/testdb")

    #Begin creation of database query string, records is the table name
    db_query_string = "SELECT * FROM " + table_name + " WHERE "

    #Process rq dictionary, get list of key value tuples
    query_items = list(rq.items())
    
    '''
    TODO: Fix the query building loop, currently query only works for string
    values as the query terms are converted to & compared in lower case form.
    Hence, does not work for integers, booleans, dates etc.
    
    Also field names should be put in double quotes in the query string as DB 
    contains fields with upper case letters.
    
    Ref:
    https://stackoverflow.com/questions/20878932/are-postgresql-column-names-case-sensitive
    '''
    #Build database query string from rq dictionary information
    for item in query_items:
        #If last key-value pair in rq dictionary
        if query_items.index(item) == (len(query_items) - 1):
            db_query_string += "lower(" + item[0] + ")='" + item[1].lower() + "'"
        #Create query string for key-value pairs
        else:
            #Note conversion of value to lowercase and SQL function lower()
            db_query_string += "lower(" + item[0] + ")='" + item[1].lower() + "'" + " AND "
    
    #Add limit to no. of records returned, if provided
    if limit != None:
        db_query_string += " LIMIT " + str(limit)
    
    #Dictionary for results from query
    result = {}
    
    try:
        #Send query to database, response becomes "rows" list of dictionaries
        rows = db.query(db_query_string)
        #Convert rows object to JSON format
        rows_json = rows.dataset.json
    #If db query throws an exception, return error message    
    except Exception:
        err_msg = "Query not successful."
        error_json = {"Error":err_msg} #Return error in dict format
        return error_json
    
    #Convert JSON result to Python dictionary
    rows = json.loads(rows_json)
    
    #Unpack special fields
    for record in rows:
        #Convert indexData field to Python dictionary (stored as json string)
        record["indexData"] = json.loads(record["indexData"])
        
        #Convert geopoint field to dictionary (stored as json string)
        if record["geopoint"] != None:
            record["geopoint"] = json.loads(record["geopoint"])
    
    
    #Add query rows and count to results dictionary
    result["itemCount"] = len(rows)
    result["items"] = rows
    
    #Return query result
    return result



#Function for returning individual record in JSON format from database
def psqlGetRecord(uuid, table_name):
    '''Returns an individual record from database table given using "uuid" to
       query for it.
    '''
    #Connect to database
    db = records.Database("postgresql://postgres:idigbio123@localhost/testdb")
    
    #Create database query string
    db_query_string = "SELECT * FROM " + table_name + " WHERE uuid='" + uuid + "'"
    
    try:
        #Query the database
        row = db.query(db_query_string)
        #Convert result to JSON format and return
        row_json = row.dataset.json
    except Exception:
        err_msg = "Query not successful."
        err_json = {"Error":err_msg}
        return err_json
    
    #Convert to Python dictionary, row_json is array of length 1 with all data at index 0
    result = json.loads(row_json)[0]
    
    #Convert indexData field from json string to python dict
    result["indexData"] = json.loads(result["indexData"])
    
    return result


def main():
    '''Main function for testing purposes only
    '''
    #Test query dictionary
    rq = {
      "scientificname" : "panthera onca"
      }
    table_name = "records"
    #Test uuid
    uuid = "c7c66f6f-52a0-411c-bb2a-460818e87bfe"
    #result = psqlGetRecord(uuid, table_name)
    result = psqlQuery(rq,1, table_name)
    
    print(type(result["items"][0]["indexData"]))
 
    
if __name__ == "__main__":
    main()

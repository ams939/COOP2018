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
        row_json = {"Error":err_msg}
    
    return row_json


def main():
    '''Main function for testing purposes only
    '''
    #Test query dictionary
    rq = {
      "scientificname" : "panthera onca"
      }
    table_name = "records1"
    #Test uuid
    uuid = "816a6cef-e8c6-4606-b57f-1bf17294e29b"
    #result = psqlGetRecord(uuid, table_name)
    result = psqlQuery(rq,1, table_name)
    
    print(result)
 
    
if __name__ == "__main__":
    main()

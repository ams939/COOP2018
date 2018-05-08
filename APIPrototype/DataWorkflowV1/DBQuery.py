import records


'''
    A program that constructs a query to a PostgreSQL database based on search
    terms defined in a dictionary called "rq", returns results in JSON format.
'''


#Function that returns a set of records in JSON format from database
def psqlQuery(rq, limit, table_name):
    #Connect to the database using URI of form "scheme://username:password@host/dbname
    #Current database name is testdb, username postgres with pw idigbio123
    db = records.Database("postgresql://postgres:idigbio123@localhost/testdb")

    #Begin creation of database query string, records is the table name
    db_query_string = "SELECT * FROM " + table_name + " WHERE "

    #Process rq dictionary, get list of key value tuples
    query_items = list(rq.items())

    #Build database query string from rq dictionary information
    for item in query_items:
        if query_items.index(item) == (len(query_items) - 1):
            db_query_string += item[0] + "='" + item[1] + "'"
        else:
            db_query_string += item[0] + "='" + item[1] + "'" + " AND "
    
    #Add limit to no. of records returned, if provided
    if limit != None:
        db_query_string += " LIMIT " + str(limit)
        
    try:
        #Send query to database, response becomes "rows" list of dictionaries
        rows = db.query(db_query_string)
        #Convert rows object to JSON format
        rows_json = rows.dataset.json
        
    except Exception:
        err_msg = "Query not successful."
        rows_json = {"Error":err_msg}
    
    #Return query result in JSON format
    return rows_json



#Function for returning individual record in JSON format from database
def psqlGetRecord(uuid, table_name):
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


'''
    Main function for testing purposes
'''
def main():
    #Test query dictionary
    rq = {
      "scientificname" : "panthera tigris",
      "country" : "india"
      }
    table_name = "records"
    #Test uuid
    uuid = "816a6cef-e8c6-4606-b57f-1bf17294e29b"
    result = psqlGetRecord(uuid, table_name)
    result = psqlQuery(rq,1)
    
    print(result)
 
    
if __name__ == "__main__":
    main()

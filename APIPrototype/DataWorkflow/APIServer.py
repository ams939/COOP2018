import bottle
import json
from DBQuery import psqlQuery, psqlGetRecord
'''Program that starts the API server and defines routes processed by it

   Server address: http://127.0.0.1
'''

#Initialize Bottle application
app = bottle.Bottle()


@app.get("/view/<table>/<uuid>")
def getRecord(table, uuid):
    '''Processes requests for single record, based on "uuid".
       Queries DB table specified in "table" variable, returns
       record in JSON format
       
       Example route: /view/records/47e24c9c-7ebb-417e-acee-be9408a1c297
    '''
    #Assign user given DB table name
    table_name = table
    
    #Get record from DB
    record = psqlGetRecord(uuid, table_name)
    
    return record


@app.get("/<table>/search")
def listing_handler(table):
    '''Processes requests with a query string with rq parameter and optional
       limit parameter.
       Records returned in JSON format.
       
       Example route: /records/search?rq=%7B"scientificname"%3A"panthera tigris"%7D&limit=5
    '''
    #Extracting the rq parameter from query string, JSON string
    rq_string = bottle.request.query.rq
    #Converting to JSON, stored in dictionary rq
    rq = json.loads(rq_string)
    
    #Table name given in URL
    table_name = table
    
    #Extracting limit parameter from query string
    limit = bottle.request.query.limit
    
    if limit == "":
        limit = None
    
    #Querying database with parameters
    matches = psqlQuery(rq, limit, table_name)
    
    return matches

#Start server
bottle.run(app, host = "127.0.0.1", port = 5000, debug = True)
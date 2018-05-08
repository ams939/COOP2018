import bottle
import json
from DBQuery import psqlQuery, psqlGetRecord

app = bottle.Bottle()


#Returning single record based on uuid given
@app.get("/view/<table>/<uuid>")
def getRecord(table, uuid):
    #Assign user given DB table name
    table_name = table
    
    #Get record from DB
    record = psqlGetRecord(uuid, table_name)
    
    return record


#API handler for searching records with rq param & optional limit param
@app.get("/<table>/search")
def listing_handler(table):
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


bottle.run(app, host = "127.0.0.1", port = 5000, debug = True)
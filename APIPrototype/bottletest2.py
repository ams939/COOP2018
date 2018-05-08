from bottle import Bottle, run, get
import bottle
import json



app = Bottle()

'''
#Returns dictionary with request query terms
@app.route("/records/search")
def test_handler():
    #Extracting the rq parameter from query string, JSON string
    #rq_string = bottle.request.query.rq
    #Converting to JSON, stored in dictionary rq
    #rq = json.loads(rq_string)
    
    limit = bottle.request.query.limit
    
    results = {"limit" : limit}
    
    return results

'''
@app.route("/<table>/search")
def test_handler(table):
    #Extracting the rq parameter from query string, JSON string
    #rq_string = bottle.request.query.rq
    #Converting to JSON, stored in dictionary rq
    #rq = json.loads(rq_string)
    
    limit = bottle.request.query.limit
    
    
    
    results = {"limit" : limit, "table":table}
    
    return results

run(app, host = "127.0.0.1", port = 5000, debug = True)
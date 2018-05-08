from bottle import Bottle, run, get
import bottle
import json



app = Bottle()


#Returns dictionary with request query terms
@app.route("/records/search")
def test_handler():
    #Extracting the rq parameter from query string, JSON string
    rq_string = bottle.request.query.rq
    
    rq_dict = bottle.request.query.decode()
    
    #Converting to JSON, stored in dictionary rq
    rq = json.loads(rq_string)
    
    return rq

run(app, host = "127.0.0.1", port = 5000, debug = True)

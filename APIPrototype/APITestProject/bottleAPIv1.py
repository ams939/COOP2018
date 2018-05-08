from bottle import Bottle, run, get
import bottle
import json

#API that returns dictionary with request query terms given in URL

app = Bottle()


@app.route("/records/search")
def test_handler():
    #Extracting the rq parameter from query string, JSON string
    rq_string = bottle.request.query.rq
    #Converting to JSON, stored in dictionary rq
    rq = json.loads(rq_string)
    
    return rq


def runServer():
    run(app, host = "127.0.0.1", port = 5000, debug = True)
    
if __name__ == "__main__":
    runServer()
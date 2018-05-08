import bottle
import json


records = [
    {
         "scientificname" : "Panthera Tigris",
         "family" : "felidae",
         "uuid" : 1234567,
         "countrycode": "IN"
     },
     {
         "scientificname" : "Panthera Leo",
         "family" : "felidae",
         "uuid" : 7891011,
         "countrycode": "KEN"
     },
     { 
         "scientificname" : "Puma Concolor",
         "family" : "felidae",
         "uuid" : 1234567,
         "countrycode": "US"
     },
     {
         "scientificname": "Acinonyx Jubatus",
         "family" : "felidae",
         "uuid" : 54321,
         "countrycode" : "KEN"
     }
]

#Defining endpoint for searching records with rq & limit params
@bottle.get("/records/search")
def listing_handler():
    #Extracting the rq parameter from query string, JSON string
    rq_string = bottle.request.query.rq
    #Converting to JSON, stored in dictionary rq
    rq = json.loads(rq_string)
    
    #Extracting limit parameter from query string
    limit = bottle.request.query.limit
    
    matches = []
    #Querying database with parameters
    for record in records:
        if record["countrycode"] == rq["countrycode"]:
            matches.append(record)
    results = {"items" : matches}
    
    return results


bottle.run(host = "127.0.0.1", port = 5000, debug = True)

    

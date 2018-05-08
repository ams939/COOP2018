import json
from urllib.parse import urlencode
from urllib.parse import parse_qsl

#Function for creating querystring for API URL, takes rq and limit params as args
def qsGenerator(rq, limit=None):
    #Define dictionary that will hold querystring parameters
    qsParameters = {}
    
    #Convert the rq parameter into JSON format
    qsParameters["rq"] = json.dumps(rq)
    
    #If a limit is supplied, add to parameters dictionary
    if limit != None:
        qsParameters["limit"] = limit
    
    #Assemple querystring    
    qs = urlencode(qsParameters)
    
    return qs

#Decodes querystring given as argument, returns dictionary with params
def qsDecoder(qs):
    #Decode URL encoding and create parameter dictionary
    qs_dict = dict(parse_qsl(qs))
    rq = json.loads(qs_dict["rq"]) #Convert rq's string to JSON
    qs_dict["rq"] = rq
    
    return qs_dict
        

def queryURLBuilder(endpoint, rq, limit):
    #Building the querystring from arguments
    qs = qsGenerator(rq, limit)
    
    url = endpoint+qs
    
    return url
    

def main():
    #API's endpoint
    endpoint = "http://127.0.0.1:5000/records/search?"
    
    #Defining user given arguments for API
    rq = {
            "scientificname" : "Puma Concolor",
            #"countrycode" : "KEN",
            #"institution code" : "UTEP",
            #"family" : "felidae"
        }
    limit = None
    
    #Construct the URL
    url = queryURLBuilder(endpoint, rq, limit)
    
    print(url + "\n")
    
    
    #Decoding the URL
    url_components = url.split("?") #Split into endpoint & querystring
    qs = url_components[1] #Seperate querystring
    params = qsDecoder(qs)
    print(params["rq"]["scientificname"])
    
    

if __name__ == "__main__":
    main()
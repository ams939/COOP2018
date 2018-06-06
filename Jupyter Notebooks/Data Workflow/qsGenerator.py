import json
from urllib.parse import urlencode
from urllib.parse import parse_qsl
'''Module for creating an URL with a querystring for an API. Main function
   to be called is queryURLBuilder which takes a base URL, rq dictionary and
   limit as arguments. 
'''


def qsGenerator(rq, limit=None):
    '''Helper function that builds a URL query string, takes rq dictionary
       and limit variable as arguments. Returns URL encoded querystring
    '''
    #Define dictionary that will hold all querystring parameters
    qsParameters = {}
    
    #Replace double quotes with single quotes for JSON conversion of rq dict.
    for key in rq:
        value = rq[key].replace('"', "'")
        rq[key] = value
    
    #Convert the rq parameter into JSON format
    qsParameters["rq"] = json.dumps(rq)
    
    #If a limit is supplied, add to parameters dictionary
    if limit != None:
        qsParameters["limit"] = limit
    
    #Assemple querystring and URL encode it  
    qs = urlencode(qsParameters)
    
    return qs


def qsDecoder(qs):
    '''Function for decoding the rq parameter of a querystring
       *This function has no use in the API currently*
    '''
    #Decode URL encoding and create parameter dictionary
    qs_dict = dict(parse_qsl(qs))
    rq = json.loads(qs_dict["rq"]) #Convert rq's string to JSON
    qs_dict["rq"] = rq
    
    return qs_dict

        
def queryURLBuilder(endpoint, rq, limit):
    '''Function that builds a URL address from base URL and query paramters,
       primary function of this module. Returns URL as string.
    '''
    #Building the querystring from arguments
    qs = qsGenerator(rq, limit)
    
    url = endpoint+qs
    
    return url


def main():
    '''
    Main function, for testing purposes only 
    '''
    #API's endpoint
    endpoint = "http://127.0.0.1:5000/records/search?"
    
    #Defining user given arguments for API
    rq = {
            "scientificname" : "Puma Concolor",
            "countrycode" : "KEN",
            "institution code" : "UTEP",
            "family" : "felidae"
        }
    limit = 5
    
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
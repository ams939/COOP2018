from urllib.request import urlretrieve
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import parse_qsl, parse_qs
import urllib.request
import requests
import json

url_endpoint = "http://127.0.0.1:5000/records/search/?"

#param = quote("Panthera Tigris")
#resp = urllib.request.urlopen(url_endpoint + param)
#data = json.loads(resp.read().decode())
#print(data)

#Querystring parameters
parameters = {
        "rq" : {
                "scientificname" : "Puma Concolor",
                "countrycode" : "US"
               },
        "limit" : "50"
         }

#Converting the "rq" dictionary to JSON format
parameters["rq"] = json.dumps(parameters["rq"])

#Encode mydict into URL        
querystring = urlencode(parameters)
print(querystring + "\n")

#Converting query string back to dictionary
qs_dict = dict(parse_qsl(querystring))
rq = json.loads(qs_dict["rq"]) #Convert rq's string to JSON
qs_dict["rq"] = rq

print(qs_dict["rq"]["scientificname"])


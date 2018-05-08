from urllib.request import urlretrieve
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import parse_qsl, parse_qs
import urllib.request
import requests
import json

url_endpoint = "http://127.0.0.1:5000/records/search/"

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

#Encode mydict into URL        
querystring = urlencode(parameters)
print(querystring + "\n")

#Decode URL back to dictionary format using qsl
qs_dict = dict(parse_qsl(querystring))
#print(qs_dict)

#Decode URL back to dictionary format using qs
qs_dict2 = parse_qs(querystring)
#print(qs_dict2)


#Decode URL back to dictionary format using qsl, decode rq dictionary within
#querystring back to dictionary format using json library
qs_dict3 = dict(parse_qsl(querystring))
rqstring = qs_dict3["rq"].replace("'", "\"" ) #Put string into JSON format
rq = json.loads(rqstring) #Convert string to JSON
qs_dict3["rq"] = rq 
print(qs_dict3["rq"]["scientificname"] + "\n")

print(qs_dict3)

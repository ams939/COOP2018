from qsGenerator import queryURLBuilder
import urllib.request
import json
import sys

#Function that allows user to query database
def searchRecords(rq, limit=None):
    #Endpoint for conducting queries through API with rq search terms
    endpoint = "http://127.0.0.1:5000/records/search?"
    
    #Build query URL using search terms in rq
    url = queryURLBuilder(endpoint, rq, limit)
    
    #Reading data from the URL constructed (requires API Server running)
    try:
        data = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("Invalid URL address.")
        sys.exit(0)
    
    #Convert data read from webpage to JSON format, python dictionary
    result_dict = json.loads(data.read().decode())
    
    return result_dict

def viewRecord(uuid):
    #API Endpoint for retrieving individual record by uuid
    endpoint = "http://127.0.0.1:5000/view/records/"
    
    #URL constructed by appending user defined uuid to endpoint
    url = endpoint + uuid
    
    #Reading data from the URL constructed (requires API Server running)
    try:
        data = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("Invalid URL address.")
        sys.exit(0)
    
    #Converting record to JSON format
    record = json.loads(data.read().decode())
    
    return record

    
    
    
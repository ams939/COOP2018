from qsGenerator import queryURLBuilder
from TableSchemaCreator import createSchema
from TableCreator import populateTable
import idigbio
import urllib.request
import json
import sys


def searchRecords(rq, table_name, limit=None):
    '''Function that returns a dictionary of records found using the rq dictionary
       query parameters. Requires the rq dictionary and database table name as
       arguments, parameter "limit" is optional (limits no. of records retreived) 
    '''
    #Endpoint for conducting queries through API with rq search terms
    endpoint = "http://127.0.0.1:5000/" + table_name + "/search?"
    
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


def viewRecord(uuid, table_name):
    '''Function that returns a single record from database using the record's
       uuid, which is provided as an argument to the function along with the
       name of the table to be queried
    '''
    #API Endpoint for retrieving individual record by uuid
    endpoint = "http://127.0.0.1:5000/view/" + table_name + "/"
    
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

def createTable(rq, table_name, limit=None):
    '''Function that allows user to create a table in a PostgreSQL database
       that contains the results of a query to idigbio.
       
       Takes rq dictionary (containing query params),
       table_name string (name of table to be created in DB) and
       limit int (max no. of records to be returned) as arguments.
    '''
    #Initialize idigbio's API
    api = idigbio.json()
    
    '''
    Change the call to idigbio API to a call to idigbioQuery.py
    '''
    #Conduct query through API
    results = api.search_records(rq, limit)
    
    #Create table & appropriate fields based on query result
    createSchema(results, table_name)
    
    #Enter data in query into table
    populateTable(results, table_name)

    
    
    
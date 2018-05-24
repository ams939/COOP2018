from API import searchRecords, viewRecord

def main():
    rq = {
            "scientificname" : "panthera tigris",
            "country" : "india",
            #"institutioncode" : "amnh",
            #"family" : "felidae",
            #"genus" : "panthera",
            #"recordedby" : "null",
            #"hasimage" : "false",
            #"dataqualityscore": "0.20289"
        }
    
    limit = 1
    uuid = "816a6cef-e8c6-4606-b57f-1bf17294e29b"
    
    table_name = "records1"
    
    #Condcut a query in the database using search terms in rq
    #records_query = searchRecords(rq, table_name, limit)
    #print(records_query)
    
    print("\n\n\n")
    
    #Search for a record in the database
    record = viewRecord(uuid, table_name)
    print(record)
    
if __name__ == "__main__":
    main()
    
    
    
    
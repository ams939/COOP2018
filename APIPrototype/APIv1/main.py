from APIManager import searchRecords, viewRecord

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
    uuid = "053fdcd5-236a-4a1a-9d3e-0b938b1e93f1"
    
    #Condcut a query in the database using search terms in rq
    records_query = searchRecords(rq, limit)
    print(records_query)
    
    print("\n\n\n")
    
    #Search for a record in the database
    #record = viewRecord(uuid)
    #print(record)
    
if __name__ == "__main__":
    main()
    
    
    
    
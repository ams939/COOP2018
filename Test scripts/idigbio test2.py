import idigbio
api = idigbio.json()

def getContacts(uuid):
    record = api.view("records", uuid)
    
    for key in record["attribution"]:
        if key == "contacts":
            print("Contacts:")
            for person in record["attribution"][key]:
                print(person["first_name"] + " " + person["last_name"])

def getSciName(uuid):
    record = api.view("records", uuid)
    
    for key in record["data"]:
        if key == "dwc:acceptedNameUsage":
            print("Scientific Name:")
            print(record["data"][key])
            
                


def main():
    record_list = api.search_records(rq={"country":"mexico"}, limit=5)  
    for item in record_list["items"]:
        uuid = item["uuid"]
        getSciName(uuid)
        getContacts(uuid)
        print()
        
if __name__ == "__main__":
    main()      


        
    
    
    

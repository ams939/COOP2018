import idigbio

'''
Script that conducts user's query to iDigBio using their python API. Takes
a "rq" python dictionary containing the user's search terms as first argument
and an optional "limit" argument which specifies the no. of records returned.
Returns a python dictionary containing the results for the user's query to
iDigBio.

This script is used by the createTable function in the API.py script and it's
main purpose is to augment the iDigBio API by working around its maximum query
size of 5000 records returned. This script will break queries that would return
5000 results into a series of smaller queries.
'''

def idigbioQuery(rq, limit=None):
    #Define API from idigbio library being used
    api = idigbio.json()
        
    #Determine no. of records query would result in
    record_count = api.count_records(rq)
   
    #Case #1: Limit is not given
    if limit == None:
        #Simple case: Query size is smaller than 5k records, return query as is
        if record_count <= 5000:
            results = api.search_records(rq, limit=5000)
            return results
        
        #Complex case: Query larger than 5k, break up query into 5k sized portions
        if record_count > 5000:
            #Records will be sorted by uuid when retrieved as it is unique
            sort = "uuid"
            
            #Defining needed paramteres for offset management
            offset_jump = 5000 #No. of records skipped each query, max. 5000
            offset_count = record_count // offset_jump #No. of offsets needed
            offset = 5000 #The offset parameter passed to idigbio API
            
            #First query, initializing results dictionary
            results = api.search_records(rq, limit=offset_jump, sort=sort)
            
            #Iterate through offsets and perform query
            for i in range(1, offset_count + 1):
                #Conduct query with offset
                query_results = api.search_records(rq, limit=offset_jump, sort=sort, offset=offset)
                
                #Merge offset query results list to results dictionary list
                results["items"].extend(query_results["items"])
                
                #Increment the offset
                offset += offset_jump
                
            return results
        
    #Case #2: Limit has been given
    if limit != None:
        #Simple case: Limit given is below or equal to 5000, return query as is
        if limit <= 5000:
            results = api.search_records(rq, limit)
            return results
        
        #Complex case: Limit given is above 5k
        if limit > 5000:
            print("WIP")
            return {}
        '''
        TODO
        Handle queries with limit given as more than 5k
        '''
        

def main():
    rq = {"family" : "felidae"}
    
    results = idigbioQuery(rq)
    
    print(type(results))
    print(len(results["items"]))
    print(results.keys())

if __name__ == "__main__":
    main()    
        
    
    
    
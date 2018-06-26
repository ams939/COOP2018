import idigbio
'''
This script is used in the API.py script to conduct the user's idigbio query. 
It's main purpose is to augment the iDigBio API by working around its 
maximum query size of 5000 records returned. This script will break queries 
that would return more than 5000 results into a series of smaller queries so
that all of the records wanted are returned to the user.
'''


def idigbioQuery(rq, limit=None):
    '''
    Function that conducts user's query to iDigBio using its python API. Takes
    a "rq" python dictionary containing the user's search terms as first argument
    and an optional "limit" argument which specifies the no. of records returned.
    Returns a python dictionary containing the results for the user's query to
    iDigBio.
    '''
    #Define API from idigbio library being used
    api = idigbio.json()
        
    #Determine no. of records query would result in
    record_count = api.count_records(rq)
   
    '''Case #1: Limit is not given'''
    if limit == None:
        #Simple case: Query size is smaller than 5k records, return query as is
        if record_count <= 5000:
            results = api.search_records(rq, limit=5000)
            return results
        
        #Complex case: Query larger than 5k, break up query into 5k sized portions
        if record_count > 5000:
            #Records will be sorted by uuid to avoid overlapping queries
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
                
                #Iterate to next offset
                offset += offset_jump
                
            return results
        
    '''Case #2: Limit has been given'''
    if limit != None:
        #Simple case: Limit given is below or equal to 5000, return query as is
        if limit <= 5000:
            results = api.search_records(rq, limit)
            return results
        
        #Complex case: Limit given is above 5k
        if limit > 5000:
            #Records will be sorted by uuid to avoid overlapping queries
            sort = "uuid"
            
            #Defining parameters for offset management
            offset_jump = 5000 #No. of records jumped each query
            offset_count = limit // offset_jump #No. of offsets needed
            offset_remainder = limit % offset_jump #Remainder from last offset
            offset = 5000 #Offset parameter passed to idigbio API
            
            #Initial query, offset=0, initialization of results dict
            results = api.search_records(rq, limit=offset_jump, sort=sort)
            
            #Iterate through next offset queries
            for i in range(1, offset_count + 1):   
                if i == (offset_count):
                    #If last offset, query for what is left over based on original limit
                    query_results = api.search_records(rq, limit=offset_remainder, sort=sort, offset=offset)
                else:
                    #Conduct offset queries, starting at offset = 5000
                    query_results = api.search_records(rq, limit=offset_jump, sort=sort, offset=offset)
                    
                #Add the query results to the results dict
                results["items"].extend(query_results["items"])
                
                #Iterate to next offset
                offset += offset_jump
            
            return results
                    
                

def main():
    rq = {"family" : "felidae"}
    
    results = idigbioQuery(rq, limit=45700)
    
    print(type(results))
    print(len(results["items"]))
    print(results.keys())

if __name__ == "__main__":
    main()    
        
    
    
    
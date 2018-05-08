import idigbio

query = {"scientificname":"puma concolor"}

api = idigbio.json()

record_list = api.search_records(rq=query,limit=1)


#prints the genus of each query
#for item in record_list["items"]:
#      for key in item["indexTerms"]:
#          if key == "genus":
#              print(item["indexTerms"][key])


#prints sources in the gbif:reference dictionary
#for item in record_list["items"]:
#   for key in item["indexTerms"]["indexData"]:
#        if key == "gbif:reference":
#            for entry in item["indexTerms"]["indexData"][key]:
#                print(entry["dcterms:source"])



#Prints keys of the "indexData" dictionary
for item in record_list["items"]:
    for term in item["indexTerms"]:
        if term == "indexData":
            for datum in item["indexTerms"]["indexData"]:
                print(datum)







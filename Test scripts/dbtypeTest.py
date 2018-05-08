import idigbio

api = idigbio.json()

rq = {"institutioncode":"amnh"}

result = api.search_records(rq, limit=5000)

ignored = ["indexData", "data", "flags", "recordids", "locality", "verbatimlocality", "typestatus", "mediarecords", "highertaxon"]

for record in result["items"]:
    for field in record["indexTerms"]:
        if len(str(record["indexTerms"][field])) > 200 and field not in ignored:
            print(field)
            #print(record["indexTerms"]["uuid"])
            
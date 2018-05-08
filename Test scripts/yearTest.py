import idigbio

api = idigbio.json()

rq = {"institutioncode":"ANSP"}

result = api.search_records(rq, limit=5000)

file = open("incorrectYears.txt", "w")
count = 0

for record in result["items"]:
    count += 1
    try:
        dateCollected = record["indexTerms"]["datecollected"]
    except KeyError:
        continue
    
    dateCollectedYear = dateCollected[:4]
    
    try:
        year_field = record["indexTerms"]["indexData"]["dwc:year"]
    except KeyError:
        continue
    
    if dateCollectedYear != year_field:
            file.write("%s\n" % record["uuid"])

print(count)

file.close()

    
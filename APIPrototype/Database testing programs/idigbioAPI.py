import idigbio
import re

api = idigbio.json()

results = api.search_records(rq={"scientificname":"panthera pardus", "country":"india"})

record = results["items"][0]

#Fields that will not be read into the DB
excluded_entries = [
        ""
        ]


for field in record["indexTerms"]:
    if field == "indexData":
        for subfield in record["indexTerms"]["indexData"]:
            formatted_fieldname = re.sub("^.*?:","",subfield)
            print(formatted_fieldname)
    formatted_fieldname = re.sub("^.*?:","",field)
    print(formatted_fieldname)

#Getting rid of dwc: and gbif: etc.
#re.sub("^.*?:","",str)
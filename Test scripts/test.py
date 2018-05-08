import idigbio

query = {"country":"United States"}

api = idigbio.json()

record_list = api.search_records(rq=query,limit=1)

for items in record_list["items"]:
    print(items["uuid"])


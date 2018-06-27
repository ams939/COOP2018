import API
import idigbio
from pprint import pformat
import json
from iDigBioQuery import idigbioQuery
'''
Developer script for testing the API
'''
rq = {"genus":"channa"}

table_name = "snakehead"

API.createTable(rq, table_name)
#API.deleteTable(table_name)


'''
# Testing offsets

api = idigbio.json()

rq = {"family":"felidae"}

sort = "uuid"
offset = 50579

results = api.search_records(rq, offset=50579)

print(len(results["items"]))
'''




'''
#Testing true false values in data stored in local DB

uuid = "c7c66f6f-52a0-411c-bb2a-460818e87bfe"
table_name = "records"

result = API.viewRecord(uuid, table_name)

raw_indexData = result["indexData"]

raw_indexData = raw_indexData.replace("True", "true")
raw_indexData = raw_indexData.replace("False", "false")



indexData = json.loads(raw_indexData)

print(indexData)
'''
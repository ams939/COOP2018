import qsGenerator
from urllib.parse import urlencode
import idigbio

#Initialize idigbio's API
api = idigbio.json()

rq = {
      "family":"felidae",
      #"institutioncode":"amnh"
      }

limit = 5000
offset = 0
sort = "uuid"

"""
params = {
        "limit" : 5000,
        "sort" : "uuid",
        "offset" : 4999
        }

qs = qsGenerator.qsGenerator(rq)

qs = qs + "&" + urlencode(params)

print(qs)
"""

#Conduct query through API
results = api.search_records(rq, limit, offset, sort)

limit = 5000
offset = 4990

results2 = api.search_records(rq, limit, offset, sort)

for i in range(4990,5000):
    print(results["items"][i]["uuid"])

print("\n\n\n")
 
for i in range(0, 10):
    print(results2["items"][i]["uuid"])

import urllib.request
import json
import sys

url = "https://raw.githubusercontent.com/vega/vega-datasets/gh-pages/data/world-110m.json"
#Reading data from the URL constructed (requires API Server running)
try:
    data = urllib.request.urlopen(url)
except urllib.error.URLError as e:
    print("Invalid URL address.")
    sys.exit(0)
    
#Convert data read from webpage to JSON format, python dictionary
result_dict = json.loads(data.read().decode())

with open ("data2.json", "w") as outfile:
    json.dump(result_dict, outfile)
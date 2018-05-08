from qsGenerator import queryURLBuilder
import urllib.request
import json
import sys

def main():
    endpoint = "http://127.0.0.1:5000/records/search?"
    
    #Defining user given arguments for API
    rq = {
            "scientificname" : 'Puma" Concolor',
            "countrycode" : "KEN",
            "institution code" : "UTEP",
            "family" : "felidae"
        }
    limit = 5
    
    #Construct the URL
    url = queryURLBuilder(endpoint, rq, limit)
    
    #Reading data from the URL constructed (requires API Server running)
    try:
        data = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("Invalid URL address.")
        print(e)
        sys.exit(0)
    
    #Convert data read from webpage to JSON format
    result_dict = json.loads(data.read().decode())
    
    #Print resulting dictionary
    print(result_dict)
    
if __name__ == "__main__":
    main()

    
    
    
    
    
    
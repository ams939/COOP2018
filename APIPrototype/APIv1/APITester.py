from qsGenerator import queryURLBuilder
import webbrowser
import urllib.request
import json
import sys

#Program for testing how the API works, opens webbrowser pages for results

def main():
    endpoint = "http://127.0.0.1:5000/records/search?"
    endpoint2 = "http://127.0.0.1:5000/view/records/"
    
    #Defining user given arguments for API
    rq = {
            #"scientificname" : "felis catus",
            "country" : "kenya",
            #"institutioncode" : "UTEP",
            #"family" : "felidae"
        }
    
    uuid = "a0cf17b9-9120-4e2e-b798-d3be1dba4020"

    
    limit = None
    
    #Construct the URL
    url = queryURLBuilder(endpoint, rq, limit)
    
    '''
    #Reading data from the URL constructed (requires API Server running)
    try:
        data = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("Invalid URL address.")
        print(e)
        sys.exit(0)
    
    #Convert data read from webpage to JSON format to store it
    result_dict = json.loads(data.read().decode())
    print(result_dict)
    '''
    
    #Open results for rq query in web browser window
    webbrowser.open(url)
    
    #Open results for search by record name in browser
    #webbrowser.open(endpoint2+uuid)
    
if __name__ == "__main__":
    main()

    
    
    
    
    
    
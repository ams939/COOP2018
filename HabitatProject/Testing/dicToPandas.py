import pandas
import sys
sys.path.append(r'C:\Users\ams939\Documents\Python Scripts\APIPrototype\Dataworkflow')

from API import searchRecords

rq = {"scientificname":"lynx canadensis"}
table_name = "lynxcanadensis"

results = searchRecords(rq, table_name)

print(results["itemCount"])

#To create the pandas dataframe from dict data, use this method!
#https://stackoverflow.com/questions/40496008/loop-to-append-multiple-lists-into-dataframe-python?noredirect=1&lq=1


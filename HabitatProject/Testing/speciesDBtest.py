import sys
sys.path.append(r'C:\Users\ams939\Documents\Python Scripts\APIPrototype\Dataworkflow')

from API import createTable

rq = {"genus":"puma", "specificepithet":"concolor", "basisofrecord":"preservedspecimen"}

tablename = "pumaconcolor"

createTable(rq, tablename)
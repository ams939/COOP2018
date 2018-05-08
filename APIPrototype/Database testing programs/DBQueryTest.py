import records

#A program testing connection to the PostgreSQL database

#Connect to the database using URI of form "scheme://username:password@host/dbname
#Current database name is testdb, username postgres with pw idigbio123
db = records.Database("postgresql://postgres:idigbio123@localhost/testdb")

rq = {
      "genus" : "leopardus",
      "country" : "mexico"
      }

#Begin creation of database query string, records2 is table name
db_query_string = "SELECT * FROM records2 WHERE "

#Process rq dictionary, get list of key value tuples
query_items = list(rq.items())

#Build database query string from rq dictionary information
for item in query_items:
    if query_items.index(item) == (len(query_items) - 1):
        db_query_string += item[0] + "='" + item[1] + "'"
    else:
        db_query_string += item[0] + "='" + item[1] + "'" + " AND "
        
#Send query to database, response becomes "rows" list of dictionaries
rows = db.query(db_query_string)

'''
for row in rows:
    print(row["scientificname"])
'''    

#Convert rows object to JSON format and print
print(rows.dataset.json)
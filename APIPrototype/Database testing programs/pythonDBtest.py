import psycopg2

connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")

cursor = connection.cursor()

cursor.execute("CREATE TABLE test()")

'''
cursor.execute("ALTER TABLE test ADD COLUMN uuid VARCHAR(200)")
cursor.execute("INSERT INTO test (uuid) VALUES (1)")
cursor.execute("INSERT INTO test (uuid) VALUES (2)")

cursor.execute("ALTER TABLE test ADD COLUMN number INTEGER")
'''

cursor.execute("SELECT * FROM test LIMIT 0")
columns = [desc[0] for desc in cursor.description]

print(columns)

#Save changes to database
connection.commit()

#Close connection to database
cursor.close()
connection.close()

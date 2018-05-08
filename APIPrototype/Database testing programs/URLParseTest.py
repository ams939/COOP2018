import urllib.parse # import urllib.parse for python 3+

result = urllib.parse.urlparse("field1://username:password@host/database")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

print("database: " + database)
print(result)



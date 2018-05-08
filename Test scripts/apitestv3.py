from flask import Flask
from flask_restful import Api, Resource, reqparse

#Simple API that returns records from "records" dictionary, URL's that can
#be used are http://127.0.0.1:5000/records followed by /scientificname/,
#/family/ or /country/

app = Flask(__name__)
api = Api(app)

#Dictionary that holds test data that API can return
records = [
    {
         "scientificname" : "Panthera Tigris",
         "family" : "felidae",
         "uuid" : 1234567,
         "countrycode": "IN"
     },
     {
         "scientificname" : "Panthera Leo",
         "family" : "felidae",
         "uuid" : 7891011,
         "countrycode": "KEN"
     },
     { 
         "scientificname" : "Puma Concolor",
         "family" : "felidae",
         "uuid" : 1234567,
         "countrycode": "US"
     },
     {
         "scientificname": "Acinonyx Jubatus",
         "family" : "felidae",
         "uuid" : 54321,
         "countrycode" : "KEN"
     }
]



class ScientificName(Resource):
    def get(self, name):
        for record in records:
            if (name == record["scientificname"]):
                return record, 200
        return "Record not found", 404
    
class Family(Resource):
    def get(self, name):
        result = []
        for record in records:
            if name == record["family"]:
                result.append(record)
        return result, 200

class Country(Resource):
    def get(self, name):
        result = []
        for record in records:
            if name == record["countrycode"]:
                result.append(record)
        return result, 200

      
api.add_resource(ScientificName, "/records/scientificname/<string:name>")
api.add_resource(Family, "/records/family/<string:name>")
api.add_resource(Country, "/records/country/<string:name>")

#Delete this & run program to shut down server
app.run(debug=True)

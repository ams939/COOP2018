from flask import Flask
from flask_restful import Api, Resource, reqparse

#Extension to tutorial in apitest.py

app = Flask(__name__)
api = Api(app)

#Test data that API can return
users = [
    {
         "name":"Nicholas",
         "age" : 42,
         "occupation": "Computer Scientist"
    },
    {
         "name": "Elvin",
         "age": 22,
         "occupation": "Data Scientist"
    },
    {
         "name": "Kevin",
         "age": 44,
         "occupation": "Web Developer"
    },
    {
         "name": "Frank",
         "age": 22,
         "occupation": "Web Developer"
    }
]


class UserAge(Resource):
    def get(self, age):
        result = []
        for user in users:
            if age == user["age"]:
                result.append(user)
        return result, 200
        

class User(Resource):
    def get(self, name):
        for user in users:
            if (name == user["name"]):
                return user, 200
        return "User not found", 404
                
    
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200
        
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200

        
api.add_resource(User, "/user/<string:name>")
api.add_resource(UserAge, "/user/age/<int:age>")

#Delete this & run program to shut down server
app.run(debug=True)


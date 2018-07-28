#!/usr/bin/env python

import sys
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


def get_jsondict(json_file):
    """get_jsondict(<json_file>) -> 
    Returns python dictionary object from JSON file"""
    try:
        jc = json.load(open(json_file, 'r'))
    except ValueError:
        print ("error while reading %s" % json_file)
    except AttributeError:
        print ("wrong json syntax : check your syntax in %s" % json_file)
    except Exception, e:
        print str(e)
        sys.exit(0)
    return jc


def put_jsondict(json_file, json_dict):
    """Write back the updated dict to JSON file"""
    with open(json_file, 'w') as f:
        json.dump(json_dict, f)


def get_value(dict, key):
    val = dict.get(key, None)
    if not val:
        print ("%s key not present in the dict, Plz check your conf file" % key)
        sys.exit(1)
    return val


class Person(Resource):
    def get(self, name):
        """get(<name>) -> Returns python dictionary object from JSON file, retrieve a particular person details by specifying the name"""
        if name.isalpha():
            person = get_value(jc, 'person')
            for p in person:
                if(name == p["first_name"]):
                    return p, 200
            return "person not found", 404
        return "Please input the name correctly, it can not be integer/alphanumeric"

    def post(self, name):
        """post(<name>) -> Creates the details of new person and updates the JSON file, returns dictionary of newly created person"""
        person = get_value(jc, 'person')
        parser = reqparse.RequestParser()
        parser.add_argument("last_name", type=str,
                            required=True, help="Can not be left blank")
        parser.add_argument("age", type=int, required=True,
                            help="Can not be left blank and it should be integer")
        parser.add_argument("favourite_colour", type=str,
                            required=True, help="Can not be left blank")
        args = parser.parse_args()

        for p in person:
            if(name == p["first_name"]):
                return "person with name {} already exists".format(name), 400

        if name.isalpha():
            user = {
                "first_name": name,
                "last_name": args["last_name"],
                "age": args["age"],
                "favourite_colour": args["favourite_colour"]
            }
            person.append(user)
            put_jsondict(json_file, jc)
            return user, 201
        else:
            return "Please input the name correctly, it can not be integer/alphanumeric"

    def put(self, name):
        """put(<name>) -> Updates the details of person, or create a new one if it does not exist with corresponding update of JSON file, returns dictionary of newly created/existing person"""
        if name.isalpha():
            parser = reqparse.RequestParser()
            parser.add_argument("last_name", type=str,
                                required=True, help="Can not be left blank")
            parser.add_argument("age", type=int, required=True,
                                help="Can not be left blank and it should be integerger")
            parser.add_argument("favourite_colour", type=str,
                                required=True, help="Can not be left blank")
            args = parser.parse_args()
            person = get_value(jc, 'person')

            for p in person:
                if(name == p["first_name"]):
                    p["last_name"] = args["last_name"]
                    p["age"] = args["age"]
                    p["favourite_colour"] = args["favourite_colour"]
                    put_jsondict(json_file, jc)
                    return p, 200

            user = {
                "first_name": name,
                "last_name": args["last_name"],
                "age": args["age"],
                "favourite_colour": args["favourite_colour"]
            }
            person.append(user)
            put_jsondict(json_file, jc)
            return user, 201
        else:
            return "Please input the name correctly, it can not be integer/alphanumeric"

    def delete(self, name):
        """delet(<name>) -> Deletes the details of person and updates the JSON file respectively"""
        global person
        person = get_value(jc, 'person')
        for p in person:
            if(name == p["first_name"]):
                person = [user for user in person if user["first_name"] != name]
                updated_dict = {'person': person}
                put_jsondict(json_file, updated_dict)
                return "{} is deleted.".format(name), 200
        return "person not found", 404


json_file = sys.argv[1]
jc = get_jsondict(json_file)


api.add_resource(Person, "/person/<string:name>")

#app.run(debug=True)
app.run()
#app.run(host='0.0.0.0', port=8080)

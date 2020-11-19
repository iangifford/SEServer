from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet, Account, Job
import json
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(AccountInfo,"/accountinfo/<string:data>")
    app_api.add_resource(AccountModify,"/accountmodify/<string:data>")
    app_api.add_resource(Login,"/login/<string:data>")
    app_api.add_resource(AccountCreate,"/accountcreate")

class Login(Resource):
    def get(self,data):
        return {"Get":data}
    def post(self,data):
        return {"Post":data}


class AccountModify(Resource):
    def get(self,data):
        return {"Get":data}
    def post(self,data):
        return {"Post":data}

class AccountInfo(Resource):
    def get(self,data):
        try:
            int(data)
        except:
            return "Invalid Account id", 400
        acc = Account.query.filter_by(id=int(data)).first()
        if not acc:
            return "Invalid Account id", 400
        return {"id":acc.id,"type":acc.type, "first_name":acc.first_name,"last_name":acc.last_name,"email":acc.email}
    def post(self,data):
        try:
            int(data)
        except:
            return "Invalid Account id", 400
        acc = Account.query.filter_by(id=int(data))

        return "No post access for this endpoint yet. Get only."

class AccountCreate(Resource):
    create_parser = reqparse.RequestParser()
    create_parser.add_argument('id',type=int)
    create_parser.add_argument('type',type=int)
    create_parser.add_argument('first_name',type=str)
    create_parser.add_argument('last_name',type=str)
    create_parser.add_argument('email',type=str)
    create_parser.add_argument('password',type=str)
    
    def post(self):
        args = self.create_parser.parse_args()
        acc = Account(id = args["id"],type=args["type"],first_name = args["first_name"], last_name = args["last_name"], email = args["email"], password = args["password"])
        db.session.add(acc)
        db.session.commit()
        return "Successfully created account", 201 

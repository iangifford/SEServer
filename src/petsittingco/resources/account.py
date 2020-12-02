from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import sqlite3
from src.petsittingco.database import db, Pet, Account, Job
import json
import uuid
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(AccountInfo,"/accountinfo")
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

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        args = parser.parse_args()
        acc = Account.query.get(int(args["id"]))
        if not acc:
            return {"msg":"Invalid Account id"}, 400
        return {"is_owner":acc.is_owner,"is_sitter":acc.is_sitter,"is_shelter":acc.is_shelter,"is_admin":acc.is_admin, "first_name":acc.first_name,"last_name":acc.last_name,"email":acc.email}, 200


class AccountCreate(Resource):
    parser = reqparse.RequestParser()   
    parser.add_argument('is_owner',type=bool)
    parser.add_argument('is_sitter',type=bool)
    parser.add_argument('is_admin',type=bool)
    parser.add_argument('is_shelter',type=bool)
    parser.add_argument('first_name',type=str)
    parser.add_argument('last_name',type=str)
    parser.add_argument('email',type=str)
    parser.add_argument('password',type=str)
    
    def post(self):
        try:
            created_id = uuid.uuid4()
            args = self.parser.parse_args()
            acc = Account(id =created_id,is_owner = args["is_owner"], is_sitter = args["is_sitter"], is_admin = args["is_admin"], is_shelter = args["is_shelter"], first_name = args["first_name"], last_name = args["last_name"], email = args["email"], password = args["password"])
            db.session.add(acc)
            db.session.commit()
            return {"id":created_id}, 201 
        except:
            return {"msg":"Bad account parameters."}, 400



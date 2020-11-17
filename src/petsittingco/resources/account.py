from flask import Flask, jsonify
from flask_restful import Resource, Api
from database import db, Pet, Account, Job

app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(AccountInfo,"/accountinfo/<string:data>")
    app_api.add_resource(AccountModify,"/accountmodify/<string:data>")
    app_api.add_resource(Login,"/login/<string:data>")

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

        return jsonify(acc)
    def post(self,data):
        try:
            int(data)
        except:
            return "Invalid Account id", 400
        accs = Account.query.filter_by(id=int(data))

        return jsonify(acc)
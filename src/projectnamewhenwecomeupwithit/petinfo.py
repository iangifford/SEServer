from flask import Flask
from flask_restful import Resource, Api

app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(PetInfoEndpoint,"/petinfoendpoint/<string:data>")

class PetInfoEndpoint(Resource):
    def get(self,data):
        return {"Get":data}
    def post(self,data):
        return {"Post":data}
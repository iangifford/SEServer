from flask import Flask, send_from_directory
from flask_restful import Resource, Api

app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(PetInfoEndpoint,"/petinfoendpoint")
    app_api.add_resource(PetCreationEndpoint,"/petcreationendpoint/<string:data>")
    
class PetInfoEndpoint(Resource):
    def get(self):
        return send_from_directory('test_data','petinfoendpoint.json')
    def post(self):
        return {"Post":"data"}



class PetCreationEndpoint(Resource):
    def get(self,data):
        return {"Get":data}
    def post(self,data):
        return {"Post":data}
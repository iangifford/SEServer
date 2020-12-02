from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet, Account, Job
from src.petsittingco.resources.verify_auth import verify_auth
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(PetInfo,"/petinfo")
    app_api.add_resource(PetCreation,"/petcreation")
    #delete pet
    #modify pet

    
    

class PetInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth',type=str)
        #parser add argument for pet id
        args = parser.parse_args()
        if(verify_auth(args["auth"],args["id"])):
            #make sure the pet belongs to the owner

            acc = Account.query.get(str(args["id"]))
            pet = Pet.query.get(asdwadaw)
            if pet.owner == args["id"]
                return json ---> , 200
            return send_from_directory('test_data','petinfoendpoint.json') #{"pet_name":pet.name, "attributes":pet.atributes}
        return "bad pet", 404


class PetCreation(Resource):
    def get(self,data):
        return {"Get":data}
    def post(self,data):
        return {"Post":data}
from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet, Account, Job
from src.petsittingco.resources.verify_auth import verify_auth
import uuid
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(PetInfo,"/petinfo")
    app_api.add_resource(PetCreation,"/petcreation")
    app_api.add_resource(PetList, "/petlist")
    app_api.add_resource(PetModify, "/petmodify")
    app_api.add_resource(PetDelete, "/petdelete")

class PetInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('pet_id',type=str)
        args = parser.parse_args()
        if verify_auth('auth','id'):
            pet = Pet.query.filter_by( args["pet_id"] ).first()
            if pet:
                if pet.owner_id == args["id"]:
                    return { "name":pet.name, "attributes":pet.attributes }, 200
        return 404


class PetCreation(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('name',type=str)
        parser.add_argument('attributes', type=str)
        try:
            args = parser.parse_args()
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination"}, 400
            created_id = uuid.uuid4()
            
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account."}, 400
            pet = Pet(id=str(created_id), owner=acc, name=args["name"],attributes = args["attributes"])
            db.session.add(pet)
            db.session.commit()
            return {"id":str(created_id)}, 201 
        except Exception  as e:
            print(e)
            return {"msg":"Bad pet parameters."}, 400

class PetList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account."}, 400
            pet_array = acc.pets
            pet_dict = {}
            for pet in pet_array:
                pet_dict[pet.id] = pet.name
            print("pet_dict:",pet_dict)
            return pet_dict, 200 
        return 404

class PetModify(Resource):
    def modify(self):
        return 404

class PetDelete(Resource):
    def delete(self):
        return 404 

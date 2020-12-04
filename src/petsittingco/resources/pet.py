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
            pet = Pet.query.filter_by(id=args["pet_id"] ).first()
            if pet:
                if pet.owner_id == args["id"]:
                    return { "name":pet.name, "attributes":pet.attributes,"success":True }, 200
        return {"msg":"Bad Pet ID","success":False}, 400


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
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            created_id = uuid.uuid4()

            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account.","success":False}, 400
            pet = Pet(id=str(created_id), owner=acc, name=args["name"],attributes = args["attributes"])
            db.session.add(pet)
            db.session.commit()
            return {"id":str(created_id),"success":True}, 201 
        except Exception  as e:
            print(e)
            return {"msg":"Bad pet parameters.","success":False}, 400

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
            pet_dict["success"] = True
            print("pet_dict:",pet_dict)
            return pet_dict, 200 
        return {"success":False},404

class PetModify(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('pet_id',type=str)
        parser.add_argument('name',type=str)
        parser.add_argument('attributes', type=str)
        parser.add_argument('auth', type=str)

        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account","success":False}, 400

            pet = Pet.query.get([args["pet_id"]])
            if pet and pet.owner == acc:
                pet.name = args["name"]
                pet.attributes = args["attributes"]

                db.session.commit()
                return {"msg": "Pet Information Modified","success":True}, 200

        return {"msg": "Unable to Modify","success":False}, 400

class PetDelete(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('pet_id',type=str)
        parser.add_argument('auth', type=str)

        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account"}, 400

            pet = Pet.query.get(args["pet_id"])
            if pet:
                db.session.delete(pet)
                db.session.commit()
                return {"msg":"Pet Deleted","success":True}, 200
        return {"msg":"Pet Could Not Be Deleted","success":False}, 400

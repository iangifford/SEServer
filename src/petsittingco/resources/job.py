from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.petsittingco.resources.verify_auth import verify_auth
from src.petsittingco.database import db, Pet, Account, Job
import uuid
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(JobCreation,"/jobcreation")
    app_api.add_resource(JobInfo,"/jobinfo")
    app_api.add_resource(OwnerJobList,"/ownerjoblist")
    app_api.add_resource(SitterJobList,"/sitterjoblist")
    app_api.add_resource(AvailableJobList,"/availablejoblist")
class JobCreation(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('location',type=str)
        parser.add_argument('lat', type=float)
        parser.add_argument('long', type=float)
        parser.add_argument('is_at_owner', type=bool)
        parser.add_argument('start_datetime',type=str)
        parser.add_argument('end_datetime', type=str)
        parser.add_argument('pet_id', type=str)
        parser.add_argument('details', type=str)
        try:
            args = parser.parse_args()
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            job_id = uuid.uuid4()

            owner_acc = Account.query.get( str(args["id"]) )
            pet = Pet.query.get(str(args["pet_id"]))
            if not owner_acc:
                return {"msg":"No Account.","success":False}, 400
            job = Job(
                id = job_id,
                location = args["location"],
                lat = args["lat"],
                long = args["long"],
                is_at_owner = args["is_at_owner"],
                start_datetime = args["start_datetime"],
                end_datetime = args["end_datetime"],
                pet = pet,
                owner = owner_acc,
                accepted = False,
                canceled = False,
                details = args["details"]
            )
            db.session.add(job)
            db.session.commit()
            return {"job_id":str(job_id),"success":True}, 201 
        except Exception  as e:
            print(e)
            return {"msg":"Bad job parameters.","success":False}, 400
    
class JobInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('job_id',type=str)
        args = parser.parse_args()
        if verify_auth('auth','id'):
            job = Job.query.get(id=args["job_id"])
            if job:
                if job.owner_id == args["id"] or job.sitter_id == args["id"]:
                    jobinfo = {
                        "location":job.location,
                        "lat":job.lat,
                        "long":job.long,
                        "is_at_owner":job.is_at_owner,
                        "start_datetime":job.start_datetime,
                        "end_datetime":job.end_datetime,
                        "pet_id":job.pet_id,
                        "accepted":job.accepted,
                        "canceled":job.canceled,
                        "details":job.details,
                        "success":True
                    }
                    owner_acc = Account.query.get(id = job.owner_id)
                    jobinfo["owner_name"] = owner_acc.first_name
                    if job.accepted:
                        sitter_acc = Account.query.get(id = job.sitter_id)
                        jobinfo["sitter_name"] = sitter_acc.first_name
                    else:
                        jobinfo["sitter_name"] = "No Sitter"
                    return jobinfo, 200
        return {"msg":"Bad Job ID","success":False}, 400



class OwnerJobList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('is_accepted', type=bool)
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account."}, 400
            job_array = acc.owner_jobs
            job_dict = {}
            for job in job_array:
                sitter = Job.query.get(job.sitter_id)
                sitter_name = ""
                if sitter:
                    sitter_name = sitter.first_name
                else:
                    sitter_name = "No Sitter"
                if job.accepted == args["is_accepted"]:
                    job_dict[job.id] = {"sitter_name":sitter_name, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404

class SitterJobList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('is_canceled', type=bool)
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account."}, 400
            job_array = acc.sitter_jobs
            job_dict = {}
            for job in job_array:
                owner = Job.query.get(job.owner_id)
                owner_name = owner.first_name
                if job.canceled == args["is_canceled"]:
                    job_dict[job.id] = {"owner_name":owner_name, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404

class AvailableJobList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            job_array = Job.query.all()
            job_dict = {}
            for job in job_array:
                owner = Job.query.get(job.owner_id).owner
                owner_name = owner.first_name
                if not (job.accepted or job.canceled):
                    job_dict[job.id] = {"location":job.location,"owner_name":owner_name,"pet_id":job.pet_id, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404
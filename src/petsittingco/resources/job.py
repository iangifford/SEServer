from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse,inputs

from src.petsittingco.resources.verify_auth import verify_auth
from src.petsittingco.database import db, Pet, Account, Job
import uuid

from math import sin, cos, sqrt, atan2, radians
app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(JobCreation,"/jobcreation")
    app_api.add_resource(JobInfo,"/jobinfo")
    app_api.add_resource(OwnerJobList,"/ownerjoblist")
    app_api.add_resource(SitterJobList,"/sitterjoblist")
    app_api.add_resource(AvailableJobList,"/availablejoblist")
    app_api.add_resource(JobSearch, "/jobsearch")
    app_api.add_resource(JobModify, "/jobmodify")
    app_api.add_resource(JobDelete, "/jobdelete")
    app_api.add_resource(JobAccept, "/jobaccept")
class JobCreation(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('location',type=str)
        parser.add_argument('lat', type=float)
        parser.add_argument('long', type=float)
        parser.add_argument('is_at_owner', type=inputs.boolean)
        parser.add_argument('start_datetime',type=str)
        parser.add_argument('end_datetime', type=str)
        parser.add_argument('details', type=str)

        try:
            args = parser.parse_args()
            print("id:",args["id"])
            print("auth:",args["auth"])
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            job_id = str(uuid.uuid4())

            owner_acc = Account.query.get( str(args["id"]) )
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
            print("Bad Job Parameters")
            return {"msg":"Bad job parameters.","success":False}, 400
    
class JobInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('job_id',type=str)
        args = parser.parse_args()
        if verify_auth('auth','id'):
            job = Job.query.get(args["job_id"])
            if job:
                print("job exists")
                if job.owner_id == args["id"] or job.sitter_id == args["id"]:
                    jobinfo = {
                        "location":job.location,
                        "lat":job.lat,
                        "long":job.long,
                        "is_at_owner":job.is_at_owner,
                        "start_datetime":job.start_datetime,
                        "end_datetime":job.end_datetime,
                        "accepted":job.accepted,
                        "canceled":job.canceled,
                        "details":job.details,
                        "success":True
                    }
                    print(jobinfo)
                    print("getting owner name")
                    jobinfo['owner_name'] = str(job.owner.first_name)
                    if job.accepted:
                        sitter_acc = Account.query.get(job.sitter_id)
                        jobinfo['sitter_name'] = sitter_acc.first_name
                    else:
                        jobinfo['sitter_name'] = str("No Sitter")
                    print("returning")
                    return jobinfo, 200
        return {"msg":"Bad Job ID","success":False}, 400



class OwnerJobList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('is_accepted', type=inputs.boolean)
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            acc = Account.query.get( str(args["id"]) )
            if not acc:
                return {"msg":"No Account."}, 400
            job_array = acc.owner_jobs
            job_dict = {}
            for job in job_array:
                print(job)
                if job.sitter_id:
                    sitter = Account.query.get(job.sitter_id)
                    sitter_name = sitter.first_name
                else:
                    sitter_name = "No Sitter"
                
                if job.accepted == args["is_accepted"] and not job.canceled:
                    job_dict[job.id] = {"sitter_name":sitter_name, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
                else:
                    print("bad job")
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404

class SitterJobList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('is_canceled', type=inputs.boolean)
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
                owner = job.owner
                owner_name = owner.first_name
                if not (job.accepted or job.canceled):
                    job_dict[job.id] = {"location":job.location,"owner_name":owner_name, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404

class JobSearch(Resource):
    MAX_DISTANCE = 50
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('lat',type=float)
        parser.add_argument('lon',type=float)
        
        args = parser.parse_args()
        if verify_auth(args['auth'],args['id']):
            job_array = Job.query.all()
            job_dict = {}
            for job in job_array:
                owner = owner = job.owner
                owner_name = owner.first_name
                if not (job.accepted or job.canceled):
                    if type(job.lat) is float and type(job.lon) is float:
                        if calc_lat_long_distance(job.lat, job.long, args["lat"], args["lon"]) <= self.MAX_DISTANCE:
                            job_dict[job.id] = {"location":job.location, "start_datetime":job.start_datetime, "end_datetime":job.end_datetime}
            job_dict["success"] = True
            print("job_dict:",job_dict)
            return job_dict, 200 
        return {"success":False},404

def calc_lat_long_distance(lat1, lon1, lat2, lon2):
    earth_radius = 3958.8

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c

    return distance

class JobModify(Resource):
    def put(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('location',type=str)
        parser.add_argument('lat', type=float)
        parser.add_argument('long', type=float)
        parser.add_argument('is_at_owner', type=inputs.boolean)
        parser.add_argument('start_datetime',type=str)
        parser.add_argument('end_datetime', type=str)
        parser.add_argument('details', type=str)
        parser.add_argument('job_id', type=str)

        try:
            args = parser.parse_args()
            print("id:",args["id"])
            print("auth:",args["auth"])
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            job = Job.query.get(args["job_id"])
            if not job or not job.owner_id == args["id"]:
                return {"msg":"User does not own a job of that id", "success":False}, 404
            job.location = args["location"]
            job.lat = args["lat"]
            job.long = args["long"]
            job.is_at_owner = args["is_at_owner"]
            job.start_datetime = args["start_datetime"]
            job.end_datetime = args["end_datetime"]
            job.details = args["details"]
    
            db.session.commit()
            return {"success":True}, 201 
        except Exception  as e:
            print(e)
            print("Bad Job Parameters")
            return {"msg":"Bad job parameters.","success":False}, 400

class JobDelete(Resource):
    def delete(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('job_id', type=str)

        try:
            args = parser.parse_args()
            print("id:",args["id"])
            print("auth:",args["auth"])
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            job = Job.query.get(args["job_id"])
            if not job or not job.owner_id == args["id"]:
                return {"msg":"User does not own a job of that id", "success":False}, 404
            job.canceled = True
            db.session.commit()
            return {"success":True}, 201 
        except Exception  as e:
            print(e)
            print("Bad Job Parameters")
            return {"msg":"Bad job parameters.","success":False}, 400

class JobAccept(Resource):
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('job_id', type=str)

        try:
            args = parser.parse_args()
            print("id:",args["id"])
            print("auth:",args["auth"])
            if not verify_auth(args["auth"],args["id"]):
                return {"msg":"Bad ID/Auth combination","success":False}, 400
            job = Job.query.get(args["job_id"])
            if not job or job.accepted or job.canceled:
                return {"msg":"Invalid job to accept", "success":False}, 404
            user = Account.query.get(args["id"])
            if not user:
                return {"msg": "Bad sitter","success":False}, 400
            job.accepted = True
            job.sitter = user
            db.session.commit()
            return {"success":True}, 201 
        except Exception  as e:
            print(e)
            print("Bad Job Parameters")
            return {"msg":"Bad job parameters.","success":False}, 400
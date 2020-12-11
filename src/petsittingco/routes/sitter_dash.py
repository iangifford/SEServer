from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet, Account, Job
import json 


sitter_blueprint = Blueprint("sitter","__sitter__")

@login_required
@sitter_blueprint.route('/petsitterdashboard/joblistings', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/joblistings.html', methods=['GET'])
def jobs():
    jobs = ""
    
    job_array = Job.query.all()

    for job in job_array:
        if not job.canceled and not job.accepted:
            jobs += '<div class="row"><h3 style="text-align: center">Job for ' + job.owner.first_name + ' on ' + job.start_datetime +  '</h3></div><div class="row"><button onclick="document.location=\'../petsitterdashboard/accept.html?job_id=' + job.id + '\'"  id="submit-button" class="custom-btn btn-bg btn mt-3" data-aos-delay="300" >Accept Job</button> </div><br>'

    return render_template("petsitterdashboard/joblistings.html", job_list=jobs)

@login_required
@sitter_blueprint.route('/petsitterdashboard/accept', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/accept.html', methods=['GET'])
def accept():
    message = ""
    parser = reqparse.RequestParser()
    parser.add_argument('job_id',type=str)

    args = parser.parse_args()

    job = Job.query.get(args["job_id"])
    if not job:
        message += "This Job could not be accepted."
    else:
        job.accepted = True
        job.sitter = current_user
        db.session.commit()
        message += "Job successfully accepted."
    
    return render_template('/petsitterdashboard/accept.html', job_accept_message=message)

@login_required
@sitter_blueprint.route('/petsitterdashboard/job', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/job', methods=['GET'])
def job():
    parser = reqparse.RequestParser()
    parser.add_argument('job_id',type=str)

    args = parser.parse_args()

    job = Job.query.get(args["job_id"])
    if not job:
        job_details = "This Job could not be found."
    else:
        pets = job.owner.pets
        petstring = ""
        for pet in petstring:
            petstring +='<p style="text-indent: 40px">' + pet.name + '</p>'
        job_details = '<div class="row">Owner Name: ' + job.owner.first_name + '<br>Start date and time: '+job.start_datetime + '<br>End date and time: ' + job.end_datetime + '<br>Pets: <br>' + petstring + '</div>'
        
        
        
        
        
    
    return render_template('/petsitterdashboard/job.html', job=job_details)

@sitter_blueprint.route('/petsitterdashboard/dashboard.html', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/dashboard', methods=['GET'])
@login_required
def pet_sitter_dashboard():
    return render_template("petsitterdashboard/dashboard.html")

@login_required
@sitter_blueprint.route('/petsitterdashboard/acceptedjobs', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/acceptedjobs.html', methods=['GET'])
def accepted_jobs():
    jobs = ""
    job_array = Job.query.all()

    for job in job_array:
        if job.sitter == current_user and not job.canceled:
            jobs += '<div class="row"><h3 style="text-align: center">Job for ' + job.owner.first_name + ' on ' + job.start_datetime +  '</h3></div><div class="row"><button onclick="document.location=\'../petsitterdashboard/job.html?job_id=' + job.id + '\'"  id="submit-button" class="custom-btn btn-bg btn mt-3" data-aos-delay="300" >View Job Details</button> </div><br>'

    return render_template("petsitterdashboard/acceptedjobs.html", job_list=jobs)

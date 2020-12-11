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
            jobs += '<div class="row"><h3 style="text-align: center">Job for ' + job.owner.first_name + ' on ' + job.start_datetime +  '</h3></p></div><div class="row"><button onclick="document.location=\'../petsitterdashboard/accept.html?job_id=' + job.id + '\'"  id="submit-button" class="custom-btn btn-bg btn mt-3" data-aos-delay="300" >Accept Job</button> </div><br>'

    return render_template("petsitterdashboard/joblistings.html", job_list=jobs)
"""
@login_required
@pet_blueprint.route('/petownerdashboard/delete', methods=['GET'])
@pet_blueprint.route('/petownerdashboard/delete.html', methods=['GET'])
def delete_pet():
    message = ""
    parser = reqparse.RequestParser()
    parser.add_argument('pet_id',type=str)

    args = parser.parse_args()

    pet = Pet.query.get(args["pet_id"])
    if not pet:
        message += "This Pet Could not Be Deleted."
    print("bad pet")
    if pet:
        if current_user == pet.owner:
            db.session.delete(pet)
            db.session.commit()
            message += "Pet Has Been Deleted."
        print("Bad owner")
    
    return render_template('/petownerdashboard/delete.html', delete_pet_message=message)
"""

@sitter_blueprint.route('/petsitterdashboard/dashboard.html', methods=['GET'])
@sitter_blueprint.route('/petsitterdashboard/dashboard', methods=['GET'])
def pet_sitter_dashboard():
    return render_template("petsitterdashboard/dashboard.html")


from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import InputRequired, Length
from src.petsittingco.database import db, Pet, Account, Job
import json 
import uuid


owner_jobs_blueprint = Blueprint("owner_jobs","__owner_jobs__")

@owner_jobs_blueprint.route('/petownerdashboard/joblistings', methods=['GET'])
@owner_jobs_blueprint.route('/petownerdashboard/joblistings.html', methods=['GET'])
@login_required
def jobs():
    jobs = ""
    
    job_array = Job.query.all()

    for job in job_array:
        if not job.canceled and job.owner == current_user:
            if job.accepted:
                sitter_name = "Job sat by " + job.sitter.first_name
            else:
                sitter_name = 'Job with no sitter'
            jobs += '<div class="row"><h3 style="text-align: center">Job sat by ' + job.sitter.first_name + ' on ' + job.start_datetime +  '</h3></div><div class="row"><button onclick="document.location=\'../petownerdashboard/job.html?job_id=' + job.id + '\'"  id="submit-button" class="custom-btn btn-bg btn mt-3" data-aos-delay="300" >View Job</button> </div><br>'

    return render_template("petownerdashboard/joblistings.html", job_list=jobs)

@login_required
@owner_jobs_blueprint.route('/petownerdashboard/job', methods=['GET'])
@owner_jobs_blueprint.route('/petownerdashboard/job.html', methods=['GET'])
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
        for pet in pets:
            petstring +=pet.name + "<br>"
        if job.accepted:
            sitter_name = job.sitter.first_name
        else:
            sitter_name = "No Sitter"
        job_details = '<div class="row"><p>Owner Name: ' + job.owner.first_name + '<br>Start date and time: '+job.start_datetime + '<br>End date and time: ' + job.end_datetime + '<br>Sitter: ' + sitter_name + '<br>Job details: ' + job.details + '</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p><br><p>Pets: <br>' + petstring + '</p></div>'
    return render_template('/petownerdashboard/job.html', job=job_details)

class RegisterForm(FlaskForm):
    loc = StringField('Location', validators = [InputRequired()])
    is_at_owner = BooleanField("At your place?", validators = [])
    start_datetime = StringField("Start Date + Time (MM/DD/YYYY HH:MM)", validators = [InputRequired()])
    end_datetime = StringField("End Date + Time (MM/DD/YYYY HH:MM)", validators = [InputRequired()])
    details = StringField("Extra Details?")

    
@login_required
@owner_jobs_blueprint.route('/petownerdashboard/createjob', methods=['GET', 'POST'])
@owner_jobs_blueprint.route('/petownerdashboard/createjob.html', methods=['GET', 'POST'])
def job_forms():
    form = RegisterForm()

    if form.validate_on_submit():
        
        new_job = Job(id=str(uuid.uuid4()), owner_id=current_user.id, location = form.loc.data, is_at_owner = form.is_at_owner.data, lat = 0, long = 0, start_datetime = form.start_datetime.data, end_datetime = form.end_datetime.data, details = form.details.data)
        db.session.add(new_job)
        db.session.commit()

        return redirect('/petownerdashboard/jobs.html')
    return render_template('/petownerdashboard/createjob.html', job_form=form )
    
@owner_jobs_blueprint.route('/petownerdashboard/dashboard.html', methods=['GET'])
@owner_jobs_blueprint.route('/petownerdashboard/dashboard', methods=['GET'])
def pet_owner_dashboard():
    return render_template("petownerdashboard/dashboard.html")


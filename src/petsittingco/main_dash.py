from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse


button_blueprint = Blueprint("buttons","__buttons__")

@button_blueprint.route('/main_dashboard', methods=['GET'])
@button_blueprint.route('/main_dashboard.html', methods=['GET'])
def main_dashboard():
    all_buttons = ""
    # Owner
    if current_user.is_owner:
        all_buttons += '<form action="petownerdashboard/dashboard.html" method="get" class="contact-form" data-aos-delay="300" role="form"> <div class="row"> <button class="form-control custom-btn" id="submit-button" >Owner Dashboard</button> </div> </form>'
    # Sitter
    if current_user.is_sitter:
        all_buttons += '<form action="petsitterdashboard/dashboard.html" method="get" class="contact-form" data-aos-delay="300" role="form"> <div class="row"> <button class="form-control custom-btn" id="submit-button" >Sitter Dashboard</button> </div> </form>'
    # Shelter
    if current_user.is_shelter:
        all_buttons += '<form action="shelterdashboard/dashboard.html" method="get" class="contact-form" data-aos-delay="300" role="form"> <div class="row"> <button class="form-control custom-btn" id="submit-button" >Shelter Dashboard</button> </div> </form>'
    #Admin
    if current_user.is_admin:
        all_buttons += '<a href="admindashboard/dashboard.html" class="custom-btn btn-bg btn mt-3" data-aos-delay="100">Admin Dashboard</a>'
    # No Roles 
    if current_user.is_owner == False and current_user.is_sitter == False and current_user.is_shelter == False and current_user.is_admin == False:
        all_buttons += '<p> Did Not Choose Any Roles. Please Modify Account.</p>'
    return render_template("main_dashboard.html", buttons=all_buttons)





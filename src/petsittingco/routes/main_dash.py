from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse


button_blueprint = Blueprint("buttons","__buttons__")


@button_blueprint.route('/main_dashboard', methods=['GET'])
@button_blueprint.route('/main_dashboard.html', methods=['GET'])
@login_required
def main_dashboard():
    all_buttons = ""
    # Owner
    if current_user.is_owner:
        all_buttons += '<a href="../petownerdashboard/dashboard.html" class="custom-btn btn-bg btn mt-3" data-aos-delay="100">Owner Dashboard</a><br>'
    # Sitter
    if current_user.is_sitter:
        all_buttons += '<a href="../petsitterdashboard/dashboard.html" class="custom-btn btn-bg btn mt-3" data-aos-delay="100">Sitter Dashboard</a><br>'
    # Shelter
    if current_user.is_shelter:
        all_buttons += '<a href="../shelter" class="custom-btn btn-bg btn mt-3" data-aos-delay="100">Shelter Dashboard</a><br>'
    #Admin
    if current_user.is_admin:
        all_buttons += '<a href="../admin" class="custom-btn btn-bg btn mt-3" data-aos-delay="100">Admin Dashboard</a><br>'
    # No Roles 
    if current_user.is_owner == False and current_user.is_sitter == False and current_user.is_shelter == False and current_user.is_admin == False:
        all_buttons += '<p> Did Not Choose Any Roles. Please Modify Account.</p>'
    return render_template("main_dashboard.html", buttons=all_buttons)





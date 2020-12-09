from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet


pet_blueprint = Blueprint("pets","__pets__")

@pet_blueprint.route('/petownerdashboard/pets', methods=['GET'])
@pet_blueprint.route('/petownerdashboard/pets.html', methods=['GET'])
def pets():
    pets = ""
    user_pet_array = current_user.pets
    if not user_pet_array:
        pets += '<p> You Have No Pets Yet. Add Some Pets! </p>'

    for pet_info in user_pet_array:
        pets += '<p> <br>' + pet_info.name + '<br>' + pet_info.attributes + '<br> </p>'

    return render_template("petownerdashboard/pets.html", pet_list=pets)


@pet_blueprint.route('/petownerdashboard/dashboard.html', methods=['GET'])
@pet_blueprint.route('/petownerdashboard/dashboard', methods=['GET'])
def pet_owner_dashboard():
    return render_template("petownerdashboard/dashboard.html")


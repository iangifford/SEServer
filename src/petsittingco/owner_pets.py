from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet


pet_blueprint = Blueprint("pets","__pets__")

@pet_blueprint.route('/pets', methods=['POST'])
@pet_blueprint.route('/pets.html', methods=['POST'])
def pets():
    pets = ""
    user_pet_array = current_user.pets
    if not user_pet_array:
        pets += "You Have No Pets Yet. Add Some Pets!"

    for pet_info in user_pet_array:
        pets += "<br>" + pet_info.name + "<br>" + pet_info.attributes + "<br>"

    return render_template("pets.html", pet_list=pets)

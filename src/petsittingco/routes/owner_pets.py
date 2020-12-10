from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet, Account
import json 


pet_blueprint = Blueprint("pets","__pets__")

@pet_blueprint.route('/petownerdashboard/pets', methods=['GET'])
@pet_blueprint.route('/petownerdashboard/pets.html', methods=['GET'])
def pets():
    pets = ""
    
    user_pet_array = current_user.pets
    if not user_pet_array:
        pets += '<p> You Have No Pets Yet. Add Some Pets! </p>'

    for pet_info in user_pet_array:
        pet_temp_dict = json.loads(pet_info.attributes)
        pets += '<p> <br> Pet Name: ' + pet_temp_dict["pet_name"] + '<br> Pet Type: ' + pet_temp_dict["other_type"] + '<br> Attributes: '
        if pet_temp_dict["energetic"]:
            pets += '<br> This Pet is Energetic <br>'
        if pet_temp_dict["noisy"]:
            pets += '<br> This Pet is Noisy <br>'
        if pet_temp_dict["trained"]:
            pets += '<br> This Pet is Trained<br>'
        pets += '<br> Other Info: ' + pet_temp_dict["other_info"] + '<br></p><button onclick="document.location=\'../petownerdashboard/delete.html?pet_id=' + pet_info.id + '\'"  class="contact-form" data-aos-delay="300" >Delete Pet</button> <br>'

    pets += '<br> <form action="../petownerdashboard/pet_forms.html" method="get" class="contact-form" data-aos-delay="300" role="form"> <div class="col-lg-5 mx-auto col-1"> <div class="row"> <button class="form-control" id="submit-button" >Create Pet</button> </div> </div> </form> <br> <form action="../petownerdashboard/change_pet.html" method="get" class="contact-form" data-aos-delay="300" role="form"> <div class="col-lg-5 mx-auto col-1"> <div class="row"> <button class="form-control" id="submit-button" >Modify Pet</button> </div> </div> </form><br>'
    return render_template("petownerdashboard/pets.html", pet_list=pets)

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
    

@pet_blueprint.route('/petownerdashboard/dashboard.html', methods=['GET'])
@pet_blueprint.route('/petownerdashboard/dashboard', methods=['GET'])
def pet_owner_dashboard():
    return render_template("petownerdashboard/dashboard.html")


from wtforms import BooleanField, StringField
from flask_wtf import FlaskForm
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet
from wtforms.validators import InputRequired, Length
import uuid
import json

pet_form_blueprint = Blueprint("pet_forms","__pet_forms__")

class RegisterForm(FlaskForm):
    pet_name = StringField('Pet Name', validators=[InputRequired(), Length(min=4,max=64)])

    pet_type = StringField(' Animal ', validators=[InputRequired()] )
    is_energetic = BooleanField('Energetic?')

    is_noisy = BooleanField('Noisy?')
    is_trained = BooleanField('Trained?')
    other_info = StringField('Other Information', validators=[InputRequired(), Length(min=0,max=200)])

@login_required
@pet_form_blueprint.route('/petownerdashboard/pet_forms', methods=['GET', 'POST'])
@pet_form_blueprint.route('/petownerdashboard/pet_forms.html', methods=['GET', 'POST'])
def pet_forms():
    form = RegisterForm()

    if form.validate_on_submit():
        pet_attr_dict = {} 
   
        pet_attr_dict = {"pet_name":form.pet_name.data, "pet_type":"", "other_type":form.pet_type.data, "energetic":form.is_energetic.data,  "noisy":form.is_noisy.data, "trained":form.is_trained.data, "other_info":form.other_info.data} 

        new_pet = Pet(id=str(uuid.uuid4()), owner_id=current_user.id, name=form.pet_name.data, attributes=json.dumps(pet_attr_dict))
        db.session.add(new_pet)
        db.session.commit()

        return redirect('/petownerdashboard/pets.html')
    return render_template('/petownerdashboard/pet_forms.html', pet_form=form )

@pet_form_blueprint.route('/petownerdashboard/change_pet', methods=['GET', 'POST'])
@pet_form_blueprint.route('/petownerdashboard/change_pet.html', methods=['GET', 'POST'])
@login_required
def modify_pet():
    message = ""
    parser = reqparse.RequestParser()
    parser.add_argument('pet_id',type=str)
    parser.add_argument('name',type=str)
    parser.add_argument('attributes', type=str)

    args = parser.parse_args()

    pet = Pet.query.get(args["pet_id"])
    if not pet:
        message += "This Pet Could not Be Modified."
        print("Bad Pet")

    form = RegisterForm()
    pet_attr_dict = {} 
    
    if form.validate_on_submit():
        if pet:
            if current_user == pet.owner:
                form.pet_name.data = args["name"]
                pet_attr_dict = {"pet_name":form.pet_name.data, "pet_type":"", "other_type":form.pet_type.data, "energetic":form.is_energetic.data,  "noisy":form.is_noisy.data, "trained":form.is_trained.data, "other_info":form.other_info.data}
                
                pet.attributes = json.dumps(pet_attr_dict)
                pet.name = form.pet_name.data 

                db.session.commit()
                message += "Pet Has Been Modified."
                return redirect('/petownerdashboard/pets.html')
            print("Bad Owner")
    return render_template('/petownerdashboard/change_pet.html', change_pet_form=form)
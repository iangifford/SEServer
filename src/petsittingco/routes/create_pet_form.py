from wtforms import BooleanField, StringField
from flask_wtf import FlaskForm
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from src.petsittingco.database import db, Pet
from wtforms.validators import InputRequired, Length
import uuid

pet_form_blueprint = Blueprint("pet_forms","__pet_forms__")

class RegisterForm(FlaskForm):
    pet_name = StringField('Pet Name', validators=[InputRequired(), Length(min=4,max=64)])
    pet_type = StringField(' Animal ', validators=[InputRequired()] )
    is_energetic = BooleanField('Energetic?')
    is_noisy = BooleanField('Noisy?')
    is_trained = BooleanField('Trained?')
    other_info = StringField('Other Information', validators=[InputRequired(), Length(max=200)])

@pet_form_blueprint.route('/petownerdashboard/pet_forms', methods=['GET', 'POST'])
@pet_form_blueprint.route('/petownerdashboard/pet_forms.html', methods=['GET', 'POST'])
def pet_forms():
    form = RegisterForm()

    if form.validate_on_submit():
        pet_attr_dict = {} 
        # pet_attributes_string = ""
        pet_attr_dict = {"pet_name":form.pet_name, "pet_type":"", "other_type":form.pet_type, "energetic":form.is_energetic,  "noisy":form.is_noisy, "trained":form.is_trained, "other info":form.other_info} 
        
        new_pet = Pet(id=str(uuid.uuid4()), owner_id=current_user.id, name=form.pet_name, attributes=str(pet_attr_dict))
        db.session.add(new_pet)
        db.session.commit()

        # pet_attributes_string += "<br> <p>"+ str(pet_attr_dict) + "<br> </p>"
        
        return redirect('/petownerdashboard/pets.html')
    return render_template('/petownerdashboard/pet_forms.html', pet_form=form )
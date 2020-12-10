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
    other_info = StringField('Other Information', validators=[InputRequired(), Length(min=0,max=200)])

@login_required
@pet_form_blueprint.route('/petownerdashboard/pet_forms', methods=['GET', 'POST'])
@pet_form_blueprint.route('/petownerdashboard/pet_forms.html', methods=['GET', 'POST'])
def pet_forms():
    form = RegisterForm()

    if form.validate_on_submit():
        pet_attr_dict = {} 
   
        pet_attr_dict = {"pet_name":form.pet_name.data, "pet_type":"", "other_type":form.pet_type.data, "energetic":form.is_energetic.data,  "noisy":form.is_noisy.data, "trained":form.is_trained.data, "other info":form.other_info.data} 

        new_pet = Pet(id=str(uuid.uuid4()), owner_id=current_user.id, name=form.pet_name.data, attributes=str(pet_attr_dict))
        db.session.add(new_pet)
        db.session.commit()

        return redirect('/petownerdashboard/pets.html')
    return render_template('/petownerdashboard/pet_forms.html', pet_form=form )
from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, login_required,logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from src.petsittingco.database import db, Account
login_manager = LoginManager()
login_manager.login_view = '/login'
login_blueprint = Blueprint("logins","__logins__")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4,max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=64)])
    remember_me = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4,max=64), Email(message='Invalid Email Address')])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=64)])
    is_owner = BooleanField('Owner?')
    is_sitter = BooleanField('Pet Sitter?')
    is_shelter = BooleanField('Animal Shelter?')
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=64)])

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    column_searchable_list = ["first_name","last_name","name","location","owner_id","sitter_id"]

@login_manager.user_loader
def load_user(id):
    return Account.query.get(id)

@login_blueprint.route('/login', methods=['GET','POST'])
@login_blueprint.route('/login.html', methods=['GET','POST'])
@login_blueprint.route('/signin.html', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Account.query.filter_by(email=str(form.email.data).lower()).first()
        if user:
            if check_password_hash(user.password,str(form.password.data)):
                login_user(user, remember = form.remember_me.data)
                return redirect(url_for("buttons.main_dashboard"))
            return "Bad email+password combo "
        return "User does not exist."
    return render_template("signin.html", form=form)

@login_blueprint.route('/signup', methods=['GET','POST'])
@login_blueprint.route('/signup.html', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data, method="sha512")
        new_user = Account(id=str(uuid.uuid4()), email = str(form.email.data).lower(),first_name = form.first_name.data, last_name = form.last_name.data, is_owner=form.is_owner.data, is_shelter = form.is_shelter.data, is_admin = False, is_sitter = form.is_sitter.data, password = hashed_pass,phone_number="",address="")
        db.session.add(new_user)
        db.session.commit()
        return redirect('/signup_successful.html')
    return render_template('signup.html',form=form)


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index.html')

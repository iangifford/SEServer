from flask import Flask, send_from_directory, request, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.routing import BaseConverter
from src.petsittingco.resources.resource_map import apis
from src.petsittingco.login import login_manager, login_blueprint, AdminModelView
from src.petsittingco.database import db, Account

#init app
app  = Flask(__name__, static_url_path='')

#bootstrap
Bootstrap(app)


#init api
for create_api in apis:
    create_api(app)
#init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hi"
db.app = app
db.init_app(app)

#init flask login

login_manager.init_app(app)

#add blueprints
app.register_blueprint(login_blueprint)

#init admin dashboard
admin = Admin(app)
admin.add_view(AdminModelView(Account, db.session))

#custom routing (turns empty url into /)
class WildcardConverter(BaseConverter):
    regex = r'(|/.*?)'
    weight = 200
app.url_map.converters['wildcard'] = WildcardConverter


@app.route('/home')
@login_required
def home():
    return render_template("main_dashboard.html", name = current_user.first_name)


@app.route('/petsitterdashboard/<path:path>')
@login_required
def petsitterdashboard(path=None):
    if not current_user.is_sitter:
        return "Page not found", 404
    
    return send_from_directory('static/petsitterdashboard',path)

@app.route('/<wildcard:path>')
@app.route('/', defaults={"path":''})
def static_files(path=None):
    print("path:",path)
    if(path=="/" or path==""):
        return send_from_directory("static","/index.html")
    return send_from_directory('static',path)


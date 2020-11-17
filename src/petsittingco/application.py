from flask import Flask, send_from_directory, request
from petinfo import create_api
from database import db
#init app
app  = Flask(__name__, static_url_path='')
#init api
create_api(app)
#init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)




@app.route('/<path:path>')
@app.route('/')
def static_files(path=None):
    return send_from_directory('static',path)


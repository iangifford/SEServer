from flask import Flask, send_from_directory, request
from resources import create_api

#init
app  = Flask(__name__, static_url_path='')
#app serving function for db 
def getApp():
    return app
#init api
create_api(app)
#init database



@app.route('/<path:path>')
@app.route('/')
def static_files(path=None):
    return send_from_directory('static',path)


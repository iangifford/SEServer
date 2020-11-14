from flask import Flask, send_from_directory, request
from resources import create_api
app  = Flask(__name__, static_url_path='')
create_api(app)
@app.route('/<path:path>')
@app.route('/')
def static_files(path=None):
    return send_from_directory('static',path)


from flask import Flask, send_from_directory, request
app  = Flask(__name__, static_url_path='')

@app.route('/<path:path>')
def static_files(path=None):
    return send_from_directory('static',path)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application import getApp
app = getApp()
app.config['SQLALCHEMY_DATABASE_URI'] = 'test.db'
db = SQLAlchemy(app)

class User(db)
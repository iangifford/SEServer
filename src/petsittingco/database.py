from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    type = db.Column(db.Integer, nullable = False)
    first_name = db.Column(db.String(32), nullable = False)
    last_name = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(128), unique=True,nullable = False)
    password = db.Column(db.String(128), nullable = False)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    owner_id = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(32), nullable = False)
    attributes = db.Column(db.String(512), nullable = False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    location = db.Column(db.String(256),nullable = False)
    pet_id = db.Column(db.Integer, nullable = False)
    sitter_id = db.Column(db.Integer, nullable = True)
    accepted = db.Column(db.Boolean, nullable = False)
    details = db.String(db.String(1024))
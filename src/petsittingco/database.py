from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from dataclasses import dataclass
db = SQLAlchemy()

#@dataclass
class Account(db.Model):
    """id: int
    type: int
    first_name: str
    last_name: str
    email: str
    """
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    type = db.Column(db.Integer, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, unique=True,nullable = False)
    password = db.Column(db.Text, nullable = False)

class Pet(db.Model):
    """id: int
    owner_id: int
    name: str
    attributes: str
"""
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    owner_id = db.Column(db.Integer, nullable = False)
    name = db.Column(db.Text, nullable = False)
    attributes = db.Column(db.Text, nullable = False)

class Job(db.Model):
    """
    id: int
    location: str
    pet_id: int
    sitter_id: int
    owner_id: int
    accepted: bool
    details: str
"""
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    location = db.Column(db.Text,nullable = False)
    pet_id = db.Column(db.Integer, nullable = False)
    sitter_id = db.Column(db.Integer, nullable = True)
    owner_id = db.Column(db.Integer, nullable = False)
    accepted = db.Column(db.Boolean, nullable = False)
    details = db.String(db.Text)
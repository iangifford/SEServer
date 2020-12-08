from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
#from dataclasses import dataclass
db = SQLAlchemy()

#@dataclass
class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    """id: int
    isOwner: bool
    isSitter: bool
    isShelter: bool
    isAdmin: bool
    first_name: str
    last_name: str
    email: str
    """
    #fields
    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    is_owner = db.Column(db.Boolean, nullable = False)
    is_sitter = db.Column(db.Boolean, nullable = False)
    is_shelter = db.Column(db.Boolean, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, unique=True,nullable = False)
    password = db.Column(db.Text, nullable = False)
    address = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    #relationships
    pets = db.relationship("Pet", backref='owner')
    owner_jobs = db.relationship("Job", backref='owner', lazy = 'dynamic', foreign_keys = 'Job.owner_id')
    sitter_jobs = db.relationship("Job", backref = 'sitter',lazy = 'dynamic', foreign_keys = 'Job.sitter_id')

class Pet(db.Model):
    __tablename__ = 'pet'
    """id: int
    owner_id: int
    name: str
    attributes: str
"""

    #fields
    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    owner_id = db.Column(db.Text, db.ForeignKey('account.id'))
    name = db.Column(db.Text, nullable = False)
    attributes = db.Column(db.Text, nullable = False)



class Job(db.Model):
    __tablename__ = 'job'
    """
    id: int
    location: str
    pet_id: int
    sitter_id: int
    owner_id: int
    accepted: bool
    details: str
"""
    #fields
    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    location = db.Column(db.Text)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    is_at_owner = db.Column(db.Boolean, nullable = False)
    start_datetime = db.Column(db.Text, nullable = False)
    end_datetime = db.Column(db.Text, nullable = False)
    sitter_id = db.Column(db.Text, db.ForeignKey('account.id'))
    owner_id = db.Column(db.Text, db.ForeignKey('account.id'))
    accepted = db.Column(db.Boolean, nullable = False)
    canceled = db.Column(db.Boolean, nullable = False)
    details = db.Column(db.Text)
    
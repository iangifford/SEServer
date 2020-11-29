from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#from dataclasses import dataclass
db = SQLAlchemy()

#@dataclass
class Account(db.Model):
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
    jobs = db.relationship("Job",backref="pet",lazy = 'dynamic',foreign_keys = 'Job.pet_id')


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
    location = db.Column(db.Text,nullable = False)
    pet_id = db.Column(db.Text, db.ForeignKey('pet.id'))
    sitter_id = db.Column(db.Text, db.ForeignKey('account.id'))
    owner_id = db.Column(db.Text, db.ForeignKey('account.id'))
    accepted = db.Column(db.Boolean, nullable = False)
    details = db.String(db.Text)
    
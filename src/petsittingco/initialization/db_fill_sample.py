import context
from src.petsittingco.application import db
from src.petsittingco.database import Account, Pet, Job
from werkzeug.security import generate_password_hash
acc1 = Account(id = "1", is_owner = True, is_sitter = False, is_shelter = False, is_admin = False, first_name = "John", last_name = "Smith", email = "JSmith@test.com", password = generate_password_hash("password123AIJI"))
pet1 = Pet(id = "1", owner = acc1, name = "Fluffy", attributes = "{'Aggressive':'False'}")
job1 = Job(id = "1", location = "1234 Shady Lane, Baltimore, Maryland 21043", pet = pet1, sitter = acc1, owner = acc1, accepted = False, details = "Please feed twice a day with food from cabinet")
db.session.add(acc1)
db.session.add(pet1)
db.session.add(job1)
db.session.commit()

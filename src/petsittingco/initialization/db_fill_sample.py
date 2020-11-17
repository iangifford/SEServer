import context
from application import db
from database import Account, Pet, Job

acc1 = Account(id = 1, type = 1, first_name = "John", last_name = "Smith", email = "JSmith@test.com", password = "password")
pet1 = Pet(id = 1, owner_id = 1, name = "Fluffy", attributes = "{'Aggressive':'False'}")
job1 = Job(id = 1, location = "1234 Shady Lane, Baltimore, Maryland 21043", pet_id = 1, sitter_id = 1, owner_id = 1, accepted = False, details = "Please feed twice a day with food from cabinet")
db.session.add(acc1)
db.session.add(pet1)
db.session.add(job1)
db.session.commit()

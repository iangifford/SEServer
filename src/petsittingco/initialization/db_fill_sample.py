import context
from src.petsittingco.application import db
from src.petsittingco.database import Account, Pet, Job
from werkzeug.security import generate_password_hash
acc1 = Account(id = "1", is_owner = True, is_sitter = False, is_shelter = False, is_admin = False, first_name = "John", last_name = "Smith", email = "JSmith@test.com", password = generate_password_hash("password123AIJI",method="SHA512"), address="1234 North Lincoln Road", phone_number="867-5309")
pet1 = Pet(id = "1", owner = acc1, name = "Fluffy", attributes = "{'Aggressive':'False'}")
job1 = Job(id = "1",lat=0.05, long=0.05,is_at_owner = True, canceled = False, start_datetime = "01/01/2020,15:30", end_datetime = "01/01/2020,16:30", location = "1234 Shady Lane, Baltimore, Maryland 21043", sitter = acc1, owner = acc1, accepted = False, details = "Please feed twice a day with food from cabinet")
try:
    db.session.add(acc1)
except Exception as e:
    print(e)

try:
    db.session.add(pet1)
except Exception as e:
    print(e)
try:
    db.session.add(job1)
except Exception as e:
    print(e)
try:
    db.session.commit()
except Exception as e:
    print(e)
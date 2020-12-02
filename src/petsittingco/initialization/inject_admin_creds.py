import context
import uuid
from src.petsittingco.application import db
from src.petsittingco.database import Account, Pet, Job
from werkzeug.security import generate_password_hash
admin = Account(id = str(uuid.uuid4()), is_owner = False, is_sitter = False, is_shelter = False, is_admin = True, first_name = "Admin", last_name = "Admin", email = "Admin", password = generate_password_hash("AIJIAdmin2020482",method="SHA512"))
db.session.add(admin)
db.session.commit()

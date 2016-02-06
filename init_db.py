from run_app import db
from models.models import User, ActivatedUsers

db.create_all()
db.session.commit()

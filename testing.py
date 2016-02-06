from run_app import db
from models.models import User

q = User.query.filter_by(username='Maxx').first()
# q.online = False
# db.session.commit()
# q = q.__dict__
q = q.online
print(q)

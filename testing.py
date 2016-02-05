from models.models import Users
from run_app import db
from sqlalchemy import update

# db.create_all()

# query = Users(username='admin', password='1', email='fugg@ukr.net', register=True)
# db.session.add(query)
# db.session.commit()


query = Users.query.filter_by(username='Name2').first()
query.username = 'Name2'
query.activated = True
db.session.commit()

print(query.__dict__)

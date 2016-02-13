from run_app import db
from sqlalchemy.dialects import postgres


class Rooms(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer)
    members = db.Column(postgres.ARRAY(db.Integer))


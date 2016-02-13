from run_app import db
from datetime import datetime


class Rooms(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_room = db.Column(db.String(20))
    time = db.Column(db.DateTime, default=datetime.now())
    id1_messages = db.Column(db.Text)
    id2_messages = db.Column(db.Text)

    def __init__(self):
        pass

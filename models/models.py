from flask_login import UserMixin, current_user
from run_app import db
import datetime


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    activated = db.Column(db.Boolean, default=False)
    registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id=None, username=None, password=None, email=None, query=None, register=False):

        if register:
            self.username = username
            self.email = email
            self.password = password

        if user_id:
            print(user_id)
            query = Users.query.filter(Users.id == user_id).first()

        if query:
            self.take_query(query)

    def get_id(self):
        print(self)
        return self.id

    def take_query(self, query):
        print(query)
        query = query.__dict__
        print(query)
        self.username = query['username']
        self.password = query['password']
        self.id = query['id']
        self.activated = query['activated']
        self.registered = query['registered']
        self.active = query['active']

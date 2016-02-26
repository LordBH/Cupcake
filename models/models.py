from flask import request, session
from run_app import db, mail
from flask_login import UserMixin
from flask_mail import Message
from base64 import b64encode
from os import urandom
from hashlib import sha224
from datetime import datetime
from sqlalchemy.orm import backref


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.DateTime, default=datetime.now())
    online = db.Column(db.Boolean, default=False)

    child = db.relationship('ActivatedUsers', backref=backref("users", uselist=False))

    def __init__(self, last_name=None, first_name=None, password=None, email=None, user_id=None,
                 query=None, register=False, login=False, user_session=False):

        # if login:
        #     self.username = username
        #     self.id = user_id

        if register:
            self.last_name = last_name
            self.first_name = first_name
            self.email = email
            self.password = password
            self.online = True

        if query:
            self.take_query(query)

    #     if user_session:
    #         session['user_id'] = self.id
    #         session['user_username'] = self.username
    #         session['user_email'] = self.email
    #         session['user_active'] = self.active
    #         session['user_online'] = self.online

    def take_query(self, query):
        query = query.__dict__
        self.id = query['id']
        self.last_name = query.get('last_name')
        self.first_name = query.get('first_name')
        self.password = query.get('password')
        self.email = query.get('email')
        self.active = query.get('active')
        self.online = query.get('online')

    def get_id(self):
            return self.id

    @classmethod
    def valid_date(cls):

        last_name = request.form['last-name']
        first_name = request.form['first-name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']

        if not cls.clean_passwords(password1, password2):
            return False

        if not cls.clean_email(email):
            return False

        extra = dict(
            last_name=last_name,
            first_name=first_name,
            password=User.hash_password(password1),
            email=email
        )

        return extra

    @staticmethod
    def clean_passwords(p1, p2):
        if p1 != p2 and len(p1) > 3:
            return False
        return True

    @staticmethod
    def clean_email(e):
        if '@' not in e:
            return False
        return True

    @staticmethod
    def hash_password(p):

        p = p.encode()
        sha = sha224(p)
        sha = sha.hexdigest()

        return sha


class ActivatedUsers(db.Model):
    __tablename__ = 'activated_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    activated = db.Column(db.Boolean, default=False)
    activated_str = db.Column(db.String(120))
    registered = db.Column(db.DateTime, default=datetime.now())

    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship("User", backref=backref("activated_users", uselist=False))

    def __init__(self, cls):
        self.activated_str = self.activated_message()
        self.email = cls.email
        self.users = cls

    def send_email(self):

        msg = Message("Confirm your account on Cake Messenger", recipients=[self.email])
        msg.html = "Link http://127.0.0.1:5000/user/activate/%s" % (self.activated_str,)

        # mail.send(msg)

    @staticmethod
    def activated_message():
        random_bytes = urandom(80)
        token = b64encode(random_bytes).decode('utf-8')
        a = ''
        for x in token:
            if '/' == x or '+' == x:
                continue
            a += x
        return a[:-1]


# class UsersConfig(db.Model):
#
#     __tablename__ = "users_config"
#
#     def __init__(self):
#         pass


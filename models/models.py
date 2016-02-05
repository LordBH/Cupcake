from flask_login import UserMixin
from flask import request
from run_app import db, mail
from flask_mail import Message
from base64 import b64encode
from os import urandom
import hashlib
import datetime


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    activated = db.Column(db.Boolean, default=False)
    activated_str = db.Column(db.String(80))
    registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id=None, username=None, password=None, email=None, query=None, register=False):

        if register:
            self.username = username
            self.email = email
            self.password = password
            self.activated_str = self.activated_message()

        if user_id:
            print(user_id)
            query = Users.query.filter(Users.id == user_id).first()

        if query:
            self.take_query(query)

    def get_id(self):
        return self.id

    def take_query(self, query):
        query = query.__dict__
        self.username = query['username']
        self.password = query['password']
        self.id = query['id']
        self.activated = query['activated']
        self.registered = query['registered']
        self.active = query['active']

    @classmethod
    def valid_date(cls):

        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']

        if not cls.clean_username(username):
            return False

        if not cls.clean_passwords(password1, password2):
            return False

        if not cls.clean_email(email):
            return False

        return dict(username=username, password=Users.hash_password(password1), email=email)

    @staticmethod
    def clean_username(name):
        if len(name) < 4:
            return False
        return True

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

    def send_email(self):

        msg = Message("Confirm your account on Cake Messenger", recipients=[self.email])
        msg.html = "Link http://192.168.3.111:5000/user/activate/%s" % (self.activated_str,)

        mail.send(msg)

    @staticmethod
    def hash_password(p):

        p = p.encode()
        md = hashlib.md5()

        md.update(b"%s" % (p,))
        md = md.hexdigest()

        return md

    @staticmethod
    def activated_message():
        random_bytes = urandom(20)
        token = b64encode(random_bytes).decode('utf-8')
        a = ''
        for x in token:
            if '/' == x:
                continue
            a += x
        return a[:-1]

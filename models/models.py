from flask import request, session
from run_app import db, mail
from flask_login import UserMixin
from flask_mail import Message
from base64 import b64encode
from os import urandom
from hashlib import sha224
from datetime import datetime, date
from sqlalchemy.orm import backref


PERMITTED_EMAILS = ['gmail.com', 'ukr.net', 'yandex.ua']


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.DateTime, default=datetime.now())
    online = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(80))
    city = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    birthday = db.Column(db.DateTime)

    child = db.relationship('ActivatedUsers', backref=backref("users", uselist=False))

    def __init__(self, last_name=None, first_name=None, password=None, email=None,
                 query=None, register=False, user_session=False, reverse_user_session=False):

        if register:
            self.last_name = last_name
            self.first_name = first_name
            self.email = email
            self.password = ActivatedUsers.activated_message(20)
            self.online = True

        if password is not None:
            self.password = password

        if query:
            self.take_query(query)

        if user_session:
            session['user_id'] = self.id
            session['user_last_name'] = self.last_name
            session['user_first_name'] = self.first_name
            session['user_email'] = self.email
            session['user_active'] = self.active
            session['user_online'] = self.online

        if reverse_user_session:
            self.id = session.get('user_id')
            self.last_name = session.get('user_last_name')
            self.first_name = session.get('user_first_name')
            self.email = session.get('user_email')
            self.active = session.get('user_active')
            self.online = session.get('user_online')

    def take_query(self, query):
        query = query.__dict__
        self.id = query.get('id')
        self.last_name = query.get('last_name')
        self.first_name = query.get('first_name')
        self.password = query.get('password')
        self.email = query.get('email')
        self.active = query.get('active')
        self.online = query.get('online')

    def get_id(self):
        return self.id

    @staticmethod
    def valid_date(context):

        last_name = context.get('last_name')
        first_name = context.get('first_name')
        email = context.get('email').lower()

        if not User.clean_names(first_name, last_name):
            return False

        if not User.clean_email(email):
            return False

        extra = dict(
            last_name=last_name,
            first_name=first_name,
            email=email
        )

        return extra

    @staticmethod
    def clean_names(p1, p2):
        if not (len(p1) and len(p2) > 2):
            return False
        return True

    @staticmethod
    def clean_passwords(p1, p2):
        if len(p1) < 6 and p1 != p2:
            return False
        return True

    @staticmethod
    def clean_email(e):
        domain = e.split('@')

        if len(domain) == 2 and domain[1] in PERMITTED_EMAILS:
            return True
        return False

    @staticmethod
    def hash_password(p):

        p = p.encode()
        sha = sha224(p)
        sha = sha.hexdigest()

        return sha

    @staticmethod
    def re_write_config(q):
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        status = request.form.get('status')
        city = request.form.get('city')
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')

        if User.clean_names(last_name, first_name):
            q.first_name = first_name
            q.last_name = last_name

        if status:
            q.status = status

        if city:
            q.city = city
        if phone:
            q.phone = phone
        if birthday:
            try:
                birthday = [int(x) for x in birthday.split('-')]
                birthday = date(birthday[0], birthday[1], birthday[2])
            except ValueError:
                birthday = None
            q.birthday = birthday


class ActivatedUsers(db.Model):
    __tablename__ = 'activated_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    activated = db.Column(db.Boolean, default=False)
    activated_str = db.Column(db.String(120))
    registered = db.Column(db.DateTime, default=datetime.now())
    rooms = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship("User", backref=backref("activated_users", uselist=False))

    def __init__(self, cls):
        self.activated_str = self.activated_message()
        self.email = cls.email
        self.users = cls

    def send_email(self):

        host = request.host_url

        msg = Message("Confirm your account on Cupcake Messenger", recipients=[self.email])
        msg.html = "Link %suser/activate/%s" % (host, self.activated_str)

        mail.send(msg)

    @staticmethod
    def send_email_for_password(email, activated_str=None):
        if activated_str is None:
            activated_str = ActivatedUsers.activated_message()
        host = request.host_url
        msg = Message("Create your new password on Cupcake Messenger", recipients=[email])
        msg.html = "Link %suser/new_password/%s" % (host, activated_str)
        session['act_str_for_password'] = activated_str
        session['email'] = email

        mail.send(msg)

    @staticmethod
    def activated_message(quantity=80):
        random_bytes = urandom(quantity)
        token = b64encode(random_bytes).decode('utf-8')
        a = ''
        for x in token:
            if '/' == x or '+' == x:
                continue
            a += x
        return a[:-1]


class Rooms(db.Model):
    __tablename__ = 'users_chat'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    room_id = db.Column(db.String(80))
    time = db.Column(db.DateTime, default=datetime.now())
    messages_1_ = db.Column(db.Text)
    messages_2_ = db.Column(db.Text)
    checked = db.Column(db.Boolean, default=False)

    def __init__(self, room_id, time=None, user1_mes=None, user2_mes=None):
        self.room_id = room_id
        if time is not None:
            self.time = time

        self.user1_mes = user1_mes
        self.user2_mes = user2_mes


db.create_all()

from flask import render_template, abort
from datetime import datetime
from . import from_main

extra = from_main


@extra.route('/')
def index_page():
    return render_template('main/index.html')


# @extra.route('/<name>')
# def user_page(name):
#
#     from models.models import User, db
#
#     try:
#         name = int(name)
#     except TypeError:
#         abort(404)
#
#     user = User.query.filter_by(id=name).first()
#
#     if user is None:
#         abort(404)
#
#     last_active = user.active
#
#     day_today = last_active.date() != datetime.now().date()
#     hour_now = last_active.hour <= datetime.now().hour
#     last_10_minute = last_active.minute < datetime.now().minute - 10
#
#     if day_today or hour_now and last_10_minute:
#         user.online = False
#         db.session.commit()
#
#     context = {
#         'user': user
#     }
#
#     return render_template('profile.html', context=context)


@extra.route('/all')
def all_users():

    from models.models import User

    users = User.query.all()

    return render_template('users.html', users=users)



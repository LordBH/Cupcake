from flask import render_template, abort
from datetime import datetime
from . import from_main

extra = from_main


@extra.route('/')
def index_page():
    return render_template('main/index.html')


@extra.route('/<name>')
def user_page(name):

    from models.models import User, db

    try:
        name = int(name)
    except ValueError:
        abort(404)

    user = User.query.filter_by(id=name).first()

    if last_seen(user):
        user.online = False
        db.session.commit()

    context = {
        'user': user
    }

    return render_template('profile.html', context=context)


@extra.route('/all')
def all_users():
    from models.models import User, db

    users = User.query.all()

    for x in users:
        if last_seen(x):
            x.online = False
    db.session.commit()

    return render_template('users.html', users=users)


def last_seen(user):
    if user is None:
        abort(404)

    last_active = user.active

    day_today = last_active.date() != datetime.now().date()
    hour_now = last_active.hour <= datetime.now().hour
    last_10_minute = last_active.minute < datetime.now().minute - 1

    return day_today or hour_now or last_10_minute

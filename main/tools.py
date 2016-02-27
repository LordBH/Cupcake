from flask import abort
from datetime import datetime


def last_seen(user):
    if user is None:
        abort(404)

    last_active = user.active

    day_today = last_active.date() != datetime.now().date()
    hour_now = last_active.hour <= datetime.now().hour
    last_10_minute = last_active.minute < datetime.now().minute - 1

    return day_today or hour_now or last_10_minute


def get_context(q=None):

    q = q.__dict__
    extra = {
        'flag': True,
        'msg': 'success',
        'id': q.id,
        'last_name': q.last_name,
        'first_name': q.first_name,
        'email': q.email,
        'online': q.id,
        'status': q.users_config.status,
        'city': q.users_config.city,
        'phone': q.users_config.phone,
        'birthday': q.users_config.birthday,
    }

    return extra

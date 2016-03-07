from flask import abort
from datetime import datetime


def last_seen(user):
    if user is None:
        abort(404)

    last_active = user.active

    day_today = last_active.date() != datetime.now().date()
    hour_now = last_active.hour <= datetime.now().hour
    last_10_minute = last_active.minute < datetime.now().minute - 10

    return day_today or hour_now or last_10_minute


def all_users_context(query, current_id):
    from models.chat import Rooms

    data = {'people': []}

    for x in query:
        q = x.__dict__

        activated = Rooms.query.filter_by(user_id=q.get('id')).first()
        extra = {
            'flag': True,
            'msg': 'success',
            'id': q.get('id'),
            'last_name': q.get('last_name'),
            'first_name': q.get('first_name'),
            'email': q.get('email'),
            'online': q.get('online'),
            'status': q.get('status'),
            'city': q.get('city'),
            'phone': q.get('phone'),
            'birthday': str(q.get('birthday')),
            'activated': activated

        }

        if not extra.get('online'):
            """Re-write for active"""
            # extra['active'] = last_seen()
            pass

        if q.get('id') == current_id:
            for key, value in extra.items():
                data[key] = value
        else:
            data['people'].append(extra)

    return data

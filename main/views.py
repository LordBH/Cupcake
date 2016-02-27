from flask import render_template, abort
from datetime import datetime
from . import from_main

extra = from_main


@extra.route('/')
def index_page():

    context = {}

    return render_template('base.html', context=context)


def last_seen(user):
    if user is None:
        abort(404)

    last_active = user.active

    day_today = last_active.date() != datetime.now().date()
    hour_now = last_active.hour <= datetime.now().hour
    last_10_minute = last_active.minute < datetime.now().minute - 1

    return day_today or hour_now or last_10_minute

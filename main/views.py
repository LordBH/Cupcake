from flask import render_template, Blueprint, abort

from_main = Blueprint('main', __name__, template_folder='templates',
                      static_folder='static', static_url_path='/%s' % __name__)

extra = from_main


@extra.route('/')
def index_page():
    return render_template('main/index.html')


@extra.route('/<name>')
def user_page(name):
    from models.models import User, db
    from datetime import datetime

    try:
        name = int(name)
    except TypeError:
        abort(404)

    q = User.query.filter_by(id=name).first()

    if q is None:
        abort(404)

    last_active = q.active

    day_today = last_active.date() != datetime.now().date()
    hour_now = last_active.hour <= datetime.now().hour
    last_10_minute = last_active.minute < datetime.now().minute - 1

    if day_today or hour_now and last_10_minute:
        q.online = False
        db.session.commit()

    context = {
        'user': q
    }

    return render_template('user.html', context=context)

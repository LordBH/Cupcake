from flask import render_template, abort, request, session, redirect, url_for
from flask_socketio import emit
from chats import socket_io
from main.tools import all_users_context
from . import from_main

extra = from_main


@extra.route('/')
def index_page():
    context = {}
    return render_template('base.html', context=context)


@extra.route(r'/config', methods=['POST'])
def user_conf():
    if request.method == 'POST':
        from models.models import User, db

        q = User.query.filter_by(id=session.get('user_id')).first()
        if q is None:
            abort(404)

        User.re_write_config(q)
        db.session.commit()

    return redirect(url_for('main.index_page'))


@socket_io.on('page', namespace='/main')
def page(data=None):
    from models.models import User, db

    current_id = session.get('user_id')
    query = User.query.all()

    context = all_users_context(query, current_id)

    db.session.commit()

    return emit('userData', context)

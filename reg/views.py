from flask import request, redirect, render_template, url_for, session, abort
from flask_login import login_user, logout_user
from chats import socket_io
from flask_socketio import emit
from . import from_reg

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    from models.models import User, ActivatedUsers, UsersConfig
    from run_app import db

    if request.method == 'GET':
        return render_template('reg/register.html', context={})

    context = {
        'last_name': request.form.get('last-name'),
        'first_name': request.form.get('first-name'),
        'password1': request.form.get('password1'),
        'password2': request.form.get('password2'),
        'email': request.form.get('email'),
        'msg': 'Validation error',
    }

    if request.method == 'POST':
        date = User.valid_date(context)
        if date:
            config = UsersConfig()
            user = User(first_name=date.get('first_name'), last_name=date.get('last_name'),
                        password=date.get('password'), email=date.get('email'), register=True)
            user.users_config = config
            activate = ActivatedUsers(user)

            db.session.add(config)
            db.session.add(user)
            db.session.add(activate)
            db.session.commit()

            activate.send_email()

            login_user(user, remember=True)

            return redirect(url_for('main.index_page'))
        else:

            return render_template('reg/register.html', context=context)

    context['msg'] = 'Problem with registration'

    return render_template('reg/register.html', context=context)


@extra.route('/login', methods=['GET', 'POST'])
def login():
    from models.models import User, db, datetime

    if request.method == 'GET':
        return render_template('base.html', context={})

    context = {
        'password': request.form.get('password'),
        'email': request.form.get('email'),
        'msg': 'Sorry, but your login or password is incorrect',
    }

    if request.method == 'POST':

        query = User.query.filter_by(email=context.get('email'),
                                     password=User.hash_password(context.get('password'))).first()

        if query:
            user = User(query=query)

            query.online = True
            query.active = datetime.now()
            db.session.commit()

            login_user(user, remember=True)

    return render_template('base.html', context=context)


@extra.route('/logout')
def logout():
    from models.models import User, db, datetime

    query = User.query.filter_by(id=session.get('user_id')).first()

    if query is not None:
        query.online = False
        query.active = datetime.now()
        db.session.commit()
        logout_user()

    return redirect(url_for('main.index_page'))


@extra.route(r'/user/activate/<s>')
def activate_user(s):
    from models.models import ActivatedUsers, db

    context = {
        'msg': 'Successfully accept email'
    }

    query = ActivatedUsers.query.filter_by(activated_str=s).first()

    if query is not None:
        query.activated = True
        db.session.commit()

        return render_template('reg/accepting_email.html', context=context)

    context['msg'] = 'Wrong code'
    return render_template('reg/accepting_email.html', context=context)


@extra.route(r'/config', methods=['POST'])
def user_conf():
    if request.method == 'POST':
        from models.models import User

        q = User.query.filter_by(id=session.get('user_id')).first()

        if q is None:
            abort(404)
        else:
            context = {
                'last_name': request.form.get(''),
                'first_name': request.form.get(''),
                'password1': request.form.get('password1'),
                'password2': request.form.get('password2'),
                'email': request.form.get('email'),
                'msg': 'Validation error',
            }


@socket_io.on('validationEmail', namespace='/reg')
def check_unique_email(email):
    from models.models import User

    q = User.query.filter_by(email=email.get('email')).first()

    if q is None:
        flag = True
    else:
        flag = False

    emit('flag', {'extra': flag})

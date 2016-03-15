from flask import request, redirect, render_template, url_for, session
from flask_login import login_user, logout_user
from chats import socket_io
from flask_socketio import emit
from sqlalchemy.exc import IntegrityError
from . import from_reg

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    from models.models import User, ActivatedUsers
    from run_app import db

    if request.method == 'GET':
        return render_template('reg/register.html', context={})

    context = {
        'last_name': request.form.get('last-name'),
        'first_name': request.form.get('first-name'),
        'email': request.form.get('email'),
        'msg': 'Validation error',
    }

    if request.method == 'POST':
        date = User.valid_date(context)
        if date:
            user = User(first_name=date.get('first_name'), last_name=date.get('last_name'),
                        email=date.get('email'), register=True)
            activate = ActivatedUsers(user)

            for x in [user, activate]:
                db.session.add(x)
            try:
                db.session.commit()
            except IntegrityError:
                context['msg'] = 'This email has already registered'
                return render_template('reg/register.html', context=context)

            activate.send_email()

            return render_template('reg/flash_message.html', context={'msg': 'Activate your e-mail'})
        else:

            return render_template('reg/register.html', context=context)

    context['msg'] = 'Problem with registration'

    return render_template('reg/register.html', context=context)


@extra.route('/login', methods=['GET', 'POST'])
def login():
    from models.models import User, db, datetime

    context = {
        'password': request.form.get('password'),
        'email': request.form.get('email'),
        'msg': 'Sorry, but your login or password is incorrect',
    }

    if request.method == 'POST':

        query = User.query.filter_by(email=context.get('email').lower(),
                                     password=User.hash_password(context.get('password'))).first()

        if query:
            user = User(query=query)

            query.online = True
            query.active = datetime.now()
            db.session.commit()

            login_user(user, remember=True)
        else:
            return render_template('base.html', context=context)
    return redirect(url_for('main.index_page'))


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


@extra.route(r'/user/activate/<s>', methods=['POST', 'GET'])
def activate_user(s):
    from models.models import User, ActivatedUsers, db

    context = {
        'msg': 'Write yours password',
        'action': "/user/activate/%s" % (s,),
    }

    query = ActivatedUsers.query.filter_by(activated_str=s).first()

    if request.method == 'GET' and query is not None:
        return render_template('reg/handling_pass.html', context=context)

    if request.method == 'POST':

        f = {
            'pass1': request.form.get('pass1'),
            'pass2': request.form.get('pass2'),
        }

        if query is not None:
            if query.activated:
                context['msg'] = 'This code has already registered'
            query.activated = True

            if User.clean_passwords(f['pass1'], f['pass2']):
                query.users.password = User.hash_password(f['pass1'])
            else:
                context['msg'] = 'Bad password'
                return render_template('reg/handling_pass.html', context=context)

            user = query.users

            login_user(user, remember=True)

            db.session.commit()

            context['msg'] = 'Your account successfully create'

            return render_template('reg/flash_message.html', context=context)

        context['msg'] = 'Wrong code'

    context['msg'] = 'Problem with activation'

    return render_template('reg/flash_message.html', context=context)


@extra.route(r'/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    from models.models import ActivatedUsers, User
    context = {
        'msg': 'Please write your e-mail'
    }

    if request.method == 'POST':
        email = request.form.get('email').lower()
        q = User.query.filter_by(email=email).first()
        if User.clean_email(email) and q is not None:
            # ActivatedUsers.send_email_for_password(email)
            context['msg'] = 'Check your email address and confirm the link'

            return render_template('reg/flash_message.html', context=context)

        context['msg'] = 'Wrong e-mail'

    return render_template('reg/email.html', context=context)


@extra.route(r'/user/new_password/<s>', methods=['POST', 'GET'])
def new_password(s):
    context = {
        'msg': 'Wrong code for create new password',
        'action': "/user/new_password/%s" % (s,),
    }

    if s == session.get('act_str_for_password'):
        context['msg'] = 'Please write your new password'

        if request.method == 'POST':
            from models.models import User, db

            pass1 = request.form.get('pass1')
            pass2 = request.form.get('pass2')

            if User.clean_passwords(pass1, pass2):
                query = User.query.filter_by(email=session.get('email')).first()
                query.password = User.hash_password(pass1)

                db.session.add(query)
                db.session.commit()

                del session['email']
                del session['act_str_for_password']

                context['msg'] = 'Successfully changed password'

                return render_template('reg/flash_message.html', context=context)

        return render_template('reg/handling_pass.html', context=context)

    return render_template('reg/flash_message.html', context=context)


@socket_io.on('validationEmail', namespace='/reg')
def check_unique_email(data):
    from models.models import User

    email = data.get('email')
    if email:
        q = User.query.filter_by(email=email).first()

        if q is None:
            flag = True
        else:
            flag = False

        return emit('flag', {'extra': flag})
    return emit('flag', {'extra': False})

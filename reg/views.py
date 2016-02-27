from flask import request, redirect, render_template, url_for, abort, session
from flask_login import login_user, logout_user
from . import from_reg

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    from models.models import User, ActivatedUsers, UsersConfig
    from run_app import db

    if request.method == 'GET':
        return render_template('reg/register.html')

    context = {}

    if request.method == 'POST':
        date = User.valid_date()
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

    context['msg'] = 'Problem with registration'

    return render_template('reg/register.html', context=context)


@extra.route('/login', methods=['GET', 'POST'])
def login():
    from models.models import User, db, datetime

    if request.method == 'GET':
        return render_template('base.html')

    context = {}

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = User.query.filter_by(email=email, password=User.hash_password(password)).first()

        if query:

            user = User(query=query)

            query.online = True
            query.active = datetime.now()
            db.session.commit()

            login_user(user, remember=True)
            return redirect(url_for('main.index_page'))

        context['msg'] = 'Wrong username or password'
        return render_template('base.html', context=context)

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    from models.models import User, db, datetime

    query = None

    try:
        query = User.query.filter_by(id=session['user_id']).first()
    except AttributeError:
        abort(404)

    if query is not None:
        query.online = False
        query.active = datetime.now()
        print(__file__)
        db.session.commit()

    logout_user()
    return redirect(url_for('main.index_page'))


@extra.route(r'/user/activate/<num>')
def activate_user(num):
    """Activation user for code from email """

    from models.models import ActivatedUsers, db

    query = ActivatedUsers.query.filter_by(activated_str=num).first()

    if query is not None:
        query.activated = True
        print(__file__)
        db.session.commit()

        return render_template('reg/accepting_email.html', msg='Successfully accept email')

    return render_template('reg/accepting_email.html', msg='Wrong code')

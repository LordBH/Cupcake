from flask import request, redirect, render_template, url_for, Blueprint
from flask_login import login_user, logout_user, current_user


from_reg = Blueprint('reg', __name__, template_folder='templates',
                     static_folder='static', static_url_path='/%s' % __name__)

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    from models.models import User, ActivatedUsers
    from run_app import db

    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        date = User.valid_date()
        if date:
            user = User(username=date['username'], password=date['password'],
                        email=date['email'], register=True)
            activate = ActivatedUsers(user)

            db.session.add(user)
            db.session.add(activate)
            db.session.commit()

            activate.send_email()

            login_user(user, remember=True)

            return render_template('base.html', msg='Please accept your message on email')

    return render_template('register.html', msg='Problem with registration')


@extra.route('/login', methods=['GET', 'POST'])
def login():
    from models.models import User, db, datetime

    if request.method == 'GET':
        return render_template('base.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = User.query.filter_by(username=username, password=User.hash_password(password)).first()
        activated = None

        if query:
            """ RE - WRITE THIS CODE """

            # activated = query.__dict__['activated']
            activated = True

        if activated:
            user = User(query=query)

            query.online = True
            query.active = datetime.now()
            db.session.commit()

            login_user(user, remember=True)
        elif activated is False:
            return render_template('base.html', msg="U don't confirm email")

        return render_template('base.html', msg='Wrong username or password')

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    from models.models import User, db, datetime

    query = User.query.filter_by(id=current_user.id).first()

    if query is not None:
        query.online = False
        query.active = datetime.now()
        db.session.commit()

    logout_user()
    return redirect(url_for('main.index_page'))


@extra.route(r'/user/activate/<num>')
def activate_user(num):
    from models.models import ActivatedUsers, db

    query = ActivatedUsers.query.filter_by(activated_str=num).first()

    if query is not None:
        query.activated = True
        db.session.commit()

        return render_template('base.html', msg='Successfully accept email')

    return render_template('base.html', msg='wrong code')

from flask import request, redirect, render_template, url_for, Blueprint
from flask_login import login_user, logout_user
from models.models import Users, db


from_reg = Blueprint('reg', __name__, template_folder='templates',
                     static_folder='static', static_url_path='/%s' % __name__)

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        date = Users.valid_date()
        if date:
            user = Users(username=date['username'], password=date['password'],
                         email=date['email'], register=True)

            db.session.add(user)
            db.session.commit()

            user.send_email()

            return render_template('base.html', msg='Please accept your message on email')

    return render_template('register.html', msg='Problem with registration')


@extra.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('base.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = Users.query.filter_by(username=username, password=Users.hash_password(password)).first()
        activated = None

        if query:
            activated = query.__dict__['activated']

        if activated:
            user = Users(query=query)
            login_user(user, remember=True)
        elif activated is False:
            return render_template('base.html', msg="U don't confirm email")

        return render_template('base.html', msg='Wrong username or password')

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index_page'))


@extra.route(r'/user/activate/<num>')
def activate_user(num):
    query = Users.query.filter_by(activated_str=num).first()

    if query is not None:
        query.activated = True
        db.session.commit()

        return render_template('base.html', msg='Successfully accept email')

    return render_template('base.html', msg='wrong code')

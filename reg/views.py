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

            Users.send_email(user.email)

            login_user(user, remember=True)

            return redirect(url_for('main.index_page'))

    return render_template('register.html', msg='Problem with registration')


@extra.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('base.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = Users.query.filter(Users.username == username, Users.password == password).first()

        activated = query.__dict__['activated']

        if query and activated:
            user = Users(query=query)
            login_user(user, remember=True)

        return render_template('base.html', msg='Please accept your message on email')

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index_page'))


@extra.route(r'/user/activate/<num>')
def activate_user(num):
    query = Users.query.filter_by(activated_str=num).first()
    query = query.__dict__
    if query['activated_str'] == num:
        query['activated'] = True

    return render_template('base.html', msg='Successfully accept email')

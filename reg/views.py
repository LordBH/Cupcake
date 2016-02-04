from flask import request, redirect, render_template, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, session
from models.models import Users


from_reg = Blueprint('reg', __name__, template_folder='templates',
                      static_folder='static', static_url_path='/%s' % __name__)

extra = from_reg


@extra.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    print(request.form['username'])
    print(request.method)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email'] or None

        user = Users(username=username, password=password, email=email, register=True)

        login_user(user, remember=True)
    return redirect(url_for('main.index_page'))


@extra.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('base.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = Users.query.filter(Users.username == username, Users.password == password).first()

        if query:
            user = Users(query=query)
            login_user(user, remember=True)

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index_page'))





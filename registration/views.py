from flask import request, redirect, render_template, url_for, Blueprint
from flask_login import login_user, logout_user, current_user
from .models import User, SqlQuery


views_from_registration = Blueprint('registration', __name__, template_folder='templates',
                                    static_folder='static', static_url_path='/%s' % __name__)
extra = views_from_registration


@extra.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    response = SqlQuery()
    response.execute(
            """INSERT INTO user_table (username, password) VALUES ('%s', '%s');"""
            % (username, password))



    query = response.execute(
            """SELECT * FROM user_table as u WHERE u.username='%s' AND u.password='%s';"""
            % (username, password))

    print(query)

    user = User(query[1], query[0])

    login_user(user, remember=True)

    return redirect(url_for('main.index_page'))


@extra.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('base.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = SqlQuery()
        query = response.execute(
                """SELECT * FROM user_table as u WHERE u.username='%s' AND u.password='%s';"""
                % (username, password)
        )

        print(query)

        if query:
            user = User(username)
            login_user(user, remember=True)
            print(current_user)

    return redirect(url_for('main.index_page'))


@extra.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index_page'))

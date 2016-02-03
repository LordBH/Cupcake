from flask import Flask
from flask_mail import Mail
from config import settings, urls
from flask_login import LoginManager
from registration.models import SqlQuery, User


app = Flask(__name__)

# configurations
app.config.from_object(settings.DevelopmentConfig)

# sending email
mail = Mail(app)

# user handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# register blueprints
for x in urls.blueprints:
    app.register_blueprint(x)


@login_manager.user_loader
def load_user(user_id):

    response = SqlQuery()
    query = response.execute(
            """SELECT * FROM user_table as u WHERE u.id='%s';""" % (user_id[0],)
    )

    user = User(query[1], query[0])
    return user


if __name__ == '__main__':
    app.run()

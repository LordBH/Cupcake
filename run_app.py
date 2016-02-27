from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from chats import socket_io
from configurations import filters, settings


# application
app = Flask(__name__)

# configurations
app.config.from_object(settings.DevelopmentConfig)


# db
db = SQLAlchemy(app)

# sending email
mail = Mail(app)

# user handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# template filters
for x in filters.filters:
    app.jinja_env.filters[x.__name__] = x


# rolling db when exception

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


if __name__ == '__main__':
    from configurations.blueprints import blueprints

    # blueprint
    for x in blueprints:
        app.register_blueprint(x)

    @login_manager.user_loader
    def load_user(user_id):

        from models.models import User, datetime, session

        if session.get('user_active'):
            return User()

        print(' ==> '*10)
        query = User.query.filter(User.id == user_id).first()
        print(' <== '*10)

        if query is None:
            return None

        query.online = True
        query.active = datetime.now()
        user = User(query=query, user_session=True)

        db.session.commit()

        datetime.now()
        return user

    socket_io.init_app(app)
    host = '0.0.0.0'
    port = 5000
    socket_io.run(app, host=host, port=port)

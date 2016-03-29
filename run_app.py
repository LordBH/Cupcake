from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from main.tools import loading_user, t_r
from chats import socket_io
from configurations import filters, settings, thread, blueprints

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

# blueprints
for x in blueprints.blueprints:
    app.register_blueprint(x)

# threading
for x in thread.list_of_thread:
    x.start()


@app.teardown_request
def teardown_request(e):
    t_r(e, db)


@login_manager.user_loader
def load_user(user_id):
    return loading_user(user_id)


if __name__ == '__main__':
    socket_io.init_app(app)

    host = '0.0.0.0'
    port = 5000

    socket_io.run(app, host=host, port=port)

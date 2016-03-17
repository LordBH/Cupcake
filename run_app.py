from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from main.tools import loading_user
from chats import socket_io
from configurations import filters, settings, thread


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

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


# template filters
for x in filters.filters:
    app.jinja_env.filters[x.__name__] = x


if __name__ == '__main__':
    from configurations.blueprints import blueprints

    # blueprint
    for x in blueprints:
        app.register_blueprint(x)

    # threading
    for x in thread.list_of_thread:
        x.start()

    @login_manager.user_loader
    def load_user(user_id):
        return loading_user(user_id)

    socket_io.init_app(app)
    host = '0.0.0.0'

    # port = 5000
    from port import port

    socket_io.run(app, host=host, port=port)

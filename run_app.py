from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from blueprints import blueprints
from filters import fil
import settings
import psycopg2

app = Flask(__name__)

app.config.from_object(settings.DevelopmentConfig)

db = SQLAlchemy(app)

# configurations

# sending email
mail = Mail(app)

# db = SQLAlchemy(app)

# user handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# blueprint
for x in blueprints:
    app.register_blueprint(x)

# template filters
for x in fil:
    app.jinja_env.filters[x.__name__] = x


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


if __name__ == '__main__':

    from models.models import User, datetime


    @login_manager.user_loader
    def load_user(user_id):

        query = User.query.filter(User.id == user_id).first()

        if query is None:
            return None

        query.online = True
        query.active = datetime.now()

        db.session.commit()

        user = User(query=query)

        return user


    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port)

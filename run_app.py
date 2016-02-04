from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)

# configurations
app.config.from_object(settings.DevelopmentConfig)

# sending email
mail = Mail(app)

db = SQLAlchemy(app)

# user handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if __name__ == '__main__':

    from models.models import Users

    @login_manager.user_loader
    def load_user(user_id):

        user = Users(user_id=user_id)

        return user



    from main.views import from_main
    from reg.views import from_reg



    blueprints = (

        from_main,
        from_reg,

    )

    for x in blueprints:
        app.register_blueprint(x)




    app.run()

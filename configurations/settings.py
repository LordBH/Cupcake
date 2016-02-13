class ConfigClass(object):
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///keks_db"
    CSRF_ENABLED = True

    # Flask-Mail settings1
    MAIL_USERNAME = 'testingdjangomaxx@gmail.com'
    MAIL_PASSWORD = '][poi123'
    MAIL_DEFAULT_SENDER = 'testingdjangomaxx@gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int('465')
    MAIL_USE_SSL = True

    # Registration
    USER_LOGIN_TEMPLATE = 'main/templates/login.html'
    USER_REGISTER_TEMPLATE = 'main/templates/register.html'

    # Flask-User settings
    USER_APP_NAME = "Social website"
    STATIC_FOLDER = 'static'


class ProductionConfig(ConfigClass):
    DEBUG = False


class DevelopmentConfig(ConfigClass):
    DEVELOPMENT = True
    DEBUG = True

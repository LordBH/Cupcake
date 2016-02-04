import os


class ConfigClass(object):
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = "postgresql:///keks_db"
    CSRF_ENABLED = True

    # Flask-Mail settings1
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'testingdjangomaxx@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '][poi123')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'fugg@ukr.net')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

    # Registration
    USER_LOGIN_TEMPLATE = 'about/templates/login.html'
    USER_REGISTER_TEMPLATE = 'about/templates/register.html'

    # Flask-User settings
    USER_APP_NAME = "Social website"


class ProductionConfig(ConfigClass):
    DEBUG = False


class DevelopmentConfig(ConfigClass):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(ConfigClass):
    TESTING = True


class ManageConfig(DevelopmentConfig):
    pass
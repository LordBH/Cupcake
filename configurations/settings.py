import os


class ConfigClass:
    # App Settings
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    SECRET_KEY = 'SECRET_KEY'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///cupcake"
    CSRF_ENABLED = True

    # Flask-Mail settings
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

    # Files folder
    FILES_FOLDER = BASE_DIR + '/files'
    IMAGES_FOLDER = FILES_FOLDER + '/images'


class ProductionConfig(ConfigClass):
    DEBUG = False


class DevelopmentConfig(ConfigClass):
    DEVELOPMENT = True
    DEBUG = True


class BionicConfig(ConfigClass):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/cupcake"

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'ce1e098bee3e893eb8a108629f3fc117'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #
    # SQLALCHEMY_TRACK_MODIFICATION = False
    #
    # SQLALCHEMY_ECHO = True

    SECURITY_PASSWORD_SALT = 'kjsdhkjsdkjhkjds'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    RECAPTCHA_PUBLIC_KEY = '6LfjbN8nAAAAAI-ySgynDFEnlWRU8i9IszWkENDG'
    RECAPTCHA_PRIVATE_KEY = '6LfjbN8nAAAAAPHRqNmZh1GrfOZ8YGRlPvtgLylI'

    TESTING = True

    RECAPTCHA_OPTIONS = dict(
        theme='custom',
        custom_theme_widget='recaptcha_widget'
    )
    RECAPTCHA_ENABLED = False
    RECAPTCHA_THEME = 'dark'
    RECAPTCHA_SIZE = "compact"
    RECAPTCHA_LANGUAGE = "ru"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply.notifications.flaskblog@gmail.com'
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

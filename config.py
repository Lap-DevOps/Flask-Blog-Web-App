import os
from dotenv import load_dotenv
from envparse import env

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

env.read_envfile()



class Configuration(object):
    DEBUG = True
    SECRET_KEY = env.str("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #
    # SQLALCHEMY_TRACK_MODIFICATION = False
    #
    # SQLALCHEMY_ECHO = True

    SECURITY_PASSWORD_SALT = 'kjsdhkjsdkjhkjds'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    TESTING = False

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
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

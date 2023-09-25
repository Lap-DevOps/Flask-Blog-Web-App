import os
from dotenv import load_dotenv
from envparse import env

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'hard to guess string'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    # DATABASE Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL Settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # RECAPTCHA Settings
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS = dict(
        theme='custom',
        custom_theme_widget='recaptcha_widget'
    )
    RECAPTCHA_ENABLED = False
    RECAPTCHA_THEME = 'dark'
    RECAPTCHA_SIZE = "compact"
    RECAPTCHA_LANGUAGE = "ru"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATION = True
    SQLALCHEMY_RECORD_QUERIES = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False




class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

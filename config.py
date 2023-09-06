class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'ce1e098bee3e893eb8a108629f3fc117'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
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

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()
moment = Moment()
migrate = Migrate(db)

from flaskblog.main.routes import main
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.errors.error_handelers import errors


# from flaskblog.users.utils import *


def create_app(config_name):
    # Create Flask app load app.config
    app = Flask(__name__)
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

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


# from flaskblog.users.utils import *


def crate_app(config_class=Configuration):
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(Configuration)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app

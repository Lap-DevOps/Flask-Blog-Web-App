from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail

from config import Configuration


# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(Configuration)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


mail = Mail(app)

moment = Moment(app)

migrate = Migrate(app, db)


from flaskblog.main.routes import main
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
# from flaskblog.users.utils import *


app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
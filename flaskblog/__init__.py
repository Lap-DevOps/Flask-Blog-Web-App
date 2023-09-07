from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

migrate = Migrate(app, db)

from flaskblog import routes
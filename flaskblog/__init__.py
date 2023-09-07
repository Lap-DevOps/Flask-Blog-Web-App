from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from config import Configuration

# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(Configuration)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

from flaskblog import routes

migrate = Migrate(app, db)


#!/usr/bin/env python


from flask_migrate import Migrate
from flaskblog import  *

from flaskblog import current_app

migrate = Migrate(current_app, db)

@app.cli.command('my_custom_command')
def db_init():
    """This is a custom CLI command."""
    print("Running my custom command...")
    # Ваш код



if __name__ == "__main__":
    pass

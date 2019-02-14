import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension


# Allez les extensiones!
login = LoginManager()
# this tells flask-login which view function handles logins
login.login_view = 'auth.login'
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
debug_toolbar = DebugToolbarExtension()


# app factory
def create_app(test_config=None):
    """ create the Flask instance.
    instance_relative_config=True tells the app that config files
    are relative to the instance folder. The instance folder is
    located outside the chingu package and can hold data that
    shouldn't be commited to version control.
    """
    app = Flask(__name__, instance_relative_config=True)
    # set some default configurations
    app.config.from_object('config.settings')
    # silet=True for silent failures if missing files
    app.config.from_pyfile('settings.py', silent=True)

    if test_config:
        app.config.update(test_config)

    # Allez les extensiones!
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)

    from chingu.auth import bp as auth_bp
    """ the url_prefix is optional - any routes defined in this bp will get
    this prefix in their URLs. Useful for namespacing
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from chingu.core import bp as core_bp
    app.register_blueprint(core_bp)

    return app

# imported below app instantiation to avoid circular imports
from chingu import models

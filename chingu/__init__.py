import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Allez les extensiones!
login = LoginManager()
db = SQLAlchemy()


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
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'chingu.sqlite'),
        # if no env var is set a sqlite db will be cretaed in /instance
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        os.path.join(app.instance_path, 'chingu.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        # overrides default config with values from config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in (instead of instance config)
        app.config.from_mapping(test_config)

    # ensure the instance folder exists (that is where SQLite will be)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Allez les extensiones!
    db.init_app(app)
    login.init_app(app)

    from app.auth import bp as auth_bp
    """ the url_prefix is optional - any routes defined in this bp will get
    this prefix in their URLs. Useful for namespacing
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from chingu.core import bp as core_bp
    app.register_blueprint(core_bp)

    return app



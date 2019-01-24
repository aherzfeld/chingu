from flask import Blueprint

bp = Blueprint('core', __name__)

from chingu.core import routes

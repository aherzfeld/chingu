from flask import (current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
#  from chingu import db
#  from chingu.core.forms import
#  from chingu.models import
from chingu.core import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')


#just a test
@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

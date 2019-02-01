from flask import (current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
#  from chingu import db
#  from chingu.core.forms import
#  from chingu.models import
from chingu.core import bp
from chingu.core.forms import QuizSetupForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')

@bp.route('/quiz_setup', methods=['GET', 'POST'])
def quiz_setup():
    form = QuizSetupForm()
    return render_template('quiz_setup.html', form=form)
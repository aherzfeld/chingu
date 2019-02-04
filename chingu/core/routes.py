from flask import (current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
#  from chingu import db
#  from chingu.models import
from chingu.core import bp
from chingu.core.forms import QuizSetupForm, QuestionForm
from chingu.quiz import QuizSetup


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')


@bp.route('/quiz_setup', methods=['GET', 'POST'])
def quiz_setup():
    form = QuizSetupForm()
    if form.validate_on_submit():
        # Instantiate quiz object
        quiz_setup = QuizSetup(category=form.category.data,
            quiz_type=form.quiz_type.data, length=form.length.data)
        quiz_manager = quiz_setup.create_quiz()
        # TODO: Intatiate Quiz Model
        # TODO: Commit Quiz Model into DB (question_list will be empty)
        # user = current_user OR guest (where do I create guest??)
        # TODO: Pass Quiz ID to /quiz via URL???
        # TODO: Serialize question_list to JSON and store in Session
        # Begin the quiz with question at index 0 of quiz.question_list
        return redirect(url_for('core.quiz', question=0))
    return render_template('quiz_setup.html', form=form)


# TODO: also add Quiz ID into URL so we know where to commit questions
@bp.route('/quiz/<question>', methods=['GET', 'POST'])
def quiz(question):
    form = QuestionForm()
    # TODO: pull next question from session and deserialize
    # TODO: commit question to DB after user answers (by Quiz ID in url)
    # TODO: generate feedback via QuizManager
    # TODO: perhaps store quiz state in Session ??
    return render_template('quiz.html', form=form)


# TODO: create quiz/results route











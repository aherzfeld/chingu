from flask import (current_app, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required
from chingu import db
from chingu.models import Question, Quiz
from chingu.core import bp
from chingu.core.forms import QuizSetupForm, QuestionForm
from chingu.quiz import QuizManager, QuizSetup


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')


# TODO: add a decorator to log anonymour users in as Guest???
@bp.route('/quiz_setup', methods=['GET', 'POST'])
def quiz_setup():
    form = QuizSetupForm()
    if form.validate_on_submit():
        # Instantiate quiz "factory" object
        quiz_setup = QuizSetup(category=form.category.data,
                               quiz_type=form.quiz_type.data,
                               length=form.length.data)
        quiz = quiz_setup.setup_quiz()
        # Instatiate Quiz Model and commit to DB (with empty Question list)
        db_quiz = Quiz(category=quiz.category,
                       quiz_type=quiz.type,
                       user=current_user)
        # user = current_user OR guest (where do I create guest??)
        db.session.add(db_quiz)
        db.session.commit()
        # TODO: Serialize question_list to JSON and store in Session
        for q in quiz.question_list:
            session[str(q['n'])] = q
        # Begin the quiz with question at index 0 of quiz.question_list
        return redirect(url_for('core.quiz',
                                quiz_id=db_quiz.quiz_id, question='1'))
    return render_template('quiz_setup.html', form=form)


# TODO: refactor - clean up variable names
@bp.route('/quiz/<int:quiz_id>/<question>', methods=['GET', 'POST'])
def quiz(quiz_id, question):
    q = session[question]
    form = QuestionForm()
    # TODO: abstract some of the below logic into QuizManager
    if form.validate_on_submit():
        # TODO: check user_answer & update Question.correct
        q['correct'] = QuizManager.check(q['answer'], form.answer.data)
        # TEMPORARY
        if q['correct']:
            flash('Correct!')
        else:
            flash(f'Hmm not quite. The correct answer is {q["answer"]}')
        # instantiate Question model object and commit to db
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first_or_404()
        finished_question = Question(key=q['key'],
                                     answer=q['answer'],
                                     definition=q['definition'],
                                     question=q['question'],
                                     correct=q['correct'],
                                     quiz=quiz)
        db.session.add(finished_question)
        db.session.commit()
        # TODO: generate feedback via QuizManager
        # TODO: perhaps store quiz state in Session ??
        # TODO: need logic to check for no more questions (redirect to results)
        n = str(q['n'] + 1)
        if n not in session:
            return redirect(url_for('core.quiz_results', quiz_id=quiz_id))
        return redirect(url_for('core.quiz', quiz_id=quiz_id, question=n))
    return render_template('quiz.html', form=form, question=q)


# TODO: create quiz/results route
@bp.route('quiz/<int:quiz_id>/results', methods=['GET', 'POST'])
def quiz_results(quiz_id):
    pass









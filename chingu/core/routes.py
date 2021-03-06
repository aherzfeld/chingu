from flask import (flash, redirect, render_template, session, url_for)
from flask_login import current_user  # login_required
from chingu import db
from chingu.models import Noun, Question, Quiz, Verb
from chingu.core import bp
from chingu.core.forms import (NewNounForm, NewVerbForm, QuizSetupForm,
                               QuestionForm)
from chingu.quiz import QuizManager, QuizSetup


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')


# TODO: decorator to only allow admin User
@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    noun_form = NewNounForm()
    verb_form = NewVerbForm()
    # maybe the below validation could move into form validations
    if noun_form.noun_submit.data and noun_form.validate():
        db_noun = Noun.query.filter_by(word=noun_form.word.data).first()
        if db_noun:
            flash(f'{db_noun.word} is already in the database', 'warning')
            return redirect(url_for('core.admin'))
        noun = Noun(category=noun_form.category.data,
                    word=noun_form.word.data,
                    definition=noun_form.definition.data)
        db.session.add(noun)
        db.session.commit()
        flash('New noun added.', 'success')
        return redirect(url_for('core.admin'))
    # verb_form
    if verb_form.verb_submit.data and verb_form.validate():
        db_verb = Noun.query.filter_by(word=verb_form.word.data).first()
        if db_verb:
            flash(f'{db_verb.word} is already in the database', 'warning')
            return redirect(url_for('core.admin'))
        verb = Verb(word=verb_form.word.data,
                    definition=verb_form.definition.data)
        db.session.add(verb)
        db.session.commit()
        flash('New verb added.', 'success')
        return redirect(url_for('core.admin'))
    return render_template('admin.html',
                           noun_form=noun_form,
                           verb_form=verb_form)


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
        q['correct'] = QuizManager.check(q['answer'], form.answer.data)
        # TEMPORARY
        if q['correct']:
            flash('Correct!', 'info')
        else:
            flash(f'Hmm not quite. The correct answer is {q["answer"]}', 'info')
        # query db for quiz-parent of question
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first_or_404()
        finished_question = Question(key=q['key'],
                                     answer=q['answer'],
                                     definition=q['definition'],
                                     question=q['question'],
                                     correct=q['correct'],
                                     quiz=quiz)
        db.session.add(finished_question)
        db.session.commit()
        # remove the question from flask session
        session.pop(question)
        # TODO: generate feedback via QuizManager
        n = str(q['n'] + 1)
        if n not in session:
            return redirect(url_for('core.quiz_results', quiz_id=quiz_id))
        return redirect(url_for('core.quiz', quiz_id=quiz_id, question=n))
    return render_template('quiz.html', form=form, question=q)


@bp.route('/quiz/<int:quiz_id>/results', methods=['GET', 'POST'])
def quiz_results(quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first_or_404()
    return render_template('quiz_results.html',
                           quiz_string=quiz.__str__(),
                           results=quiz.results())









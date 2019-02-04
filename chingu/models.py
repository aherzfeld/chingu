from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from time import time  # used for password reset tokens
import jwt  # JSON web tokens for password reset
from flask import current_app
from flask_login import UserMixin
from chingu import db, login


# TODO: combine Question class and model into one model here
# TODO: combine Quiz class and model into one model here
# TODO: Analyse viability, then remove need for old_db.py
# TODO: create mini-classes for quiz categories / quiz_types
# to be used by Quiz_Setup, QuizSetupForm validation etc
# TODO: consider namedtuple for quiz results output etc


class Question(db.Model):
    """ Question object that will be a part of a Quiz's question_list """

    __tablename__ = 'questions'

    question_id = db.Column('id', db.Integer, primary_key=True)
    key = db.Column(db.String)
    answer = db.Column(db.String)
    definition = db.Column(db.String)
    question = db.Column(db.String)
    correct = db.Column(db.Boolean)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))

    quiz = db.relationship('Quiz', back_populates='questions')

    def __init__(self, key, answer, definition, question):
        """ Initiate using params prepared by Quiz object

        Params:
            key - word/item to be tested from subject dictionary
            answer - correct answer generated via Quiz.type_method
            definition - word definition from subject dict
            question - question_string created by quiz.Quiz

        """
        self.key = key
        self.answer = answer
        self.definition = definition
        self.question = question
        self.correct = None

    # Just in case I need this until confirmed working
    # def check(self, user_answer):
    #     """ Return True if user input answer is correct """

    #     # the length check allows for incomplete, but close enough definitions
    #     self.correct = user_answer in self.answer and (
    #         len(user_answer) >= (len(self.answer) / 3))
    #     return self.correct

    def __repr__(self):
        return (f"<Question(key='{self.key}', answer='{self.answer}', "
                f"definition='{self.definition}', question='{self.question}', "
                f"correct={self.correct}, quiz_id={self.quiz_id})>")


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    quiz_id = db.Column('id', db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    quiz_type = db.Column('type', db.String, nullable=False)
    taken_on = db.Column(db.String,
                         default=datetime.utcnow().isoformat(' ', 'seconds'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    questions = db.relationship('Question', order_by=Question.question_id,
                                back_populates='quiz')
    user = db.relationship('User', back_populates='quizzes')

    def __repr__(self):
        return (f"<Quiz(category='{self.category}', "
                f"quiz_type='{self.quiz_type}', quiz_id={self.quiz_id}, "
                f"taken_on={self.taken_on}>)")


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db.String because sqlite has no DateTime type isoformat='YYYY-MM-DD'
    created_on = db.Column(db.String,
                           default=datetime.utcnow().isoformat(' ', 'seconds'))
    # num_correct , num_wrong

    quizzes = db.relationship('Quiz', order_by=Quiz.quiz_id,
                              back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    '''
    the jwt.encode() function returns the token as a byte sequence, but we
    use decode(utf-8) here to return it as a string
    '''

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @property
    def num_correct(self):
        pass

    @property
    def num_wrong(self):
        pass

    def __repr__(self):
        return (f"<User(id={self.id}, username='{self.username}',"
                f" created_on={self.created_on})")


# user loader function to help flask-login load a user from the db
# flask-login passes the id as a string so it needs to be converted for the db
@login.user_loader
def load_user(id):
    return User.query.get(int(id))




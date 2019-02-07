from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


#TODO: use javascript to dynamically update quiz_type based on category
class QuizSetupForm(FlaskForm):
    category = SelectField('Category', choices=[('verb', 'Verb'),
                                                ('noun', 'Noun')],
                           validators=[DataRequired()])
    quiz_type = SelectField('Quiz Type', choices=[('definition', 'Definition'),
                                                  ('present', 'Present Tense'),
                                                  ('noun', 'Noun')],
                            validators=[DataRequired()])
    length = IntegerField('Length', validators=[DataRequired(),
                                                NumberRange(min=1, max=20)])
    submit = SubmitField('Start Quiz')


class QuestionForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')


# TODO: remove categories for now - Keep it Simple
class NewNounForm(FlaskForm):
    category = SelectField('Category', choices=[('body', 'Body'),
        ('clothing', 'Clothing'), ('family', 'Family'), ('home', 'Home'),
        ('numbers', 'Numbers'), ('transportation', 'Transportation')])
    word = StringField('Korean Word', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Save')

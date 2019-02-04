from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.validators import AnyOf, DataRequired, NumberRange


class QuizSetupForm(FlaskForm):
    category = SelectField('Category', choices=[('verb', 'Verb')],
        validators=[DataRequired()])
    quiz_type = SelectField('Quiz Type', choices=[('definition', 'Definition'),
        ('present', 'Present Tense')], validators=[DataRequired()])
    length = IntegerField('Length', validators=[DataRequired(),
                                                NumberRange(min=1, max=20)])
    submit = SubmitField('Start Quiz')


class QuestionForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')

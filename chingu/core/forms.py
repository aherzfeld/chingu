from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import AnyOf, DataRequired, NumberRange


class QuizSetupForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(),
        AnyOf(['verb'])])
    quiz_type = StringField('Quiz Type', validators=[DataRequired(),
        AnyOf(['definition', 'present'])])
    length = IntegerField('Length', validators=[DataRequired(),
                                                NumberRange(min=1, max=20)])
    submit = SubmitField('Start Quiz')

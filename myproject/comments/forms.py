from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired


class CommentForm(FlaskForm):
    text = TextAreaField('Text', validators=[InputRequired()])
    submit = SubmitField('Comment')

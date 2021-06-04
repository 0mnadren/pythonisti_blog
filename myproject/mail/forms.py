from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length


class MessageForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=55)])
    receiver = SelectField(u'Send To', choices=[], validators=[InputRequired()])
    text = TextAreaField('Text', validators=[InputRequired()])
    submit = SubmitField('Send')



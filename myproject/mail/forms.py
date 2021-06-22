from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, ValidationError
from wtforms.validators import InputRequired, Length
from myproject.models import User


def check_receiver(form, field):
    if not User.query.filter_by(username=field.data.lower()).first():
        raise ValidationError('User does not exist!')
# usernames are saved in db as lowercase!


class MessageForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=55)])
    receiver = StringField('Send To', validators=[InputRequired(), check_receiver])
    text = TextAreaField('Text', validators=[InputRequired()])
    submit = SubmitField('Send')





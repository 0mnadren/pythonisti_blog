from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
# A file field and allowed are going to let us have the user update jpeg or png file

from myproject.models import User


def check_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Your email has been registered already!')


def check_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already taken!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), check_email])
    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=4, max=24, message='Minimum length is 4 letters'),
                                                   check_username])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     EqualTo('confirm_pass', message='Passwords must match'),
                                                     Length(min=8, max=24, message='Minimum length of a password is 8')])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Register')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=4, max=24, message='Minimum length is 4 letters')])
    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UpdateImageForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Image')


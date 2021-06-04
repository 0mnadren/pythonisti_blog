from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=64)])
    text = TextAreaField('Text', validators=[InputRequired()])
    submit = SubmitField('Post')

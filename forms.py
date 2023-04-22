from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

class CreateUserForm(FlaskForm):
    '''Form for registering or creating a new user.'''
    username   = StringField("Username", validators=[InputRequired('Username Required')])
    password   = PasswordField("Password", validators=[InputRequired('Password Required')])
    email      = EmailField("Email", validators=[InputRequired('Email Required')])
    first_name = StringField("First name", validators=[InputRequired('First name Required')])
    last_name  = StringField("Last name", validators=[InputRequired('Last name Required')])

class LoginUserForm(FlaskForm):
    '''Form for logging in a user.'''
    username = StringField("Username", validators=[InputRequired('Username Required')])
    password = PasswordField("Password", validators=[InputRequired('Password Required')])
    
class FeedbackForm(FlaskForm):
    '''Form for adding feedback.'''
    title   = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Feedback", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    '''Intentionally blank form used for deletion of users/feedback'''

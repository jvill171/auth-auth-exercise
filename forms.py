from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class CreateUserForm(FlaskForm):
    '''Form for registering or creating a new user.'''
    username    = StringField("Username", validators=[InputRequired('Username Required')])
    password    = StringField("Password", validators=[InputRequired('Password Required')])
    email       = StringField("Email", validators=[InputRequired('Email Required')])
    first_name  = StringField("First name", validators=[InputRequired('First name Required')])
    last_name   = StringField("Last name", validators=[InputRequired('Last name Required')])

class LoginUserForm(FlaskForm):
    '''Form for logging in a user.'''
    username    = StringField("Username", validators=[InputRequired('Username Required')])
    password    = StringField("Password", validators=[InputRequired('Password Required')])
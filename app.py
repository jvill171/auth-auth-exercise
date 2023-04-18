from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY']="auth-auth-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_auth'
# Specify database


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    '''Redirect to /register page'''
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    ['GET']
    Show a form that when submitted will register/create a user.
    This form accepts a username, password, email, first_name, and last_name.
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!

    ['POST']
    Process the registration form by adding a new user. Then redirect to /secret
    '''
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    ['GET']
    Show a form that when submitted will login a user. This form should accept a username and a password.
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!

    ['POST']
    Process the login form, ensuring the user is authenticated and going to /secret if so.
    '''
    return render_template('login.html')

@app.route('/secret')
def secret():
    '''
    Return the text “You made it!” (don't worry, we'll get rid of this soon)
    '''
    html="<h1>You made it!</h1>"
    return html

# @app.route('/')
# def homepage():
#     return render_template('base.html')

# @app.route('/')
# def homepage():
#     return render_template('base.html')
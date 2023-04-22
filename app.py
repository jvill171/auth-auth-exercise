from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import CreateUserForm, LoginUserForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized

import sqlalchemy
from psycopg2 import errors

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY']="auth-auth-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_auth'
# Specify database


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

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
    Display a form for users to register a new account with.
    Successful registration: create user in DB, add username to session['username'], and redirect to /users/<username>
    '''
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = CreateUserForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)
        try:
            db.session.commit()
            session['username'] = new_user.username
            return redirect(f'/users/{new_user.username}')
        except sqlalchemy.exc.IntegrityError as sqla_error:
            try:
                raise sqla_error.orig
            except (errors.UniqueViolation):
                flash("An account with that Username/Email already exists!", 'danger')

    return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Display a form for users to log in with.
    Successful login: add username to session['username'] & redirect to /users/<username>
    '''
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginUserForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.authenticate(**data)

        if(user):
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username or password"]
            return render_template("users/login.html", form=form)
    
    return render_template('users/login.html', form=form)

@app.route('/users/<username>')
def secret(username):
    '''
    Display info about the user, including any of the user's feedback 
    Login Required.
    '''
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get_or_404(username)
    form=DeleteForm()  
    return render_template('users/user.html', user=user, form=form)

@app.route('/logout')
def logout():
    '''Log out currently logged in user'''
    try:
        session.pop('username')
    except Exception:
        # User tried to access /logout route while logged out
        pass
    return redirect('/login')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''
    Delete the user from the DB & delete all of their feedback.
    Clear any user information in the session and redirect to /
    Login Required.
    '''
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Display a form to add feedback. On submission, adds to DB and redirect to /users/<username>
         Login Required.'''
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        new_feedback = Feedback(
            title = title,
            content = content, 
            username = username
        )
        
        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')
        
    return render_template('feedback/add-feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''
    Displays a form to edit feedback. When submitted, updates DB and redirects to /users/<username>
    Login Required.
    '''
    fb = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or fb.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=fb)

    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content= form.content.data
        db.session.commit()
        return redirect(f'/users/{fb.username}')

    return render_template('/feedback/edit-feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''
    Deletes a specific feedback & redirects to /users/<username>
    Login Required.
    '''
    fb = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or fb.username != session['username']:
        raise Unauthorized()
    
    user = fb.username
    db.session.delete(fb)
    db.session.commit()

    return redirect(f'/users/{user}')

@app.errorhandler(401)
def page_err_401(error):
    '''Renders 401 error page'''
    return render_template('401.html', err=error),401

@app.errorhandler(404)
def page_err_404(error):
    '''Renders 404 error page'''
    return render_template('404.html', err=error),404

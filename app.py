from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# app.app_context().push()

app.config['SECRET_KEY']=""
# ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY ADD SECRET KEY

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'
# Specify database


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# connect_db(app)
# db.create_all()


@app.route('/')
def homepage():
    return render_template('base.html')
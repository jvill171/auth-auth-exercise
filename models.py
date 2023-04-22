from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    '''Connect to database.'''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User.'''
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name} >"

    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref='user', cascade='all, delete')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        '''Register a new user w/ hashed password'''

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username  = username,
            password  = hashed_utf8,
            email     = email,
            first_name= first_name,
            last_name = last_name
        )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        '''
        Validate that a user exists & password is correct.
        If valid: return user;  Else: return False;
        '''
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    '''Feedback'''
    __tablename__ = 'feedback'
    
    def __repr__(self):
        f = self
        return f"<Feedback id={f.id} title={f.title} content={f.content} username={f.username}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
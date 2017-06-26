# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Trainee(UserMixin, db.Model):
    """
    Create an Trainee table
    """

    # Table will be named in singular
    # as is the name of the model
    __tablename__ = 'trainee'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Trainee.query.get(int(user_id))

class Trainer(db.Model):
    """
    Create a Trainer table
    """

    __tablename__ = 'trainer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    trainee = db.relationship('Trainee', backref='trainer',
                                lazy='dynamic')

    def __repr__(self):
        return '<Coached By Trainer: {}>'.format(self.name)

class Session(db.Model):
    """
    Create a Session table
    """

    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    trainee = db.relationship('Trainee', backref='session',
                                lazy='dynamic')

    def __repr__(self):
        return '<Session: {}>'.format(self.name)

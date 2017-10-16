# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class RemoteUser(UserMixin, db.Model):
    """
    Create an RemoteUser table
    """

    __tablename__ = 'remoteusers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
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
        return '<RemoteUser: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return RemoteUser.query.get(int(user_id))




class Event(db.Model):
    """
    Create a Events table
    """

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    fullnames = db.Column(db.String(100), unique=True)
    mobilenumber = db.Column(db.Integer, index=True, unique=True)
    nationalid = db.Column(db.Integer,index=True, unique=True)
    deptamount = db.Column(db.Integer, index=True)
    description = db.Column(db.String(200))
    scscomment = db.Column(db.String(200))
    fmcomment = db.Column(db.String(200))
    amcomment = db.Column(db.String(200))
    pmcomment = db.Column(db.String(200))
    sbcomment = db.Column(db.String(200))
    appstatus = db.Column(db.String(50))
    emailsent = db.Column(db.String(200))
    emailrecepient= db.Column(db.String(50))
    # remoteusers = db.relationship('RemoteUser', backref='events',
    #                             lazy='dynamic')

    def __repr__(self):
        return '<Event: {}>'.format(self.fullnames)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    remoteusers = db.relationship('RemoteUser', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

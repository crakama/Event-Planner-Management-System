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
    is_scsadmin = db.Column(db.Boolean, default=False)
    is_hradmin = db.Column(db.Boolean, default=False)

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

class StaffRequest(db.Model):
    """
    Create Staff request Table:
    """
    __tablename__ = 'staffrequests'

    id = db.Column(db.Integer,primary_key=True)
    requestname = db.Column(db.String(50))
    contracttype = db.Column(db.String(50))
    departmentname = db.Column(db.String(50))
    jobtitle = db.Column(db.String(50))
    jobdescription = db.Column(db.String(200))
    hrcomment = db.Column(db.String(200))
    requeststatus = db.Column(db.String(50))

    def __repr__(self):
        return '<StaffRequest: {}>'.format(self.requestname)

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
    task = db.Column(db.String(50))
    emailsent = db.Column(db.String(200))
    emailrecepient= db.Column(db.String(50))
    task_id = db.relationship('Task', backref='taskowner',
                                lazy='dynamic')
    # task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def __repr__(self):
        return '<Event: {}>'.format(self.fullnames)
############Task#################################

class Task(db.Model):
    """
    Create a Task table
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    listeventid = db.Column(db.Integer,index=True, unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    # event_id = db.relationship('task', backref='events',
    #                             lazy='dynamic')

#######################Task ###################
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

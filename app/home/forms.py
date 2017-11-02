# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,RadioField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Event, Role

class TaskForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """

    taskname = StringField('Name of Task', validators=[DataRequired()])
    taskdescription = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')




class HrApprovalForm(FlaskForm):
    """
    Form for
    """
    hrcomment = StringField('HR Comment', validators=[DataRequired()])
    requestapproval = RadioField('Contract Type', choices=[('True','Accept'),('False','Reject')])
    submit = SubmitField('Submit')

class StaffRequestForm(FlaskForm):
    """
    Form for admin to
    """
    requestname = StringField('Name of Request')
    contracttype = RadioField('Contract Type', choices=[('True','Full Time'),('False','Part Time')])
    departmentname = StringField('Department Requesting')
    jobtitle = StringField('Job Title')
    jobdescription = StringField('Job Description')
    submit = SubmitField('Submit')

class SCSCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    scscomment = StringField('SCS Comments')
    appapproval = RadioField('Approval', choices=[('True','Accept'),('False','Reject')])
    submit = SubmitField('Submit')

class PMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    pmcomment = StringField('Production Manager Comments')
    submit = SubmitField('Submit')

class AMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    amcomment = StringField('Administration Manager Comments')
    appapproval = RadioField('Approval', choices=[('True','Accept'),('False','Reject')])
    submit = SubmitField('Submit')

class FMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    fmcomment = StringField('Finance Manager Comments')
    submit = SubmitField('Submit')

class SendEmailForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    scssendemail = StringField('Email Subject')
    emailrecepient = StringField('Email Recepients')
    submit = SubmitField('Submit')


class SBCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    sbtcomments = StringField('Sub Team Task Activity Plan')
    submit = SubmitField('Submit')

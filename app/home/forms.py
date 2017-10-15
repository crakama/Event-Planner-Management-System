# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,RadioField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Event, Role

# class EventForm(FlaskForm):
#     """
#     Form for admin to add or edit an event
#     """
#     # fullname = StringField('Name', validators=[DataRequired()])
#     # mobileno = IntegerField('Mobile Number', validators=[DataRequired()])
#     # nationalid = IntegerField('ID Number', validators=[DataRequired()])
#     # deptamount = IntegerField('Amount', validators=[DataRequired()])
#     # description = StringField('EventDescription', validators=[DataRequired()])
#     scscomment = StringField('SCS Comments')
#     fmcomment = StringField('FM Comments')
#     amcomment = StringField('PM Comments')
#     pmcomment = StringField('STeam Comments')
#     sbcomment = StringField('AM Comments')
#     submit = SubmitField('Submit')

class SCSCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    scscomment = StringField('SCS Comments')
    appapproval = RadioField('Approval', choices=[('True','Accept'),('False','Reject')])
    submit = SubmitField('Submit')

class FMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    fmcomment = StringField('SCS Comments')
    submit = SubmitField('Submit')

class AMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    amcomment = StringField('SCS Comments')
    submit = SubmitField('Submit')

class PMCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    pmcomment = StringField('SCS Comments')
    submit = SubmitField('Submit')

class SBCommentForm(FlaskForm):
    """
    Form for admin to add or edit an event
    """
    sbcomment = StringField('SCS Comments')
    submit = SubmitField('Submit')

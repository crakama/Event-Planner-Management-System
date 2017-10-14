# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Event, Role

class EventForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    fullname = StringField('Name', validators=[DataRequired()])
    mobileno = IntegerField('Mobile Number', validators=[DataRequired()])
    nationalid = IntegerField('ID Number', validators=[DataRequired()])
    deptamount = IntegerField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RemoteUserAssignForm(FlaskForm):
    """
    Form for admin to assign roles to remote users
    QuerySelectField queries the database for all roles.
    """
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

# app/admin/__init__.py

from flask import Blueprint

scsadmin = Blueprint('scsadmin', __name__)

from . import views

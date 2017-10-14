# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from ..models import Event

# Each view handles requests to the specified URL

# admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/deptdashboard', methods=['GET', 'POST'])
@login_required
def deptdashboard():
    """
    List all events
    """

    events = Event.query.all()

    return render_template('admin/events/listevents.html',
                           events=events, title="Events")


# @home.route('/deptdashboard')
# @login_required
# def deptdashboard():
#     """
#     Render the deptdashboard template on the /deptdashboard route
#     """
#     return render_template('admin/events/listevents.html', title="DeptDashboard")

@home.route('/deptreport')
@login_required
def deptreport():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/deptreport.html', title="DeptReport")

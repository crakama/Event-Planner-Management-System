# app/home/views.py

from flask import abort, render_template,flash, redirect,url_for
from flask_login import current_user, login_required

from . import home
from forms import SCSCommentForm, FMCommentForm, AMCommentForm, PMCommentForm, SBCommentForm
from .. import db
from ..models import Event, Role

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

@home.route('/eventdashboard', methods=['GET', 'POST'])
@login_required
def eventdashboard():
    """
    List all events
    """

    events = Event.query.all()
    # roles = Role.query.all()
    # form = EventForm()
    # if roles.name == "":
    #     del form.


    return render_template('admin/events/listevents.html',
                           events=events, title="Events")

# -----------------------------
@home.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def scscomment_event(id):
    """
    Edit an Event
    """

    scscomment_event = True
    # statusdata = {'title':'Status','status':['Open','Closed']}

    event = Event.query.get_or_404(id)
    form = SCSCommentForm(obj=event)
    if form.validate_on_submit():
        event.scscomment = form.scscomment.data
        if form.appapproval.data == "True":
            status = "Open"
        status = "Closed"
        event.appstatus = status
        # event.appstatus = form.appapproval.data
        db.session.commit()
        flash('You have successfully edited an event.')

        # redirect to the events page
        return redirect(url_for('home.eventdashboard'))

    form.scscomment.data = event.scscomment
    # if form.appapproval.data == "True":
    #     status = "Open"
    # status = "Closed"
    form.appapproval.data= event.appstatus 

    return render_template('admin/events/addeditevent.html', action="Edit",
                           scscomment_event=scscomment_event, form=form,
                           event=event, title="Edit Event")
# -----------------
    # event.fmcomment = form.fmcomment.data
    # event.amcomment = form.amcomment.data
    # event.pmcomment = form.pmcomment.data
    # event.sbcomment = form.sbcomment.data
    #
    # form.fmcomment.data = event.fmcomment
    # form.amcomment.data = event.amcomment
    # form.pmcomment.data = event.pmcomment
    # form.sbcomment.data = event.sbcomment


@home.route('/deptreport')
@login_required
def deptreport():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/deptreport.html', title="DeptReport")

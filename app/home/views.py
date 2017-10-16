# app/home/views.py

from flask import abort, render_template,flash, redirect,url_for
from flask_login import current_user, login_required
from flask_mail import Mail, Message
from app import mail
from . import home
from forms import SCSCommentForm, FMCommentForm, AMCommentForm, PMCommentForm, SBCommentForm, SendEmailForm
from .. import db
from ..models import Event, Role, RemoteUser

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
    user = RemoteUser.query.filter_by(username='scsadmin').first()
    scsname2 = user
    scsname3 = user

    return render_template('admin/events/listevents.html',
                           events=events, scsname3=scsname3,scsname2=scsname2, title="Events")


@home.route('/events/send/<int:id>', methods=['GET', 'POST'])
@login_required
def scssend_email(id):
    """
    Edit an Event
    """

    scssend_email = True

    event = Event.query.get_or_404(id)
    form = SendEmailForm(obj=event)

    if form.validate_on_submit():
        msg = Message('Hello', sender = 'katerak2013@gmail.com', recipients = [form.emailrecepient.data])
        msg.body = form.scssendemail.data
        mail.send(msg)
        event.emailsent = form.scssendemail.data
        db.session.commit()
        flash('You have successfully Sent an Email.')

        # redirect to the events page
        return redirect(url_for('home.eventdashboard'))

    form.scssendemail.data = event.emailsent
    form.emailrecepient.data = event.emailrecepient

    return render_template('admin/events/addeditevent.html', action="Edit",
                           scssend_email=scssend_email, form=form,
                           event=event, title="Edit Event")

# -----------------------------
@home.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def scscomment_event(id):
    """
    Edit an Event
    """

    scscomment_event = True

    event = Event.query.get_or_404(id)
    form = SCSCommentForm(obj=event)
    if form.validate_on_submit():
        event.scscomment = form.scscomment.data
        db.session.commit()
        flash('You have successfully edited an event.')

        # redirect to the events page
        return redirect(url_for('home.eventdashboard'))

    form.scscomment.data = event.scscomment

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

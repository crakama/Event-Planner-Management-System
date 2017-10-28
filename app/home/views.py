# app/home/views.py

from flask import abort, render_template,flash, redirect,url_for
from flask_login import current_user, login_required
from flask_mail import Mail, Message
from app import mail
from . import home
from forms import SCSCommentForm, FMCommentForm, TaskForm
from forms import AMCommentForm, PMCommentForm, SBCommentForm, SendEmailForm,StaffRequestForm
from .. import db
from ..models import Event, Role, RemoteUser, Task, StaffRequest

# Each view handles requests to the specified URL

# admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

# admin dashboard view
@home.route('/scsadmin/dashboard')
@login_required
def scsadmin_dashboard():
    # prevent non-scsadmins from accessing the page
    if not current_user.is_scsadmin:
        abort(403)

    return render_template('home/scsadmin_dashboard.html', title="Dashboard")

# admin dashboard view
@home.route('/hradmin/dashboard')
@login_required
def hradmin_dashboard():
    # prevent non-scsadmins from accessing the page
    # if not current_user.is_hradmin:
    #     abort(403)

    return render_template('admin/events/liststaffrequest.html', title="Dashboard")

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
    scsname3 = "scsadmin"

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
        if form.appapproval.data == "True":
            status = "Open"
        else:
            status = "Closed"
        event.appstatus = status
        db.session.commit()
        flash('You have successfully added a event.')

        # redirect to the events page
        return redirect(url_for('home.eventdashboard'))

    form.scscomment.data = event.scscomment
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

############## Staff Request################
@home.route('/staffrequests/add', methods=['GET', 'POST'])
@login_required
def add_staffrequest():
    """
    Add a request
    """
    # add_staffrequest = True
    form = StaffRequestForm()
    if form.validate_on_submit():
        if form.contracttype.data == "True":
            ctype = "Full Time"
        else:
            ctype = "Part Time"
        staffrequest = StaffRequest(requestname=form.requestname.data,
                    contracttype=ctype,
                    departmentname=form.departmentname.data,
                    jobtitle=form.jobtitle.data,
                    jobdescription=form.jobdescription.data)
        try:
            # add role to the database
            db.session.add(staffrequest)
            db.session.commit()
            flash('You have successfully sent staff request!')
        except:
            # in case role name already exists
            flash('Error: staff request name already exists.')

        return redirect(url_for('home.eventdashboard'))

    return render_template('admin/events/addeditevent.html', action="Edit",
                           add_staffrequest=add_staffrequest, form=form,
                            title="Add Task")
############# Task Request ################

#################Task###################
@home.route('/tasks/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_task(id):
    """
    Add a Task
    """

    add_event = True

    event = Event.query.get_or_404(id)
    # tasks = Task.query.get_or_404(id)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(taskname=form.taskname.data,
                    description=form.taskdescription.data,
                    listeventid =id,
                    taskowner=event)

        try:
            # add role to the database
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
            # in case role name already exists
            flash('Error: task name already exists.')

        return redirect(url_for('home.eventdashboard',id=id,task=task))

    return render_template('admin/events/addeditevent.html', action="Edit",
                           add_event=add_event, form=form,
                           event=event, title="Add Task")
@home.route('/tasks')
@login_required
def list_staffrequest():
    # check_admin()
    """
    List all staff requests
    """
    staffrequests = StaffRequest.query.all()
    return render_template('admin/events/liststaffrequest.html',
                           staffrequests=staffrequests, title='Tasks')

@home.route('/task/list/<int:id>', methods=['GET', 'POST'])
@login_required
def select_tasks(id):
    # check_admin()
    """
    List all tasks
    """
    # select_tasks =False
    tasks = Task.query.filter(Task.listeventid==id).all()
    # tasks = Task.query.filter_by(listeventid=id).all()
    e_id = id


    return render_template('home/tasks/listtasks.html',
                           tasks=tasks, select_tasks=select_tasks,e_id=e_id, title='Tasks')
@home.route('/tasks')
@login_required
def list_tasks():
    # check_admin()
    """
    List all tasks
    """
    tasks = Task.query.all()
    return render_template('admin/tasks/listtasks.html',
                           tasks=tasks, title='Tasks')


@home.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a task
    """
    # check_admin()

    add_task = False

    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        db.session.add(task)
        db.session.commit()
        flash('You have successfully edited the task.')

        # redirect to the roles page
        return redirect(url_for('home.list_tasks', id =id))

    form.taskdescription.data = task.description
    form.taskname.data = task.taskname
    return render_template('home/tasks/addedittask.html', add_task=add_task,
                           form=form, title="Edit Task")


@home.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a task from the database
    """
    # check_admin()

    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the task.')

    # redirect to the tasks page
    return redirect(url_for('home.list_tasks'))

    return render_template(title="Delete Task")
########################Task################################################

@home.route('/deptreport')
@login_required
def deptreport():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/deptreport.html', title="DeptReport")
# mysql -u root -p

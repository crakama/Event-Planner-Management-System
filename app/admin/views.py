# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import EventForm, RemoteUserAssignForm, RoleForm,SendEmailForm
from .. import db
from ..models import Event, RemoteUser, Role,Task

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

################################  Event Views ################################

@admin.route('/events', methods=['GET', 'POST'])
@login_required
def list_events():
    """
    List all events
    """
    check_admin()

    events = Event.query.all()

    return render_template('admin/events/listevents.html',
                           events=events, title="Events")

@admin.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    """
    Add an event to the database
    """
    check_admin()

    add_event = True

    form = EventForm()
    if form.validate_on_submit():
        event = Event(fullnames=form.fullname.data,
                      mobilenumber=form.mobileno.data,
                      nationalid=form.nationalid.data,
                      deptamount=form.deptamount.data,
                      description=form.description.data)
        try:
            # add event to the database
            db.session.add(event)
            db.session.commit()
            flash('You have successfully added a new event request.')
        except:
            # in case event name already exists
            flash('Error: event name already exists.')

        # redirect to events page
        return redirect(url_for('admin.list_events'))

    # load event template
    return render_template('admin/events/addeditevent.html', action="Add",
                           add_event=add_event, form=form,
                           title="Add Event")

@admin.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    """
    Edit an Event
    """
    check_admin()

    add_event = False

    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.fullnames = form.fullname.data
        event.mobilenumber = form.mobileno.data
        event.nationalid = form.nationalid.data
        event.deptamount = form.deptamount.data
        event.description = form.description.data
        db.session.commit()
        flash('You have successfully edited an event.')

        # redirect to the events page
        return redirect(url_for('admin.list_events'))

    form.fullname.data = event.fullnames
    form.mobileno.data = event.mobilenumber
    form.nationalid.data = event.nationalid
    form.deptamount.data = event.deptamount
    form.description.data = event.description
    return render_template('admin/events/addeditevent.html', action="Edit",
                           add_event=add_event, form=form,
                           event=event, title="Edit Event")

@admin.route('/events/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    """
    Delete a event from the database
    """
    check_admin()

    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('You have successfully deleted a event.')

    # redirect to the events page
    return redirect(url_for('admin.list_events'))

    return render_template(title="Delete Event")



#######################    Tasks #####################################################


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Add a role to the database
    """
    check_admin()

    add_task = True

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(taskname=form.name.data,
                    description=form.description.data)

        try:
            # add task to the database
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
            # in case task name already exists
            flash('Error: task name already exists.')

        # redirect to the tasks page
        return redirect(url_for('admin.list_tasks'))

    # load tasks template
    return render_template('admin/tasks/addedittask.html', add_task=add_task,
                           form=form, title='Edit Task')
@admin.route('/tasks')
@login_required
def list_tasks():
    # check_admin()
    """
    List all tasks
    """
    tasks = Task.query.all()
    return render_template('admin/tasks/listtasks.html',
                           tasks=tasks, title='Tasks')

@admin.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a task
    """
    check_admin()

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
        return redirect(url_for('admin.list_tasks'))

    form.description.data = task.description
    form.name.data = task.taskname
    return render_template('admin/tasks/addedittask.html', add_task=add_task,
                           form=form, title="Edit Task")

@admin.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a task from the database
    """
    check_admin()

    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the task.')

    # redirect to the tasks page
    return redirect(url_for('admin.list_tasks'))

    return render_template(title="Delete Task")

#######################    Tasks ##############################################


############################## Role Views ###################################

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/listroles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/addeditrole.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/addeditrole.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

# ##########################  Employee Views ###################################

@admin.route('/remoteusers')
@login_required
def list_remoteusers():
    """
    List all remoteusers
    """
    check_admin()

    remoteusers = RemoteUser.query.all()
    return render_template('admin/remoteusers/listrm_users.html',
                           remoteusers=remoteusers, title='Remoteusers')

@admin.route('/remoteusers/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_remoteuser(id):
    """
    Assign a role to a remoteuser
    """
    check_admin()

    remoteuser = RemoteUser.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if remoteuser.is_admin:
        abort(403)

    form = RemoteUserAssignForm(obj=remoteuser)
    if form.validate_on_submit():
        remoteuser.role = form.role.data
        db.session.add(remoteuser)
        db.session.commit()
        flash('You have successfully assigned a remoteuser and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_remoteusers'))

    return render_template('admin/remoteusers/addeditrm_users.html',
                           remoteuser=remoteuser, form=form,
                           title='Assign A RemoteUser')

@admin.route('/events/sendemail/', methods=['GET', 'POST'])
@login_required
def pmsend_email():
    """
    Send Email
    """

    pmsend_email = True

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
        # return redirect(url_for('admin.eventdashboard'))
        return redirect(url_for('admin.list_tasks'))

    form.scssendemail.data = event.emailsent
    form.emailrecepient.data = event.emailrecepient

    return render_template('admin/events/addeditevent.html', action="Edit",
                           pmsend_email=pmsend_email, form=form,
                           event=event, title="Edit Event")

# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import RemoteUser

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        remotuser = RemoteUser(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add user to the database
        db.session.add(remotuser)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        remotuser = RemoteUser.query.filter_by(email=form.email.data).first()
        if remotuser is not None and remotuser.verify_password(
                form.password.data):
            # log employee in
            login_user(remotuser)

            # redirect to the appropriate dashboard page after login
            if remotuser.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            elif remotuser.is_scsadmin:
                return redirect(url_for('home.scsadmin_dashboard'))
            elif remotuser.is_hradmin:
                return redirect(url_for('home.hradmin_dashboard'))
            elif remotuser.is_fmadmin:
                return redirect(url_for('home.fmadmin_dashboard'))
            elif remotuser.is_fmadmin:
                return redirect(url_for('home.eventdashboard'))
            elif remotuser.is_music_sbtadmin:
                return redirect(url_for('home.sbtadmin_dashboard'))
            else:
                return redirect(url_for('home.eventdashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

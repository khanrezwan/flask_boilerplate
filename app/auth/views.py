# Library Imports
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, login_required, current_user


# App specific imports

from . import auth
from .forms import *
from .. import db
from ..models import User
from ..decorators import requires_roles


################
# login prompt #
################
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # restrict view to already logged in users
    if current_user.is_authenticated():
        return redirect('/')
    # form object to pass into render template
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rememberme.data)
            # session['username'] = user.username
            # session['logged_in'] = True
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


##########
# logout #
##########
@auth.route('/logout')
@login_required
def logout():
    # logout user and destroy session
    logout_user()
    # for session_variables in session:
    #     session.pop(session_variables, None)
    # session.pop('username', None)
    # # session.pop('password', None)
    # session.pop('logged_in', None)
    flash('Logged Out', 'success')
    return redirect('/')


##########
# Register #
##########
@auth.route('/register', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def registeruser():
    # if current_user.is_authenticated():
    #     flash('You are already logged in. <a href=\"%s\">Logout?</a>' % url_for('auth.logout'))
    #     return redirect('/')
    form = RegisterUser()
    form.choices = [("none", "----------")]

    if Role.query.count() == 0:
        flash('Please Add Roles before you register')
        return redirect(url_for('auth.addrole'))
    else:
        roles = Role.query.all()
        form.role.query = roles

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data
        user = User(username, email, password, role)

        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully', 'success')
        # session['logged_in'] = True
        # session['username'] = User.username
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


#########
# Change password #
##########
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
    pass


##########
# Add Roles #
##########
@auth.route('/addRole', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def addrole():
    form = AddRoles()
    if request.method == 'POST' and form.validate_on_submit():
        name = str(form.name.data).lower()
        role = Role(name)

        if Role.query.filter(Role.name == role.name).count() == 0:
            db.session.add(role)
            db.session.commit()
            flash('Added %s role' % role.name)
        else:
            flash('Role is already in database')
            return render_template('auth/addrole.html', form=form)

    return render_template('auth/addrole.html', form=form)

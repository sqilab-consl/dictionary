# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, hash_pass



# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # Locate user
        user = Users.objects(username=login_form.username.data).first()
        # if user is not None:
        #     pwhash=hash_pass(password)
        #     print(pwhash)
        #     user.password=pwhash
        #     user.save()
        # Check the password
        if user and verify_pass(login_form.password.data, user.password):
            print("Authenticated!!")
            if login_form.remember.data is not None:
                login_user(user, bool(login_form.remember.data))
            else:
                login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               segment = 'login',   
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               segment = 'login',  
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email_address']

        # Check usename exists
        user = Users.objects(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   segment = 'register', 
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.objects(email_address=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   segment = 'register',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        data=request.form.to_dict(flat=True)
        del data['register']
        del data['csrf_token']
        data['is_active']=True
        data['password']=hash_pass(request.form['password'])
        user = Users(**data)
        user.save()
        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               segment = 'register',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

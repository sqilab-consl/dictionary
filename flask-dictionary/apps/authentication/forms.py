# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    remember=BooleanField('remember',id='remember_me',default="unchecked")
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                         id='username_create',
                         validators=[DataRequired()])
    last_name = StringField('Last Name',
                         id='username_create',
                         validators=[DataRequired()])
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email_address = StringField('Email Address',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

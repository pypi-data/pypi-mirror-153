#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom developer login form for Hawat.
"""


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
import flask
import flask_wtf
from flask_babel import lazy_gettext

import vial.forms
import vial.db
from vial.forms import check_login, check_unique_login, get_available_groups
from vial.blueprints.users.forms import BaseUserAccountForm


class LoginForm(flask_wtf.FlaskForm):
    """
    Class representing developer authentication login form. This form provides
    list of all currently existing user accounts in simple selectbox, so that
    the developer can quickly login as different user.
    """
    login  = wtforms.SelectField(
        lazy_gettext('User account:'),
        validators = [
            wtforms.validators.DataRequired(),
            check_login
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Login')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_choices()

    def set_choices(self):
        """
        Load list of all user accounts and populate the ``choices`` attribute of
        the ``login`` selectbox.
        """
        dbsess = vial.db.db_get().session
        user_model = flask.current_app.get_model(vial.const.MODEL_USER)
        users = dbsess.query(user_model).order_by(user_model.login).all()

        choices = []
        for usr in users:
            choices.append((usr.login, "{} ({}, #{})".format(usr.fullname, usr.login, usr.id)))
        choices = sorted(choices, key=lambda x: x[1])
        self.login.choices = choices


class RegisterUserAccountForm(BaseUserAccountForm):
    """
    Class representing user account registration form.
    """
    login = wtforms.StringField(
        lazy_gettext('Login:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50),
            check_login,
            check_unique_login
        ]
    )
    memberships_wanted = QuerySelectMultipleField(
        lazy_gettext('Requested group memberships:'),
        query_factory = get_available_groups
    )
    justification = wtforms.TextAreaField(
        lazy_gettext('Justification:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 10, max = 500)
        ]
    )

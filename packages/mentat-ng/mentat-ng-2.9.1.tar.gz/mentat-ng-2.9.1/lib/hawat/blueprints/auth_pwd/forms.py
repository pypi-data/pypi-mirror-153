#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of MyDojo package (https://github.com/honzamach/mydojo).
#
# Copyright (C) since 2018 Honza Mach <honza.mach.ml@gmail.com>
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom developer login form for Hawat.
"""


__author__ = "Honza Mach <honza.mach.ml@gmail.com>"


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from flask_babel import lazy_gettext

from vial.forms import check_login, check_unique_login, get_available_groups
from hawat.blueprints.users.forms import BaseUserAccountForm


class RegisterUserAccountForm(BaseUserAccountForm):
    """
    Class representing classical account registration form.
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
    password = wtforms.PasswordField(
        lazy_gettext('Password:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 8),
        ]
    )
    password2 = wtforms.PasswordField(
        lazy_gettext('Repeat Password:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password'),
        ]
    )

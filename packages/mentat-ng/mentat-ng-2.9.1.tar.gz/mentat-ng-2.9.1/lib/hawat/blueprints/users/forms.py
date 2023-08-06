#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom user account management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import pytz
import sqlalchemy
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from flask_babel import gettext, lazy_gettext

import vial.db
import vial.forms
from mentat.datatype.sqldb import UserModel, GroupModel


def check_id_existence(form, field):
    """
    Callback for validating user logins during account create action.
    """
    try:
        vial.db.db_get().session.query(UserModel).\
            filter(UserModel.login == field.data).\
            one()
    except sqlalchemy.orm.exc.NoResultFound:
        return
    except:  # pylint: disable=locally-disabled,bare-except
        pass
    raise wtforms.validators.ValidationError(gettext('User account with this login already exists.'))


def check_id_uniqueness(form, field):
    """
    Callback for validating user logins during account update action.
    """
    user = vial.db.db_get().session.query(UserModel).\
        filter(UserModel.login == field.data).\
        filter(UserModel.id != form.db_item_id).\
        all()
    if not user:
        return
    raise wtforms.validators.ValidationError(gettext('User account with this login already exists.'))


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return vial.db.db_query(GroupModel).order_by(GroupModel.name).all()


class BaseUserAccountForm(vial.forms.BaseItemForm):
    """
    Class representing base user account form.
    """
    fullname = wtforms.StringField(
        lazy_gettext('Full name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 100)
        ]
    )
    email = wtforms.StringField(
        lazy_gettext('Email:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 250),
            wtforms.validators.Email()
        ]
    )
    organization = wtforms.StringField(
        lazy_gettext('Home organization:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 250)
        ]
    )
    locale = vial.forms.SelectFieldWithNone(
        lazy_gettext('Prefered locale:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [('', lazy_gettext('<< no preference >>'))],
        filters = [lambda x: x or None],
        default = ''
    )
    timezone = vial.forms.SelectFieldWithNone(
        lazy_gettext('Prefered timezone:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('<< no preference >>'))] + list(zip(pytz.common_timezones, pytz.common_timezones)),
        filters = [lambda x: x or None],
        default = ''
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # Handle additional custom keywords.
        #

        # The list of choices for 'locale' attribute comes from outside of the
        # form to provide as loose tie as possible to the outer application.
        # Another approach would be to load available choices here with:
        #
        #   locales = list(flask.current_app.config['SUPPORTED_LOCALES'].items())
        #
        # That would mean direct dependency on flask.Flask application.
        self.locale.choices[1:] = kwargs['choices_locales']


class AdminUserAccountForm(BaseUserAccountForm):
    """
    Class representing base user account form for admins.
    """
    enabled = wtforms.RadioField(
        lazy_gettext('State:'),
        validators = [
            wtforms.validators.InputRequired(),
        ],
        choices = [
            (True,  lazy_gettext('Enabled')),
            (False, lazy_gettext('Disabled'))
        ],
        filters = [vial.forms.str_to_bool],
        coerce = vial.forms.str_to_bool
    )
    roles = wtforms.SelectMultipleField(
        lazy_gettext('Roles:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
    memberships = QuerySelectMultipleField(
        lazy_gettext('Group memberships:'),
        query_factory = get_available_groups
    )
    managements = QuerySelectMultipleField(
        lazy_gettext('Group managements:'),
        query_factory = get_available_groups
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        # Handle additional custom keywords.
        #

        # The list of choices for 'roles' attribute comes from outside of the
        # form to provide as loose tie as possible to the outer application.
        # Another approach would be to load available choices here with:
        #
        #   roles = flask.current_app.config['ROLES']
        #
        # That would mean direct dependency on flask.Flask application.
        self.roles.choices = kwargs['choices_roles']


class CreateUserAccountForm(AdminUserAccountForm):
    """
    Class representing user account create form.
    """
    login = wtforms.StringField(
        lazy_gettext('Login:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50),
            vial.forms.check_login,
            check_id_existence
        ]
    )


class UpdateUserAccountForm(BaseUserAccountForm):
    """
    Class representing user account update form for regular users.
    """


class AdminUpdateUserAccountForm(AdminUserAccountForm):
    """
    Class representing user account update form for administrators.
    """
    login = wtforms.StringField(
        lazy_gettext('Login:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50),
            vial.forms.check_login,
            check_id_uniqueness
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # Handle additional custom keywords.
        #

        # Store the ID of original item in database to enable the ID uniqueness
        # check with check_id_uniqueness() validator.
        self.db_item_id = kwargs['db_item_id']

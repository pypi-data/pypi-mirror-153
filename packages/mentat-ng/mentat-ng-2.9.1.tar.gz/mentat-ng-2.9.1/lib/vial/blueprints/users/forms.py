#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom user account management forms for Hawat.
"""


import pytz
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_babel import lazy_gettext

import vial.db
import vial.const
import vial.forms
from vial.forms import check_login, check_unique_login, get_available_groups


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
            check_login,
            check_unique_login
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
            check_unique_login
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


class UserSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing simple user search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Login, name, email:'),
        validators = [
            wtforms.validators.Optional(),
            wtforms.validators.Length(min = 3, max = 100)
        ],
        description = lazy_gettext('User`s login, full name or email address. Search is performed even in the middle of the strings, so for example you may lookup by domain.')
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Creation time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Lower time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Creation time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Upper time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )

    state = wtforms.SelectField(
        lazy_gettext('State:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('', lazy_gettext('Nothing selected')),
            ('enabled',  lazy_gettext('Enabled')),
            ('disabled', lazy_gettext('Disabled'))
        ],
        default = '',
        description = lazy_gettext('Search for users with particular account state.')
    )
    role = wtforms.SelectField(
        lazy_gettext('Role:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = '',
        description = lazy_gettext('Search for users with particular role, or without any assigned roles.')
    )
    membership = QuerySelectField(
        lazy_gettext('Group membership:'),
        query_factory = get_available_groups,
        allow_blank = True,
        description = lazy_gettext('Search for users with membership with particular group.')
    )
    management = QuerySelectField(
        lazy_gettext('Group management:'),
        query_factory = get_available_groups,
        allow_blank = True,
        description = lazy_gettext('Search for users with management rights to particular group.')
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort result by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('createtime.desc', lazy_gettext('by creation time descending')),
            ('createtime.asc',  lazy_gettext('by creation time ascending')),
            ('login.desc', lazy_gettext('by login descending')),
            ('login.asc',  lazy_gettext('by login ascending')),
            ('fullname.desc', lazy_gettext('by name descending')),
            ('fullname.asc',  lazy_gettext('by name ascending')),
            ('email.desc', lazy_gettext('by email descending')),
            ('email.asc',  lazy_gettext('by email ascending')),
            ('logintime.desc', lazy_gettext('by login time descending')),
            ('logintime.asc',  lazy_gettext('by login time ascending')),
        ],
        default = 'fullname.asc'
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
        self.role.choices = [
            ('', lazy_gettext('Nothing selected')),
            (vial.const.NO_ROLE, lazy_gettext('Without any roles'))
        ] + kwargs['choices_roles']

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False

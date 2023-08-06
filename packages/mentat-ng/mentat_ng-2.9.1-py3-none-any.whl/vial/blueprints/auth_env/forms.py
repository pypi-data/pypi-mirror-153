#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom user account registration form for Hawat.
"""


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from flask_babel import lazy_gettext

from vial.forms import get_available_groups

from vial.blueprints.users.forms import BaseUserAccountForm


class RegisterUserAccountForm(BaseUserAccountForm):
    """
    Class representing user account registration form.
    """
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

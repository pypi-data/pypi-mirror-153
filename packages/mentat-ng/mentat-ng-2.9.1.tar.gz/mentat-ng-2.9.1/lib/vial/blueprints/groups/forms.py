#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom group management forms for Hawat.
"""


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_babel import gettext, lazy_gettext

import vial.db
import vial.forms
from vial.forms import get_available_users, get_available_group_sources

def check_parent_not_self(form, field):
    """
    Callback for validating that parent group is not self.
    """
    if field.data and form.db_item_id == field.data.id:
        raise wtforms.validators.ValidationError(gettext('You must not select a group as its own parent! Naughty, naughty you!'))


def format_select_option_label_user(item):
    """
    Format option for selection of user accounts.
    """
    return "{} ({})".format(item.fullname, item.login)


class BaseGroupForm(vial.forms.BaseItemForm):
    """
    Class representing base group form.
    """
    description = wtforms.StringField(
        lazy_gettext('Description:'),
        validators = [
            wtforms.validators.DataRequired()
        ],
        description = lazy_gettext('Additional and more extensive group description.')
    )
    source = wtforms.HiddenField(
        default = 'manual',
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50)
        ],
        description = lazy_gettext('Origin of the group record, whether it was added manually, or via some automated mechanism from data from some third party system.')
    )
    members = QuerySelectMultipleField(
        lazy_gettext('Members:'),
        query_factory = vial.forms.get_available_users,
        get_label = format_select_option_label_user,
        blank_text = lazy_gettext('<< no selection >>'),
        description = lazy_gettext('List of group members.')
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )


class UpdateGroupForm(BaseGroupForm):
    """
    Class representing group update form for regular users.
    """


class AdminBaseGroupForm(BaseGroupForm):
    """
    Class representing group create form.
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
        coerce = vial.forms.str_to_bool,
        description = lazy_gettext('Boolean flag whether the group is enabled or disabled. Disabled groups are hidden to the most of the system features.')
    )
    managers = QuerySelectMultipleField(
        lazy_gettext('Managers:'),
        query_factory = vial.forms.get_available_users,
        get_label = format_select_option_label_user,
        blank_text = lazy_gettext('<< no selection >>'),
        description = lazy_gettext('List of users acting as group managers. These users may change various group settings.')
    )
    parent = QuerySelectField(
        lazy_gettext('Parent group:'),
        validators = [
            wtforms.validators.Optional(),
            check_parent_not_self
        ],
        query_factory = vial.forms.get_available_groups,
        allow_blank = True,
        blank_text = lazy_gettext('<< no selection >>'),
        description = lazy_gettext('Parent group for this group. This feature enables the posibility to create structured group hierarchy.')
    )


class AdminCreateGroupForm(AdminBaseGroupForm):
    """
    Class representing group create form for administrators.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 100),
            vial.forms.check_unique_group
        ],
        description = lazy_gettext('System-wide unique name for the group.')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_item_id = None


class AdminUpdateGroupForm(AdminBaseGroupForm):
    """
    Class representing group update form for administrators.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 100),
            vial.forms.check_unique_group
        ],
        description = lazy_gettext('System-wide unique name for the group.')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Store the ID of original item in database to enable the ID uniqueness
        # check with check_name_uniqueness() validator.
        self.db_item_id = kwargs['db_item_id']


class GroupSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing simple user search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Name, description:'),
        validators = [
            wtforms.validators.Optional(),
            wtforms.validators.Length(min = 3, max = 100)
        ],
        description = lazy_gettext('Group`s full name or description. Search is performed even in the middle of the strings.')
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
        description = lazy_gettext('Search for groups with particular state.')
    )
    source = wtforms.SelectField(
        lazy_gettext('Record source:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = '',
        description = lazy_gettext('Search for groups coming from particular sources/feeds.')
    )
    members = QuerySelectField(
        lazy_gettext('Group members:'),
        query_factory = get_available_users,
        allow_blank = True,
        description = lazy_gettext('Search for groups with particular members.')
    )
    managers = QuerySelectField(
        lazy_gettext('Group managers:'),
        query_factory = get_available_users,
        allow_blank = True,
        description = lazy_gettext('Search for groups with particular managers.')
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('createtime.desc', lazy_gettext('by creation time descending')),
            ('createtime.asc',  lazy_gettext('by creation time ascending')),
            ('name.desc', lazy_gettext('by name descending')),
            ('name.asc',  lazy_gettext('by name ascending'))
        ],
        default = 'name.asc'
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
        source_list = get_available_group_sources()
        self.source.choices = [('', lazy_gettext('Nothing selected'))] + list(zip(source_list, source_list))

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom group management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sqlalchemy
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

#
# Flask related modules.
#
from flask_babel import gettext, lazy_gettext

#
# Custom modules.
#
import vial.db
import vial.forms
from mentat.datatype.sqldb import GroupModel, UserModel


def check_name_existence(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating user logins during account create action.
    """
    try:
        vial.db.db_get().session.query(GroupModel).\
            filter(GroupModel.name == field.data).\
            one()
    except sqlalchemy.orm.exc.NoResultFound:
        return
    except:  # pylint: disable=locally-disabled,bare-except
        pass
    raise wtforms.validators.ValidationError(gettext('Group with this name already exists.'))


def check_name_uniqueness(form, field):
    """
    Callback for validating user logins during account update action.
    """
    item = vial.db.db_get().session.query(GroupModel).\
        filter(GroupModel.name == field.data).\
        filter(GroupModel.id != form.db_item_id).\
        all()
    if not item:
        return
    raise wtforms.validators.ValidationError(gettext('Group with this name already exists.'))


def check_parent_not_self(form, field):
    """
    Callback for validating that parent group is not self.
    """
    if field.data and form.db_item_id == field.data.id:
        raise wtforms.validators.ValidationError(gettext('You must not select a group as its own parent! Naughty, naughty you!'))


def get_available_users():
    """
    Query the database for list of all available user accounts.
    """
    return vial.db.db_query(UserModel).order_by(UserModel.fullname).all()


def format_select_option_label_user(item):
    """
    Format option for selection of user accounts.
    """
    return "{} ({})".format(item.fullname, item.login)


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return vial.db.db_query(GroupModel).order_by(GroupModel.name).all()


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
        query_factory = get_available_users,
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
        query_factory = get_available_users,
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
        query_factory = get_available_groups,
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
            check_name_existence
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
            check_name_uniqueness
        ],
        description = lazy_gettext('System-wide unique name for the group.')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Store the ID of original item in database to enable the ID uniqueness
        # check with check_name_uniqueness() validator.
        self.db_item_id = kwargs['db_item_id']

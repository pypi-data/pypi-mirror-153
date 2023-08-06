#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom event report search form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

import flask_login
import flask_wtf
from flask_babel import lazy_gettext

import mentat.const
from mentat.datatype.sqldb import UserModel, GroupModel
import vial.const
import vial.forms
import vial.db
import hawat.const


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    # In case current user is administrator provide list of all groups.
    if flask_login.current_user.has_role(vial.const.ROLE_ADMIN):
        return vial.db.db_query(GroupModel).\
            order_by(GroupModel.name).\
            all()
    # Otherwise provide only list of groups current user is member of.
    return vial.db.db_query(GroupModel).\
        filter(GroupModel.members.any(UserModel.id == flask_login.current_user.id)).\
        order_by(GroupModel.name).\
        all()

def get_severity_choices():
    """
    Return select choices for report severities.
    """
    return list(
        zip(
            mentat.const.REPORT_SEVERITIES,
            [lazy_gettext(x) for x in mentat.const.REPORT_SEVERITIES]
        )
    )

def get_type_choices():
    """
    Return select choices for report severities.
    """
    return list(
        zip(
            mentat.const.REPORT_TYPES,
            [lazy_gettext(x) for x in mentat.const.REPORT_TYPES]
        )
    )

class EventReportSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing event report search form.
    """
    label = wtforms.StringField(
        lazy_gettext('Label:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
    groups = QuerySelectMultipleField(
        lazy_gettext('Groups:'),
        query_factory = get_available_groups,
        allow_blank = False,
        get_pk = lambda item: item.name
    )
    severities = wtforms.SelectMultipleField(
        lazy_gettext('Severities:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = get_severity_choices(),
        filters = [lambda x: x or []]
    )
    types = wtforms.SelectMultipleField(
        lazy_gettext('Types:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = get_type_choices(),
        filters = [lambda x: x or []]
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = lambda: vial.forms.default_dt_with_delta(hawat.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = vial.forms.default_dt
    )

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        if field_name in ('groups', 'severities', 'types'):
            return True
        return False


class ReportingDashboardForm(flask_wtf.FlaskForm):
    """
    Class representing event reporting dashboard search form.
    """
    groups = QuerySelectMultipleField(
        lazy_gettext('Groups:'),
        query_factory = get_available_groups,
        allow_blank = False,
        get_pk = lambda item: item.name
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = lambda: vial.forms.default_dt_with_delta(vial.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = vial.forms.default_dt
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        if field_name in ('groups',):
            return True
        return False


class FeedbackForm(flask_wtf.FlaskForm):
    """
    Class representing feedback form for reports.
    """
    ip = wtforms.HiddenField(
        validators=[
            wtforms.validators.DataRequired(),
            vial.forms.check_network_record
        ]
    )
    text = wtforms.TextAreaField(
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=3)
        ]
    )
    section = wtforms.HiddenField(
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=1)
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Send feedback')
    )

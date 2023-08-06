#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom reporting settings management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import pytz
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from babel import Locale

from flask_babel import lazy_gettext

import vial.const
import vial.forms
import vial.db

import mentat.const
from mentat.datatype.sqldb import GroupModel


REPORT_TRANSLATIONS = '/etc/mentat/templates/reporter/translations'


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return vial.db.db_query(GroupModel).order_by(GroupModel.name).all()


def get_available_locales():
    """
    Get list available report translations.
    """
    locale_list = [['en', 'en']]

    if os.path.isdir(REPORT_TRANSLATIONS):
        for translation in os.listdir(REPORT_TRANSLATIONS):
            if translation[0] == '.':
                continue
            if os.path.isdir(os.path.join(REPORT_TRANSLATIONS, translation)):
                locale_list.append([translation, translation])

    locale_list = sorted(locale_list, key = lambda x: x[0])

    for translation in locale_list:
        locale_obj = Locale.parse(translation[0])
        translation[1] = locale_obj.language_name.lower()

    return locale_list


class BaseSettingsReportingForm(vial.forms.BaseItemForm):
    """
    Class representing base reporting settings form.
    """
    mode = wtforms.SelectField(
        lazy_gettext('Reporting mode:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('',                                  lazy_gettext('<< system default >>')),
            (mentat.const.REPORTING_MODE_SUMMARY, lazy_gettext('summary')),
            (mentat.const.REPORTING_MODE_EXTRA,   lazy_gettext('extra')),
            (mentat.const.REPORTING_MODE_BOTH,    lazy_gettext('both')),
            (mentat.const.REPORTING_MODE_NONE,    lazy_gettext('none'))
        ],
        filters = [lambda x: x or None]
    )
    emails_low = vial.forms.CommaListField(
        lazy_gettext('Target emails - low severity:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_email_list
        ]
    )
    emails_medium = vial.forms.CommaListField(
        lazy_gettext('Target emails - medium severity:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_email_list
        ]
    )
    emails_high = vial.forms.CommaListField(
        lazy_gettext('Target emails - high severity:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_email_list
        ]
    )
    emails_critical = vial.forms.CommaListField(
        lazy_gettext('Target emails - critical severity:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_email_list
        ]
    )
    redirect = vial.forms.RadioFieldWithNone(
        lazy_gettext('Report redirection:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            (None,  lazy_gettext('System default')),
            (True,  lazy_gettext('Enabled')),
            (False, lazy_gettext('Disabled'))
        ],
        filters = [vial.forms.str_to_bool_with_none],
        coerce = vial.forms.str_to_bool_with_none
    )
    locale = wtforms.SelectField(
        lazy_gettext('Locale:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('<< system default >>'))] + get_available_locales(),
        filters = [lambda x: x or None]
    )
    timezone = wtforms.SelectField(
        lazy_gettext('Timezone:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('<< system default >>'))] + list(zip(pytz.common_timezones, pytz.common_timezones)),
        filters = [lambda x: x or None]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )

class CreateSettingsReportingForm(BaseSettingsReportingForm):
    """
    Class representing reporting settings create form.
    """
    group = QuerySelectField(
        lazy_gettext('Group:'),
        query_factory = get_available_groups,
        allow_blank = False
    )

class UpdateSettingsReportingForm(BaseSettingsReportingForm):
    """
    Class representing reporting settings update form.
    """

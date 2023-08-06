#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom host search form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms

import flask_wtf
from flask_babel import lazy_gettext

import vial.const
import vial.forms
import hawat.const


class SimpleHostSearchForm(flask_wtf.FlaskForm):
    """
    Class representing simple event timeline search form.
    """
    host_addr = wtforms.StringField(
        lazy_gettext('Host address:'),
        validators = [
            wtforms.validators.DataRequired(),
            vial.forms.check_ip_record
        ]
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Detection time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = lambda: vial.forms.default_dt_with_delta(hawat.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Detection time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = vial.forms.default_dt
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom internal whois resolving search form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import ipranges
import wtforms
import flask_wtf
from flask_babel import gettext, lazy_gettext

import vial.const


def check_search_data(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating whois search form data. Field value must be email
    address or IPv4/IPv6 address/range/network.
    """
    try:
        ipranges.from_str(field.data)
        return
    except ValueError:
        pass

    if vial.const.CRE_EMAIL.match(field.data):
        return

    raise wtforms.validators.ValidationError(
        gettext('Search argument must be email or IP address/range/network.')
    )


class WhoisSearchForm(flask_wtf.FlaskForm):
    """
    Class representing whois resolving search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Search local WHOIS:'),
        validators = [
            wtforms.validators.DataRequired(),
            check_search_data
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

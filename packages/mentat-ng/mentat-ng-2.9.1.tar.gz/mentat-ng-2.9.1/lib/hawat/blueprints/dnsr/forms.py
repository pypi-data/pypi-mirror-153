#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom DNS service search form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms
import flask_wtf
from flask_babel import lazy_gettext


class DnsrSearchForm(flask_wtf.FlaskForm):
    """
    Class representing DNS service search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Search DNS:'),
        validators = [
            wtforms.validators.DataRequired()
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

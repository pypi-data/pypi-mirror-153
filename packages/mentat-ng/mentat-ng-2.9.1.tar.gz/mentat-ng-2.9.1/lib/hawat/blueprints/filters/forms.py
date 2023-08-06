#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom reporting filter management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import pynspect.gparser

import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#
# Flask related modules.
#
import flask_wtf
from flask_babel import gettext, lazy_gettext

#
# Custom modules.
#
import vial.db
import vial.forms
from mentat.datatype.sqldb import GroupModel
from mentat.const import REPORTING_FILTER_BASIC, REPORTING_FILTER_ADVANCED
from mentat.idea.internal import Idea, IDEAFilterCompiler


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return vial.db.db_query(GroupModel).order_by(GroupModel.name).all()


def check_filter(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating Pynspect filter.
    """
    psr = pynspect.gparser.PynspectFilterParser()
    psr.build()
    compiler = IDEAFilterCompiler()
    try:
        rule = psr.parse(field.data)
        compiler.compile(rule)
    except Exception as err:
        raise wtforms.validators.ValidationError(
            gettext(
                'Filtering rule parse error: "%(error)s".',
                error = str(err)
            )
        )

def check_event(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating IDEA event JSON.
    """
    try:
        Idea.from_json(field.data)
    except Exception as err:
        raise wtforms.validators.ValidationError(
            gettext(
                'Event JSON parse error: "%(error)s".',
                error = str(err)
            )
        )


#-------------------------------------------------------------------------------


class BaseFilterForm(vial.forms.BaseItemForm):
    """
    Class representing base reporting filter form.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 250)
        ]
    )
    type = wtforms.SelectField(
        lazy_gettext('Type:'),
        validators = [
            wtforms.validators.DataRequired(),
        ],
        choices = [
            (REPORTING_FILTER_BASIC,    lazy_gettext('Basic')),
            (REPORTING_FILTER_ADVANCED, lazy_gettext('Advanced'))
        ]
    )
    description = wtforms.TextAreaField(
        lazy_gettext('Description:'),
        validators = [
            wtforms.validators.DataRequired(),
        ]
    )
    filter = wtforms.TextAreaField(
        lazy_gettext('Filter:'),
        validators = [
            wtforms.validators.Optional(),
            check_filter
        ]
    )
    detectors = wtforms.SelectMultipleField(
        lazy_gettext('Detectors:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('<< no preference >>'))],
        filters = [lambda x: x or []]
    )
    categories = wtforms.SelectMultipleField(
        lazy_gettext('Categories:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('<< no preference >>'))],
        filters = [lambda x: x or []]
    )
    ips = vial.forms.CommaListField(
        lazy_gettext('Source IPs:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea()
    )
    valid_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Valid from:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
    valid_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Valid to:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
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
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    preview = wtforms.SubmitField(
        lazy_gettext('Preview')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.detectors.choices[1:]  = kwargs['choices_detectors']
        self.categories.choices[1:] = kwargs['choices_categories']


class AdminFilterForm(BaseFilterForm):
    """
    Class representing reporting filter create form.
    """
    group = QuerySelectField(
        lazy_gettext('Group:'),
        query_factory = get_available_groups,
        allow_blank = False
    )

class PlaygroundFilterForm(flask_wtf.FlaskForm):
    """
    Class representing IP geolocation search form.
    """
    filter = wtforms.TextAreaField(
        lazy_gettext('Filtering rule:'),
        validators = [
            wtforms.validators.DataRequired(),
            check_filter
        ]
    )
    event = wtforms.TextAreaField(
        lazy_gettext('IDEA event:'),
        validators = [
            wtforms.validators.DataRequired(),
            check_event
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Check')
    )

class FilterSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing simple user search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Netname, network, description:'),
        validators = [
            wtforms.validators.Optional(),
            wtforms.validators.Length(min = 3, max = 100)
        ],
        description = lazy_gettext('Filter`s name, content or description. Search is performed even in the middle of the strings.')
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

    type = wtforms.SelectField(
        lazy_gettext('Type:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('', lazy_gettext('Nothing selected')),
            (REPORTING_FILTER_BASIC,    lazy_gettext('Basic')),
            (REPORTING_FILTER_ADVANCED, lazy_gettext('Advanced'))
        ],
        default = '',
        description = lazy_gettext('Search for filters of particular type.')
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
        description = lazy_gettext('Search for filters with particular state.')
    )
    group = QuerySelectField(
        lazy_gettext('Group:'),
        query_factory = get_available_groups,
        allow_blank = True,
        description = lazy_gettext('Search for filters belonging to particular group.')
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('createtime.desc', lazy_gettext('by creation time descending')),
            ('createtime.asc',  lazy_gettext('by creation time ascending')),
            ('name.desc', lazy_gettext('by netname descending')),
            ('name.asc',  lazy_gettext('by netname ascending')),
            ('hits.desc', lazy_gettext('by number of hits descending')),
            ('hits.asc',  lazy_gettext('by number of hits ascending')),
            ('last_hit.desc', lazy_gettext('by time of last hit descending')),
            ('last_hit.asc',  lazy_gettext('by time of last hit ascending'))
        ],
        default = 'name.asc'
    )

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False

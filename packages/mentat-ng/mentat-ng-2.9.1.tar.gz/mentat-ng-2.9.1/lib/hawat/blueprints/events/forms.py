#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains various `IDEA <https://idea.cesnet.cz/en/index>`__ event
database search forms for Hawat application.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

import flask_wtf
from flask_babel import lazy_gettext

from mentat.datatype.sqldb import GroupModel
import vial.const
import vial.forms
import vial.db
import hawat.const


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return vial.db.db_query(GroupModel).order_by(GroupModel.name).all()


class SimpleEventSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing simple event search form.
    """
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Detection time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Lower time boundary for event detection time as provided by event detector. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event detectors are usually outside of the control of Mentat system administrators and may sometimes emit events with invalid detection times, for example timestamps in the future.'),
        default = lambda: vial.forms.default_dt_with_delta(hawat.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Detection time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Upper time boundary for event detection time as provided by event detector. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event detectors are usually outside of the control of Mentat system administrators and may sometimes emit events with invalid detection times, for example timestamps in the future.'),
        default = vial.forms.default_dt
    )
    st_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Storage time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Lower time boundary for event storage time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event storage time is provided by Mentat system itself. It is a timestamp of the exact moment the event was stored into the database.')
    )
    st_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Storage time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Upper time boundary for event storage time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event storage time is provided by Mentat system itself. It is a timestamp of the exact moment the event was stored into the database.')
    )
    source_addrs = vial.forms.CommaListField(
        lazy_gettext('Source addresses:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea(),
        description = lazy_gettext('Comma separated list of event source IP4/6 addresses, ranges or networks. In this context a source does not necessarily mean a source of the connection, but rather a source of the problem as reported by a detector. Any additional whitespace is ignored and may be used for better readability.')
    )
    target_addrs = vial.forms.CommaListField(
        lazy_gettext('Target addresses:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea(),
        description = lazy_gettext('Comma separated list of event target IP4/6 addresses, ranges or networks. In this context a target does not necessarily mean a target of the connection, but rather a victim of the problem as reported by a detector. Any additional whitespace is ignored and may be used for better readability.')
    )
    host_addrs = vial.forms.CommaListField(
        lazy_gettext('Host addresses:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea(),
        description = lazy_gettext('Comma separated list of event source or target IP4/6 addresses, ranges or networks. Any additional whitespace is ignored and may be used for better readability.')
    )
    source_ports = vial.forms.CommaListField(
        lazy_gettext('Source ports:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_port_list
        ],
        description = lazy_gettext('Comma separated list of source ports as integers. In this context a source does not necessarily mean a source of the connection, but rather a source of the problem as reported by a detector. Any additional whitespace is ignored and may be used for better readability.')
    )
    target_ports = vial.forms.CommaListField(
        lazy_gettext('Target ports:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_port_list
        ],
        description = lazy_gettext('Comma separated list of target ports as integers. In this context a target does not necessarily mean a target of the connection, but rather a victim of the problem as reported by a detector. Any additional whitespace is ignored and may be used for better readability.')
    )
    host_ports = vial.forms.CommaListField(
        lazy_gettext('Host ports:'),
        validators = [
            wtforms.validators.Optional(),
            vial.forms.check_port_list
        ],
        description = lazy_gettext('Comma separated list of source or target ports as integers. Any additional whitespace is ignored and may be used for better readability.')
    )
    source_types = wtforms.SelectMultipleField(
        lazy_gettext('Source types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event source type. Each event source may be optionally assigned one or more labels to better categorize type of a source.')
    )
    target_types = wtforms.SelectMultipleField(
        lazy_gettext('Target types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event target type. Each event target may be optionally assigned one or more labels to better categorize type of a target.')
    )
    host_types = wtforms.SelectMultipleField(
        lazy_gettext('Host types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event source or target type. Each event source or target may be optionally assigned one or more labels to better categorize type of a source or target.')
    )
    detectors = wtforms.SelectMultipleField(
        lazy_gettext('Detectors:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Name of the detector that detected the event.')
    )
    not_detectors = wtforms.BooleanField(
        lazy_gettext('Negate detector selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    detector_types = wtforms.SelectMultipleField(
        lazy_gettext('Detector types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event detector type. Each event detector may be optionally assigned one or more labels to better categorize that detector.')
    )
    not_detector_types = wtforms.BooleanField(
        lazy_gettext('Negate detector_type selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    categories = wtforms.SelectMultipleField(
        lazy_gettext('Categories:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event category. Each event may be optionally assigned one or more labels to better categorize that event, for example as "Recon.Scanning", "Abusive.Spam", "Test" etc.')
    )
    not_categories = wtforms.BooleanField(
        lazy_gettext('Negate category selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    severities = wtforms.SelectMultipleField(
        lazy_gettext('Severities:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event severity. Each event may be optionally assigned one severity level, which can be then use during incident handling workflows to prioritize events.')
    )
    not_severities = wtforms.BooleanField(
        lazy_gettext('Negate severity selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    classes = wtforms.SelectMultipleField(
        lazy_gettext('Classes:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of event class. Each event may be optionally assigned one class to better describe the event and group all similar events together for better processing. Event classification in internal feature of Mentat system for better event management.')
    )
    not_classess = wtforms.BooleanField(
        lazy_gettext('Negate class selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    description = wtforms.StringField(
        lazy_gettext('Description:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Specification of event description. Each event may be optionally assigned short descriptive string.')
    )
    protocols = wtforms.SelectMultipleField(
        lazy_gettext('Protocols:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of one or more communication protocols involved in the event.')
    )
    not_protocols = wtforms.BooleanField(
        lazy_gettext('Negate protocol selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    groups = QuerySelectMultipleField(
        lazy_gettext('Abuse group:'),
        query_factory = get_available_groups,
        allow_blank = False,
        get_pk = lambda item: item.name,
        description = lazy_gettext('Specification of the abuse group to whose constituency this event belongs based on one of the event source addresses.')
    )
    not_groups = wtforms.BooleanField(
        lazy_gettext('Negate group selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    inspection_errs = wtforms.SelectMultipleField(
        lazy_gettext('Inspection errors:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []],
        description = lazy_gettext('Specification of possible event errors detected during event inspection by real-time event processing inspection daemon.')
    )
    not_inspection_errs = wtforms.BooleanField(
        lazy_gettext('Negate inspection error selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('time.desc', lazy_gettext('by time descending')),
            ('time.asc',  lazy_gettext('by time ascending')),
            ('detecttime.desc', lazy_gettext('by detection time descending')),
            ('detecttime.asc',  lazy_gettext('by detection time ascending')),
            ('storagetime.desc', lazy_gettext('by storage time descending')),
            ('storagetime.asc',  lazy_gettext('by storage time ascending'))
        ],
        default = 'time.desc'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source_types.choices   = kwargs['choices_source_types']
        self.target_types.choices   = kwargs['choices_target_types']
        self.host_types.choices     = kwargs['choices_host_types']

        self.detectors.choices[2:]       = kwargs['choices_detectors']
        self.detector_types.choices[2:]  = kwargs['choices_detector_types']
        self.categories.choices[2:]      = kwargs['choices_categories']
        self.severities.choices[2:]      = kwargs['choices_severities']
        self.classes.choices[2:]         = kwargs['choices_classes']
        self.protocols.choices[2:]       = kwargs['choices_protocols']
        self.inspection_errs.choices[2:] = kwargs['choices_inspection_errs']

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        if field_name in ('source_addrs', 'target_addrs', 'host_addrs', 'source_ports', 'target_ports', 'host_ports', 'source_types', 'target_types', 'host_types', 'detectors', 'detector_types', 'categories', 'severities', 'classess', 'protocols', 'groups', 'inspection_errs'):
            return True
        return False


class EventDashboardForm(flask_wtf.FlaskForm):
    """
    Class representing event dashboard search form.
    """
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Lower time boundary for event detection time as provided by event detector. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event detectors are usually outside of the control of Mentat system administrators and may sometimes emit events with invalid detection times, for example timestamps in the future.'),
        default = lambda: vial.forms.default_dt_with_delta(hawat.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Upper time boundary for event detection time as provided by event detector. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences. Event detectors are usually outside of the control of Mentat system administrators and may sometimes emit events with invalid detection times, for example timestamps in the future.'),
        default = vial.forms.default_dt
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

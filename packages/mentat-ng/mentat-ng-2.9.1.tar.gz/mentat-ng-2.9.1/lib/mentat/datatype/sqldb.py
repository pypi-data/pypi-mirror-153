#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Datatype model library for PostgreSQL backend storages.

Overview
^^^^^^^^

The implementation is based on the great `sqlalchemy <http://www.sqlalchemy.org/>`__
library. This module provides models for following datatypes/objects:

:py:class:`mentat.datatype.sqldb.UserModel`
    Database representation of user account objects.

:py:class:`mentat.datatype.sqldb.GroupModel`
    Database representation of group objects.

:py:class:`mentat.datatype.sqldb.FilterModel`
    Database representation of group reporting filter objects.

:py:class:`mentat.datatype.sqldb.NetworkModel`
    Database representation of network record objects for internal whois.

:py:class:`mentat.datatype.sqldb.SettingsReportingModel`
    Database representation of group settings objects.

:py:class:`mentat.datatype.sqldb.EventStatisticsModel`
    Database representation of event statistics objects.

:py:class:`mentat.datatype.sqldb.EventReportModel`
    Database representation of report objects.

:py:class:`mentat.datatype.sqldb.ItemChangeLogModel`
    Database representation of object changelog.

.. warning::

    Current implementation is for optimalization purposes using some advanced
    features provided by the `PostgreSQL <https://www.postgresql.org/>`__
    database and no other engines are currently supported.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import json
import difflib
import string
import random
import datetime
import sqlalchemy
import sqlalchemy.dialects.postgresql

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from werkzeug.security import generate_password_hash, check_password_hash

from mentat.const import REPORTING_MODES, REPORTING_FILTERS, REPORTING_FILTER_BASIC,\
    REPORT_TYPES, REPORT_SEVERITIES


#
# Modify compilation of DROP TABLE for PostgreSQL databases to enable CASCADE feature.
# Otherwise it is not possible to delete the database schema with:
#   MODEL.metadata.drop_all(engine)
#
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):  # pylint: disable=locally-disabled,unused-argument
    return compiler.visit_drop_table(element) + " CASCADE"


#-------------------------------------------------------------------------------


class MODEL:
    """
    Base class for all `sqlalchemy <http://www.sqlalchemy.org/>`__ database models
    and providing the `declarative base <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base>`__.
    All required database objects should be implemented by extending this base model.
    """
    @declared_attr
    def id(self):  # pylint: disable=locally-disabled,invalid-name
        """
        Common table column for unique numeric identifier, implementation is based
        on `declared_attr <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declared_attr>`__
        pattern.
        """
        return sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    @declared_attr
    def createtime(self):
        """
        Common table column for object creation timestamps, implementation is based
        on `declared_attr <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declared_attr>`__
        pattern.
        """
        return sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)

    def get_id(self):
        """
        Getter for retrieving current ID.
        """
        return self.id

    def to_dict(self):
        """
        Export object into dictionary containing only primitive data types.
        """
        raise NotImplementedError()

    def to_json(self):
        """
        Export object into JSON string.
        """
        return json.dumps(self.to_dict(), indent = 4, sort_keys = True)


MODEL = declarative_base(cls = MODEL)


_asoc_group_members = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: group membership.

What users are members of what groups.
"""

_asoc_group_members_wanted = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members_wanted',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: wanted group membership.

What users want to be members of what groups.
"""

_asoc_group_managers = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_managers',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: group management.

What users can manage what groups.
"""

_asoc_groups_reports = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_groups_reports',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    sqlalchemy.Column('report_id', sqlalchemy.ForeignKey('reports_events.id', onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
)
"""
Association table representing group*report relation: ownership of report.

What reports are linked to what groups (n:m relationship).
"""


class UserModel(MODEL):
    """
    Class representing user objects within the SQL database mapped to ``users``
    table.
    """
    __tablename__ = 'users'

    login        = sqlalchemy.Column(sqlalchemy.String(50), unique = True, index = True)
    fullname     = sqlalchemy.Column(sqlalchemy.String(100), nullable = False)
    email        = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    organization = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    roles        = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String(20), dimensions = 1), nullable = False, default = [])
    password     = sqlalchemy.Column(sqlalchemy.String)
    apikey       = sqlalchemy.Column(sqlalchemy.String, unique = True, index = True)
    enabled      = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = True)

    locale     = sqlalchemy.Column(sqlalchemy.String(20))
    timezone   = sqlalchemy.Column(sqlalchemy.String(50))

    memberships = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_members, back_populates = 'members', order_by = 'GroupModel.name')
    memberships_wanted = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_members_wanted, back_populates = 'members_wanted', order_by = 'GroupModel.name')
    managements = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_managers, back_populates = 'managers', order_by = 'GroupModel.name')

    changelogs  = sqlalchemy.orm.relationship('ItemChangeLogModel', back_populates = 'author', order_by = 'ItemChangeLogModel.createtime')

    logintime  = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return "<User(login='%s', fullname='%s')>" % (self.login, self.fullname)

    def __str__(self):
        return '{}'.format(self.login)

    def is_state_enabled(self):
        """
        Check if current user account state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current user account state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current user account state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current user account state to disabled.
        """
        self.enabled = False

    def set_password(self, password_plain):
        """
        Generate and set password hash from given plain text password.
        """
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        """
        Check given plaintext password agains internal password hash.
        """
        return check_password_hash(self.password, password_plain)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':                 self.id,
            'createtime':         str(self.createtime),
            'logintime':          str(self.logintime),
            'login':              self.login,
            'fullname':           self.fullname,
            'email':              self.email,
            'organization':       self.organization,
            'roles':              [ str(x) for x in self.roles],
            'apikey':             self.apikey,
            'password':           self.password,
            'enabled':            bool(self.enabled),
            'locale':             self.locale,
            'timezone':           self.timezone,
            'memberships':        [(x.id, x.name) for x in self.memberships],
            'memberships_wanted': [(x.id, x.name) for x in self.memberships_wanted],
            'managements':        [(x.id, x.name) for x in self.managements]
        }

    #---------------------------------------------------------------------------
    # Custom methods for Hawat user interface. Just couple of methods required by
    # the flask_login extension.
    #---------------------------------------------------------------------------

    @property
    def is_authenticated(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return True

    @property
    def is_active(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return self.enabled

    @property
    def is_anonymous(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return False

    def get_id(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def has_role(self, role):
        """
        Returns ``True`` if the user identifies with the specified role.

        :param str role: A role name.
        """
        return role in self.roles

    def has_no_role(self):
        """
        Returns ``True`` if the user has no role.
        """
        return len(self.roles) == 0


def usermodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.UserModel`
    object from :py:class:`mentat.datatype.internal.User` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = UserModel()
    sqlobj.login        = structure.get('_id')
    sqlobj.createtime   = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.fullname     = structure.get('name')
    sqlobj.email        = structure.get('email', structure.get('_id'))
    sqlobj.organization = structure.get('organization')
    sqlobj.roles        = [str(i) for i in structure.get('roles', [])]
    sqlobj.enabled      = 'user' in sqlobj.roles

    return sqlobj


class GroupModel(MODEL):
    """
    Class representing group objects within the SQL database mapped to ``groups``
    table.
    """
    __tablename__ = 'groups'

    name        = sqlalchemy.Column(sqlalchemy.String(100), unique = True, index = True)
    source      = sqlalchemy.Column(sqlalchemy.String(50), nullable = False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    enabled     = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = True)

    members = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_members, back_populates = 'memberships', order_by = 'UserModel.fullname')
    members_wanted = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_members_wanted, back_populates = 'memberships_wanted', order_by = 'UserModel.fullname')
    managers = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_managers, back_populates = 'managements', order_by = 'UserModel.fullname')

    networks = sqlalchemy.orm.relationship('NetworkModel', back_populates = 'group', cascade = 'all, delete-orphan', order_by = 'NetworkModel.netname')
    filters  = sqlalchemy.orm.relationship('FilterModel', back_populates = 'group', cascade = 'all, delete-orphan', order_by = 'FilterModel.name')
    reports  = sqlalchemy.orm.relationship('EventReportModel', secondary = _asoc_groups_reports, back_populates = 'groups', order_by = 'EventReportModel.label')

    settings_rep = sqlalchemy.orm.relationship('SettingsReportingModel', uselist = False, back_populates = 'group', cascade = 'all, delete-orphan')

    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))
    children  = sqlalchemy.orm.relationship('GroupModel', backref = sqlalchemy.orm.backref('parent', remote_side='GroupModel.id'))

    def __repr__(self):
        return "<Group(name='%s')>" % (self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def is_state_enabled(self):
        """
        Check if current group state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current group state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current group state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current group state to disabled.
        """
        self.enabled = False

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':             int(self.id),
            'createtime':     str(self.createtime),
            'name':           str(self.name),
            'source':         str(self.source),
            'description':    str(self.description),
            'enabled':        bool(self.enabled),
            'members':        [(x.id, x.login) for x in self.members],
            'members_wanted': [(x.id, x.login) for x in self.members_wanted],
            'managers':       [(x.id, x.login) for x in self.managers],
            'networks':       [(x.id, x.network) for x in self.networks],
            'filters':        [(x.id, x.filter) for x in self.filters],
            'parent':         str(self.parent),
        }

def groupmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.GroupModel`
    object from :py:class:`mentat.datatype.internal.AbuseGroup` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = GroupModel()
    sqlobj.name        = structure.get('_id')
    sqlobj.source      = structure.get('source')
    sqlobj.description = structure.get('description', defaults.get('netname', '-- undisclosed --'))
    sqlobj.createtime  = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init

    return sqlobj


class NetworkModel(MODEL):
    """
    Class representing network records objects within the SQL database mapped to
    ``networks`` table.
    """
    __tablename__ = 'networks'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group    = sqlalchemy.orm.relationship('GroupModel', back_populates = 'networks')

    netname     = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    source      = sqlalchemy.Column(sqlalchemy.String(50), nullable = False)
    network     = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    description = sqlalchemy.Column(sqlalchemy.String)
    rank        = sqlalchemy.Column(sqlalchemy.Integer)
    is_base     = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = False)

    def __repr__(self):
        return "<Network(netname='%s',network='%s')>" % (self.netname, self.network)

    def __str__(self):
        return '{}'.format(self.netname)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':          int(self.id),
            'createtime':  str(self.createtime),
            'group':       str(self.group),
            'netname':     str(self.netname),
            'source':      str(self.source),
            'network':     str(self.network),
            'description': str(self.description),
            'rank':        int(self.rank) if self.rank else None,
            'is_base':     bool(self.is_base)
        }

def networkmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.NetworkModel`
    object from :py:class:`mentat.datatype.internal.NetworkRecord` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = NetworkModel()
    sqlobj.network     = structure.get('network')
    sqlobj.source      = structure.get('source')
    sqlobj.netname     = structure.get('netname', defaults.get('netname', '-- undisclosed --'))
    sqlobj.description = structure.get('description', defaults.get('description', None))
    sqlobj.rank        = structure.get('rank', None)
    sqlobj.is_base     = bool(structure.get('is_base', False))

    return sqlobj


class FilterModel(MODEL):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing reporting filters objects within the SQL database mapped to
    ``filters`` table.
    """
    __tablename__ = 'filters'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group    = sqlalchemy.orm.relationship('GroupModel', back_populates = 'filters')

    name        = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    type        = sqlalchemy.Column(sqlalchemy.Enum(*REPORTING_FILTERS, name='filter_types'), default = REPORTING_FILTER_BASIC, nullable = False)
    filter      = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    valid_from  = sqlalchemy.Column(sqlalchemy.DateTime)
    valid_to    = sqlalchemy.Column(sqlalchemy.DateTime)
    enabled     = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)
    detectors   = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    categories  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    sources     = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    hits        = sqlalchemy.Column(sqlalchemy.Integer, default = 0, nullable = False)
    last_hit    = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return "<Filter(name='%s')>" % (self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def is_state_enabled(self):
        """
        Check if current filter state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current filter state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current filter state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current filter state to disabled.
        """
        self.enabled = False

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':          int(self.id),
            'createtime':  str(self.createtime),
            'group':       str(self.group),
            'name':        str(self.name),
            'type':        str(self.type),
            'filter':      str(self.filter),
            'description': str(self.description),
            'valid_from':  str(self.valid_from),
            'valid_to':    str(self.valid_to),
            'enabled':     bool(self.enabled),
            'detectors':   [str(x) for x in self.detectors],
            'categories':  [str(x) for x in self.categories],
            'sources':     [str(x) for x in self.sources],
            'hits':        int(self.hits),
            'last_hit':    str(self.last_hit)
        }

def filtermodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.NetworkModel`
    object from :py:class:`mentat.datatype.internal.NetworkRecord` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = FilterModel()

    sqlobj.name        = structure.get('_id')
    sqlobj.createtime  = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.type        = structure.get('type')
    sqlobj.filter      = structure.get('filter')
    sqlobj.description = structure.get('description') + structure.get('note', '')
    sqlobj.valid_from  = structure.get('validfrom', None)
    sqlobj.valid_to    = structure.get('validto', None)
    sqlobj.enabled     = bool(structure.get('enabled', False))
    sqlobj.detectors   = structure.get('analyzers', [])
    sqlobj.categories  = structure.get('categories', [])
    sqlobj.sources     = structure.get('ips', [])
    sqlobj.hits        = structure.get('hits', 0)
    sqlobj.last_hit    = structure.get('lasthit', None)

    return sqlobj


class SettingsReportingModel(MODEL):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class representing reporting settings objects within the SQL database mapped to
    ``settings_reporting`` table.
    """
    __tablename__ = 'settings_reporting'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group = sqlalchemy.orm.relationship('GroupModel', back_populates = 'settings_rep')

    emails_low = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_medium = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_high = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_critical = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    mode = sqlalchemy.Column(sqlalchemy.Enum(*REPORTING_MODES, name='reporting_modes'))
    locale = sqlalchemy.Column(sqlalchemy.String)
    timezone = sqlalchemy.Column(sqlalchemy.String)

    redirect = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return "<SettingsReporting(id='%d',group_id='%d')>" % (int(self.id), int(self.group_id))

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':                 int(self.id),
            'createtime':         str(self.createtime),
            'group':              str(self.group),
            'emails_low':         [str(x) for x in self.emails_low],
            'emails_medium':      [str(x) for x in self.emails_medium],
            'emails_high':        [str(x) for x in self.emails_high],
            'emails_critical':    [str(x) for x in self.emails_critical],
            'mode':               str(self.mode) if self.mode is not None else None,
            'locale':             str(self.locale) if self.locale is not None else None,
            'timezone':           str(self.timezone) if self.timezone is not None else None,
            'redirect':           bool(self.redirect) if self.redirect is not None else None
        }

def setrepmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.SettingsReportingModel`
    object from :py:class:`mentat.datatype.internal.AbuseGroup` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = SettingsReportingModel()
    sqlobj.emails_low         = structure.get('rep_emails_low', [])
    sqlobj.emails_medium      = structure.get('rep_emails_medium', [])
    sqlobj.emails_high        = structure.get('rep_emails_high', [])
    sqlobj.emails_critical    = structure.get('rep_emails_critical', [])
    sqlobj.mode               = structure.get('rep_mode', None)
    sqlobj.redirect           = structure.get('rep_redirect', None)

    if sqlobj.emails and '@' not in sqlobj.emails[0]:
        sqlobj.emails = [''.join(sqlobj.emails)]

    return sqlobj


class EventStatisticsModel(MODEL):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing event statistics objects within the SQL database mapped to
    ``statistics_events`` table.
    """
    __tablename__ = 'statistics_events'

    interval       = sqlalchemy.Column(sqlalchemy.String, nullable = False, unique = True, index = True)
    dt_from        = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    dt_to          = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    delta          = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    count          = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    stats_overall  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    stats_internal = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    stats_external = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))

    def __repr__(self):
        return "<EventStatistics(interval='%s',delta='%d')>" % (self.interval, self.delta)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':             int(self.id),
            'createtime':     str(self.createtime),
            'interval':       str(self.interval),
            'dt_from':        str(self.dt_from),
            'dt_to':          str(self.dt_to),
            'delta':          int(self.delta),
            'count':          int(self.count),
            'stats_overall':  self.stats_overall,
            'stats_internal': self.stats_internal,
            'stats_external': self.stats_external
        }

    @staticmethod
    def format_interval(dtl, dth):
        """
        Format two given timestamps into single string desribing the interval
        between them. This string can be then used as a form of a label.

        :param datetime.datetime dtl: Lower interval boundary.
        :param datetime.datetime dth: Upper interval boundary.
        :return: Interval between timestamps.
        :rtype: str
        """
        return '{}_{}'.format(dtl.strftime('%FT%T'), dth.strftime('%FT%T'))

    def calculate_interval(self):
        """
        Calculate and set internal interval label.
        """
        self.interval = self.format_interval(self.dt_from, self.dt_to)

    def calculate_delta(self):
        """
        Calculate and set delta between internal time interval boundaries.
        """
        delta = self.dt_to - self.dt_from
        self.delta = delta.total_seconds()

def eventstatsmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.EventStatisticsModel`
    object from :py:class:`mentat.datatype.internal.EventStat` objects.
    """
    if not defaults:
        defaults = {}

    interval = '{}_{}'.format(structure['ts_from'].strftime('%FT%T'), structure['ts_to'].strftime('%FT%T'))
    delta = structure['ts_to'] - structure['ts_from']

    sqlobj = EventStatisticsModel()
    sqlobj.interval       = interval
    sqlobj.createtime     = structure['ts']  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.dt_from        = structure['ts_from']
    sqlobj.dt_to          = structure['ts_to']
    sqlobj.delta          = delta.total_seconds()
    sqlobj.count          = structure.get('count', structure['overall'].get('cnt_alerts'))
    sqlobj.stats_overall  = structure['overall']
    sqlobj.stats_internal = structure.get('internal', dict())
    sqlobj.stats_external = structure.get('external', dict())

    return sqlobj


class EventReportModel(MODEL):
    """
    Class representing event report objects within the SQL database mapped to
    ``reports_events`` table.
    """
    __tablename__ = 'reports_events'

    #group_name = sqlalchemy.Column(sqlalchemy.String, nullable = False, index = True)
    groups    = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_groups_reports, back_populates = 'reports')

    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('reports_events.id'))
    children  = sqlalchemy.orm.relationship('EventReportModel', backref = sqlalchemy.orm.backref('parent', remote_side='EventReportModel.id'))

    label    = sqlalchemy.Column(sqlalchemy.String, nullable = False, unique = True, index = True)
    severity = sqlalchemy.Column(sqlalchemy.Enum(*REPORT_SEVERITIES, name='report_severities'), nullable = False)
    type     = sqlalchemy.Column(sqlalchemy.Enum(*REPORT_TYPES, name='report_types'), nullable = False)
    message  = sqlalchemy.Column(sqlalchemy.String)

    dt_from = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    dt_to   = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    delta   = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)

    flag_testdata = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)
    flag_mailed   = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)

    # Number of events actually in report (evcount_thr + evcount_rlp).
    evcount_rep     = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    # Initial number of events for reporting (evcount_new + evcount_rlp).
    evcount_all     = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    # Number of matching events fetched from database.
    evcount_new     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events remaining after filtering.
    evcount_flt     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events blocked by filters (evcount_new - evcount_flt).
    evcount_flt_blk = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events remaining after thresholding.
    evcount_thr     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events blocked by thresholds (evcount_flt - evcount_thr).
    evcount_thr_blk = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of relapsed events.
    evcount_rlp     = sqlalchemy.Column(sqlalchemy.Integer)

    mail_to  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    mail_dt  = sqlalchemy.Column(sqlalchemy.DateTime)
    mail_res = sqlalchemy.Column(sqlalchemy.String)

    statistics = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    filtering  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    structured_data = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null=True))

    def __repr__(self):
        return "<EventReport(label='%s')>" % (self.label)

    def __str__(self):
        return '{}'.format(self.label)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':              int(self.id),
            'createtime':      str(self.createtime),
            'groups':          [str(group) for group in self.groups],
            'parent':          str(self.parent),
            'label':           str(self.label),
            'severity':        str(self.severity),
            'type':            str(self.type),
            'message':         str(self.message),
            'dt_from':         str(self.dt_from),
            'dt_to':           str(self.dt_to),
            'delta':           str(self.delta),
            'flag_testdata':   bool(self.flag_testdata),
            'flag_mailed':     bool(self.flag_mailed),
            'evcount_rep':     int(self.evcount_rep) if self.evcount_rep else 0,
            'evcount_all':     int(self.evcount_all) if self.evcount_all else 0,
            'evcount_new':     int(self.evcount_new) if self.evcount_new else 0,
            'evcount_flt':     int(self.evcount_flt) if self.evcount_flt else 0,
            'evcount_flt_blk': int(self.evcount_flt_blk) if self.evcount_flt_blk else 0,
            'evcount_thr':     int(self.evcount_thr) if self.evcount_thr else 0,
            'evcount_thr_blk': int(self.evcount_thr_blk) if self.evcount_thr_blk else 0,
            'evcount_rlp':     int(self.evcount_rlp) if self.evcount_rlp else 0,
            'mail_to':         str(self.mail_to),
            'mail_dt':         str(self.mail_dt),
            'mail_res':        str(self.mail_res),
            'statistics':      str(self.statistics),
            'filtering':       str(self.filtering),
            'structured_data': str(self.structured_data),
        }

    def calculate_delta(self):
        """
        Calculate delta between internal time interval boundaries.
        """
        delta = self.dt_to - self.dt_from
        self.delta = delta.total_seconds()
        return self.delta

    def generate_label(self):
        """
        Generate and set label from internal attributes.
        """
        dt_cur = datetime.datetime.utcnow()
        self.label = 'M{:4d}{:02d}{:02d}{:1s}{:1s}-{:5s}'.format(
            dt_cur.year,
            dt_cur.month,
            dt_cur.day,
            self.type[0].upper(),
            self.severity[0].upper(),
            ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        )
        return self.label

class ItemChangeLogModel(MODEL):
    """
    Class representing item changelog records within the SQL database mapped to
    ``changelogs_items`` table.
    """
    __tablename__ = 'changelogs_items'

    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', onupdate = "CASCADE"))
    author    = sqlalchemy.orm.relationship('UserModel', back_populates = 'changelogs', enable_typechecks = False)
    model_id  = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    model     = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    endpoint  = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    module    = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    operation = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    before    = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    after     = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    diff      = sqlalchemy.Column(sqlalchemy.String, nullable = False)

    def __repr__(self):
        return "<ItemChangelog(author='%s',operation='%s',model='%s#%s')>" % (str(self.author), self.operation, self.model, self.model_id)

    def __str__(self):
        return 'ICL#{:d}:{:s}#{:d}:{:s}'.format(self.id, self.model, self.model_id, self.operation)

    def calculate_diff(self):
        """
        Calculate difference between internal ``before`` and ``after`` attributes
        and store it internally into ``diff`` attribute.
        """
        self.diff = jsondiff(self.before, self.after)


#-------------------------------------------------------------------------------


def jsondiff(json_obj_a, json_obj_b):
    """
    Calculate the difference between two model objects given as JSON strings.
    """
    return "\n".join(
        difflib.unified_diff(json_obj_a.split("\n"), json_obj_b.split("\n"))
    )

def dictdiff(dict_obj_a, dict_obj_b):
    """
    Calculate the difference between two model objects given as dicts.
    """
    json_obj_a = json.dumps(dict_obj_a, indent = 4, sort_keys = True)
    json_obj_b = json.dumps(dict_obj_b, indent = 4, sort_keys = True)
    return jsondiff(json_obj_a, json_obj_b)

def diff(obj_a, obj_b):
    """
    Calculate the difference between two model objects given as dicts.
    """
    return jsondiff(obj_a.to_json(), obj_b.to_json())

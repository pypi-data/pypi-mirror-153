#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Honza Mach <honza.mach.ml@gmail.com>"


import datetime
import json
import difflib

from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy
import sqlalchemy.dialects.postgresql
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from vial.db import MODEL


#
# Modify compilation of DROP TABLE for PostgreSQL databases to enable CASCADE feature.
# Otherwise it is not possible to delete the database schema with:
#   MODEL.metadata.drop_all(engine)
#
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):  # pylint: disable=locally-disabled,unused-argument
    return compiler.visit_drop_table(element) + " CASCADE"


class BaseMixin:
    """
    Base class providing usefull mixin functionality.
    """
    id = sqlalchemy.Column(  # pylint: disable=locally-disabled,invalid-name
        sqlalchemy.Integer,
        primary_key = True
    )
    createtime = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default = datetime.datetime.utcnow
    )

    def get_id(self):
        """
        Getter for retrieving current primary ID.
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
        return json.dumps(
            self.to_dict(),
            indent = 4,
            sort_keys = True
        )

_asoc_group_members = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members',
    MODEL.metadata,
    sqlalchemy.Column(
        'group_id',
        sqlalchemy.ForeignKey('groups.id'),
        primary_key = True
    ),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.ForeignKey('users.id'),
        primary_key = True
    )
)
"""
Association table representing user*group relation: group membership.

What users are members of what groups.
"""

_asoc_group_members_wanted = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members_wanted',
    MODEL.metadata,
    sqlalchemy.Column(
        'group_id',
        sqlalchemy.ForeignKey('groups.id'),
        primary_key = True
    ),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.ForeignKey('users.id'),
        primary_key = True
    ),
)
"""
Association table representing user*group relation: wanted group membership.

What users want to be members of what groups.
"""

_asoc_group_managers = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_managers',
    MODEL.metadata,
    sqlalchemy.Column(
        'group_id',
        sqlalchemy.ForeignKey('groups.id'),
        primary_key = True
    ),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.ForeignKey('users.id'),
        primary_key = True
    )
)
"""
Association table representing user*group relation: group management.

What users can manage what groups.
"""


class UserModel(MODEL, BaseMixin):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing user objects within the SQL database mapped to ``users``
    table.
    """
    __tablename__ = 'users'

    login = sqlalchemy.Column(
        sqlalchemy.String(50),
        unique = True,
        index = True
    )
    fullname = sqlalchemy.Column(
        sqlalchemy.String(100),
        nullable = False
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(250),
        nullable = False
    )
    roles = sqlalchemy.Column(
        sqlalchemy.dialects.postgresql.ARRAY(
            sqlalchemy.String(20),
            dimensions = 1
        ),
        nullable = False,
        default = []
    )
    enabled = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable = False,
        default = True
    )

    password = sqlalchemy.Column(
        sqlalchemy.String
    )
    apikey = sqlalchemy.Column(
        sqlalchemy.String,
        index = True
    )

    locale = sqlalchemy.Column(
        sqlalchemy.String(20)
    )
    timezone = sqlalchemy.Column(
        sqlalchemy.String(50)
    )

    memberships = sqlalchemy.orm.relationship(
        'GroupModel',
        secondary = _asoc_group_members,
        back_populates = 'members'
    )
    memberships_wanted = sqlalchemy.orm.relationship(
        'GroupModel',
        secondary = _asoc_group_members_wanted,
        back_populates =
        'members_wanted',
        order_by = 'GroupModel.name'
    )
    managements = sqlalchemy.orm.relationship(
        'GroupModel',
        secondary = _asoc_group_managers,
        back_populates = 'managers'
    )

    changelogs  = sqlalchemy.orm.relationship('ItemChangeLogModel', back_populates = 'author', order_by = 'ItemChangeLogModel.createtime')

    logintime = sqlalchemy.Column(
        sqlalchemy.DateTime
    )

    def __repr__(self):
        return "<User(login='{}', fullname='{}')>".format(self.login, self.fullname)

    def __str__(self):
        return '{}'.format(self.login)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mydojo.db.BaseMixin.to_dict` method.
        """
        return {
            'id':                 self.id,
            'createtime':         str(self.createtime),
            'logintime':          str(self.logintime),
            'login':              self.login,
            'fullname':           self.fullname,
            'email':              self.email,
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

    @classmethod
    def from_dict(cls, structure, defaults = None):
        """
        Convenience method for creating :py:class:`mydojo.db.UserModel` object
        from ``dict`` objects.
        """
        if not defaults:
            defaults = {}

        sqlobj = cls()
        sqlobj.login    = structure.get('login')
        sqlobj.fullname = structure.get('fullname')
        sqlobj.email    = structure.get('email', structure.get('login'))
        sqlobj.roles    = [str(i) for i in structure.get('roles', [])]
        sqlobj.enabled  = structure.get('enabled', None)
        sqlobj.password = structure.get('password', None)
        sqlobj.apikey   = structure.get('apikey', None)
        sqlobj.locale   = structure.get('locale', None)
        sqlobj.timezone = structure.get('timezone', None)

        return sqlobj

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


class GroupModel(MODEL, BaseMixin):
    """
    Class representing group objects within the SQL database mapped to ``groups``
    table.
    """
    __tablename__ = 'groups'

    name = sqlalchemy.Column(
        sqlalchemy.String(100),
        unique = True,
        index = True
    )
    description = sqlalchemy.Column(
        sqlalchemy.String
    )
    enabled = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable = False,
        default = True
    )

    members = sqlalchemy.orm.relationship(
        'UserModel',
        secondary = _asoc_group_members,
        back_populates = 'memberships'
    )
    members_wanted = sqlalchemy.orm.relationship(
        'UserModel',
        secondary = _asoc_group_members_wanted,
        back_populates = 'memberships_wanted',
        order_by = 'UserModel.fullname'
    )
    managers = sqlalchemy.orm.relationship(
        'UserModel',
        secondary = _asoc_group_managers,
        back_populates = 'managements'
    )

    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('groups.id')
    )
    children = sqlalchemy.orm.relationship(
        'GroupModel',
        backref = sqlalchemy.orm.backref(
            'parent',
            remote_side = 'GroupModel.id'
        )
    )

    def __repr__(self):
        return "<Group(name='{}')>".format(self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mydojo.db.BaseMixin.to_dict` method.
        """
        return {
            'id':          int(self.id),
            'createtime':  str(self.createtime),
            'name':        str(self.name),
            'description': str(self.description),
            'enabled':     bool(self.enabled),
            'members':     [(x.id, x.login) for x in self.members],
            'managers':    [(x.id, x.login) for x in self.managers],
            'parent':      str(self.parent),
        }

    @classmethod
    def from_dict(cls, structure, defaults = None):
        """
        Convenience method for creating :py:class:`mydojo.db.GroupModel` object
        from ``dict`` objects.
        """
        if not defaults:
            defaults = {}

        sqlobj = cls()
        sqlobj.createtime  = structure.get('createtime')
        sqlobj.name        = structure.get('name')
        sqlobj.description = structure.get('description', '-- undisclosed --')

        return sqlobj


class ItemChangeLogModel(MODEL, BaseMixin):
    """
    Class representing item changelog records within the SQL database mapped to
    ``changelogs_items`` table.
    """
    __tablename__ = 'changelogs_items'

    author_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id', onupdate = "CASCADE")
    )
    author = sqlalchemy.orm.relationship(
        'UserModel',
        back_populates = 'changelogs',
        enable_typechecks = False
    )
    model_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable = False
    )
    model = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    endpoint = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    module = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    operation = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    before = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    after = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )
    diff = sqlalchemy.Column(
        sqlalchemy.String,
        nullable = False
    )

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This file contains pluggable module for Hawat web interface containing features
related to user group management. These features include:

* general group listing
* detailed group view
* creating new groups
* updating existing groups
* deleting existing groups
* enabling existing groups
* disabling existing groups
* adding group members
* removing group members
* rejecting group membership requests
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask_login
from flask_babel import gettext, lazy_gettext
from sqlalchemy import and_, or_

from mentat.datatype.sqldb import SettingsReportingModel, FilterModel, NetworkModel, ItemChangeLogModel
from mentat.const import tr_

import vial.acl
import vial.menu
from vial.utils import URLParamsBuilder
import vial.blueprints.groups
from vial.blueprints.groups import BLUEPRINT_NAME, ListView, EnableView, DisableView, DeleteView, AddMemberView, RejectMemberView, RemoveMemberView, AddManagerView, RemoveManagerView
import hawat.const
from hawat.blueprints.groups.forms import AdminCreateGroupForm, AdminUpdateGroupForm,\
    UpdateGroupForm


class ShowView(vial.blueprints.groups.ShowView):
    """
    Detailed group view.
    """

    def do_before_response(self, **kwargs):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'users.show',
            hidetitle = True,
        )
        action_menu.add_entry(
            'submenu',
            'more',
            align_right = True,
            legend = gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_membership',
            endpoint = 'users.addmembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.reject_membership',
            endpoint = 'users.rejectmembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_membership',
            endpoint = 'users.removemembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_management',
            endpoint = 'users.addmanagement'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_management',
            endpoint = 'users.removemanagement'
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'users.enable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'users.disable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'users.update'
        )
        self.response_context.update(context_action_menu_users = action_menu)

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'networks.show',
            hidetitle = True,
        )
        self.response_context.update(context_action_menu_networks = action_menu)

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'filters.show',
            hidetitle = True,
        )
        self.response_context.update(context_action_menu_filters = action_menu)

        item = self.response_context['item']
        if self.can_access_endpoint('groups.update', item = item) and self.has_endpoint('changelogs.search'):
            self.response_context.update(
                context_action_menu_changelogs = self.get_endpoint_class(
                    'changelogs.search'
                ).get_context_action_menu()
            )

            item_changelog = self.dbsession.query(ItemChangeLogModel).\
                filter(
                    or_(
                        # Changelogs related directly to group item.
                        and_(
                            ItemChangeLogModel.model == item.__class__.__name__,
                            ItemChangeLogModel.model_id == item.id
                        ),
                        # Changelogs related to group reporting settings item.
                        and_(
                            ItemChangeLogModel.model == SettingsReportingModel.__name__,
                            ItemChangeLogModel.model_id.in_(
                                self.dbsession.query(SettingsReportingModel.id).filter(SettingsReportingModel.group_id == item.id)
                            )
                        ),
                        # Changelogs related to all group reporting filters.
                        and_(
                            ItemChangeLogModel.model == FilterModel.__name__,
                            ItemChangeLogModel.model_id.in_(
                                self.dbsession.query(FilterModel.id).filter(FilterModel.group_id == item.id)
                            )
                        ),
                        # Changelogs related to all group network records.
                        and_(
                            ItemChangeLogModel.model == NetworkModel.__name__,
                            ItemChangeLogModel.model_id.in_(
                                self.dbsession.query(NetworkModel.id).filter(NetworkModel.group_id == item.id)
                            )
                        )
                    )
                ).\
                order_by(ItemChangeLogModel.createtime.desc()).\
                limit(100).\
                all()
            self.response_context.update(item_changelog = item_changelog)


class ShowByNameView(ShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed group view by group name.
    """

    @classmethod
    def get_view_name(cls):
        return 'show_by_name'

    @classmethod
    def get_view_template(cls):
        return '{}/show.html'.format(cls.module_name)

    @property
    def search_by(self):
        return self.dbmodel.name


class CreateView(vial.blueprints.groups.CreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new groups.
    """

    @staticmethod
    def get_item_form(item):
        return AdminCreateGroupForm()

    def do_before_action(self, item):
        # Create empty reporting settings object and assign it to the group.
        SettingsReportingModel(group = item)


class UpdateView(vial.blueprints.groups.UpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing groups.
    """

    @staticmethod
    def get_item_form(item):
        admin = flask_login.current_user.has_role('admin')
        if not admin:
            form = UpdateGroupForm(obj = item)
        else:
            form = AdminUpdateGroupForm(db_item_id = item.id, obj = item)
        return form


#-------------------------------------------------------------------------------


class GroupsBlueprint(vial.blueprints.groups.GroupsBlueprint):
    """Pluggable module - user groups (*groups*)."""

    def register_app(self, app):

        def _fetch_my_groups():
            groups = {}
            for i in list(flask_login.current_user.memberships) + list(flask_login.current_user.managements):
                groups[str(i)] = i
            return list(sorted(groups.values(), key = str))

        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 50,
            view = ListView
        )
        app.menu_auth.add_entry(
            'submenudb',
            'my_groups',
            position = 20,
            title = lazy_gettext('My groups'),
            resptitle = True,
            icon = 'module-groups',
            align_right = True,
            entry_fetcher = _fetch_my_groups,
            entry_builder = lambda x, y: vial.menu.EndpointEntry(x, endpoint = 'groups.show', params = {'item': y}, title = x, icon = 'module-groups')
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('View details of abuse group <strong>%(name)s</strong>'),
            ShowByNameView,
            URLParamsBuilder().add_rule('item_id')
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = GroupsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ListView,          '/list')
    hbp.register_view_class(CreateView,        '/create')
    hbp.register_view_class(ShowView,          '/<int:item_id>/show')
    hbp.register_view_class(ShowByNameView,    '/<item_id>/show_by_name')
    hbp.register_view_class(UpdateView,        '/<int:item_id>/update')
    hbp.register_view_class(AddMemberView,     '/<int:item_id>/add_member/<int:other_id>')
    hbp.register_view_class(RejectMemberView,  '/<int:item_id>/reject_member/<int:other_id>')
    hbp.register_view_class(RemoveMemberView,  '/<int:item_id>/remove_member/<int:other_id>')
    hbp.register_view_class(AddManagerView,    '/<int:item_id>/add_manager/<int:other_id>')
    hbp.register_view_class(RemoveManagerView, '/<int:item_id>/remove_manager/<int:other_id>')
    hbp.register_view_class(EnableView,        '/<int:item_id>/enable')
    hbp.register_view_class(DisableView,       '/<int:item_id>/disable')
    hbp.register_view_class(DeleteView,        '/<int:item_id>/delete')

    return hbp

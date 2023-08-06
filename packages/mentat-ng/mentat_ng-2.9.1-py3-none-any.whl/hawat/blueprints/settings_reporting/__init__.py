#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access to group reporting settings management features.
These features include:

* detailed reporting settings view
* creating new reporting settings
* updating existing reporting settings
* deleting existing reporting settings
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask
import flask_principal
from flask_babel import gettext, lazy_gettext

import mentat.reports.utils
from mentat.datatype.sqldb import SettingsReportingModel, ItemChangeLogModel

import vial.acl
from vial.app import VialBlueprint
from vial.view import ItemShowView, ItemCreateView, ItemUpdateView
from vial.view.mixin import HTMLMixin, SQLAlchemyMixin
from hawat.blueprints.settings_reporting.forms import CreateSettingsReportingForm,\
    UpdateSettingsReportingForm


BLUEPRINT_NAME = 'settings_reporting'
"""Name of the blueprint as module global constant."""


class ShowView(HTMLMixin, SQLAlchemyMixin, ItemShowView):
    """
    Detailed reporting settings view.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'module-settings-reporting'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show reporting settings')

    @property
    def dbmodel(self):
        return SettingsReportingModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_mm = flask_principal.Permission(
            vial.acl.MembershipNeed(kwargs['item'].group.id),
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_mm.can()

    @classmethod
    def get_breadcrumbs_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        action_menu = vial.menu.Menu()

        action_menu.add_entry(
            'endpoint',
            'home',
            endpoint = flask.current_app.config['ENDPOINT_HOME']
        )
        action_menu.add_entry(
            'endpoint',
            'list',
            endpoint = 'groups.list'
        )
        action_menu.add_entry(
            'endpoint',
            'pshow',
            endpoint = 'groups.show'
        )
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = '{}.show'.format(cls.module_name),
        )

        return action_menu

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'showgroup',
            endpoint = 'groups.show',
            title = lazy_gettext('Group')
        )
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'settings_reporting.update'
        )
        return action_menu

    def do_before_response(self, **kwargs):
        item = self.response_context['item']
        system_default_repsettings = mentat.reports.utils.ReportingSettings(
            item.group
        )
        self.response_context.update(
            system_default_repsettings = system_default_repsettings
        )

        if self.can_access_endpoint('settings_reporting.update', item = item) and self.has_endpoint('changelogs.search'):
            self.response_context.update(
                context_action_menu_changelogs = self.get_endpoint_class(
                    'changelogs.search'
                ).get_context_action_menu()
            )

            item_changelog = self.dbsession.query(ItemChangeLogModel).\
                filter(ItemChangeLogModel.model == item.__class__.__name__).\
                filter(ItemChangeLogModel.model_id == item.id).\
                order_by(ItemChangeLogModel.createtime.desc()).\
                limit(100).\
                all()
            self.response_context.update(item_changelog = item_changelog)

class CreateView(HTMLMixin, SQLAlchemyMixin, ItemCreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new reporting settings.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Create reporting settings')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Create new reporting settings')

    @property
    def dbmodel(self):
        return SettingsReportingModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting settings <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> were successfully created.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to create new reporting settings for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled creating new reporting settings for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_item_form():
        return CreateSettingsReportingForm()


class UpdateView(HTMLMixin, SQLAlchemyMixin, ItemUpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing reporting settings.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Update details of reporting settings for group &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].group.name)
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Update reporting settings details')

    @property
    def dbmodel(self):
        return SettingsReportingModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting settings <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> were successfully updated.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to update reporting settings <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled updating reporting settings <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_item_form(item):
        return UpdateSettingsReportingForm(obj = item)


#-------------------------------------------------------------------------------


class SettingsReportingBlueprint(VialBlueprint):
    """Pluggable module - reporting settings. (*settings_reporting*)"""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Reporting settings management')


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = SettingsReportingBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(CreateView, '/create')
    hbp.register_view_class(ShowView,   '/<int:item_id>/show')
    hbp.register_view_class(UpdateView, '/<int:item_id>/update')

    return hbp

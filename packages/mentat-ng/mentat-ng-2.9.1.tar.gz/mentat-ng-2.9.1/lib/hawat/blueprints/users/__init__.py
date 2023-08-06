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
related to user account management. These features include:

* general user account listing
* detailed user account view
* creating new user accounts
* updating existing user accounts
* deleting existing user accounts
* enabling existing user accounts
* disabling existing user accounts
* adding group memberships
* removing group memberships
* rejecting group membership requests
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask
import flask_login
from flask_babel import lazy_gettext

import vial.blueprints.users
from vial.blueprints.users import BLUEPRINT_NAME, ListView, ShowView, MeView,\
    EnableView, DisableView, DeleteView, AddMembershipView, RejectMembershipView, RemoveMembershipView, AddManagementView, RemoveManagementView
from hawat.blueprints.users.forms import CreateUserAccountForm, UpdateUserAccountForm,\
    AdminUpdateUserAccountForm


class CreateView(vial.blueprints.users.CreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new user accounts.
    """

    @staticmethod
    def get_item_form(item):
        #
        # Inject list of choices for supported locales and roles. Another approach
        # would be to let the form get the list on its own, however that would create
        # dependency on application object.
        #
        roles = list(zip(flask.current_app.config['ROLES'], flask.current_app.config['ROLES']))
        locales = list(flask.current_app.config['SUPPORTED_LOCALES'].items())

        return CreateUserAccountForm(
            choices_roles = roles,
            choices_locales = locales
        )


class UpdateView(vial.blueprints.users.UpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing user accounts.
    """

    @staticmethod
    def get_item_form(item):
        #
        # Inject list of choices for supported locales and roles. Another approach
        # would be to let the form get the list on its own, however that would create
        # dependency on application object.
        #
        roles = list(zip(flask.current_app.config['ROLES'], flask.current_app.config['ROLES']))
        locales = list(flask.current_app.config['SUPPORTED_LOCALES'].items())

        admin = flask_login.current_user.has_role('admin')
        if not admin:
            form = UpdateUserAccountForm(
                choices_roles = roles,
                choices_locales = locales,
                obj = item
            )
        else:
            form = AdminUpdateUserAccountForm(
                choices_roles = roles,
                choices_locales = locales,
                db_item_id = item.id,
                obj = item
            )
        return form


#-------------------------------------------------------------------------------


class UsersBlueprint(vial.blueprints.users.UsersBlueprint):
    """Pluggable module - user account management (*users*)."""

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 40,
            group = lazy_gettext('Object management'),
            view = ListView
        )
        app.menu_auth.add_entry(
            'view',
            'my_account',
            position = 10,
            view = MeView,
            params = lambda: {'item': flask_login.current_user}
        )

        app.set_infomailer('users.enable', EnableView.inform_user)


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = UsersBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ListView,             '/list')
    hbp.register_view_class(CreateView,           '/create')
    hbp.register_view_class(ShowView,             '/<int:item_id>/show')
    hbp.register_view_class(MeView,               '/me')
    hbp.register_view_class(UpdateView,           '/<int:item_id>/update')
    hbp.register_view_class(AddMembershipView,    '/<int:item_id>/add_membership/<int:other_id>')
    hbp.register_view_class(RemoveMembershipView, '/<int:item_id>/remove_membership/<int:other_id>')
    hbp.register_view_class(RejectMembershipView, '/<int:item_id>/reject_membership/<int:other_id>')
    hbp.register_view_class(AddManagementView,    '/<int:item_id>/add_management/<int:other_id>')
    hbp.register_view_class(RemoveManagementView, '/<int:item_id>/remove_management/<int:other_id>')
    hbp.register_view_class(EnableView,           '/<int:item_id>/enable')
    hbp.register_view_class(DisableView,          '/<int:item_id>/disable')
    hbp.register_view_class(DeleteView,           '/<int:item_id>/delete')

    return hbp

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides default authentication service based on server
environment. In this case the burden of performing actual authentication is
on the web server used for serving the web interface. The authentication module
then simply uses selected environment variables set up by the server after
successfull authentication.

This module also provides interface for automated user account registration. The
registration form is pre-filled with data gathered again from server environment.
The login may not be changed and the value fetched from environment is always used.
Other account attributes like name or email address may be tweaked by user before
submitting the registration form. Administrator and user are both notified via
email about the fact new account was just created.


Environment variables
--------------------------------------------------------------------------------

Currently following environment variables set up by the HTTP server are supported:

``eppn``,``REMOTE_USER`` (*MANDATORY*)
    The ``eppn`` server variable is set up by the _shibd_ daemon implementing the
    Shibboleth SSO service. The ``REMOTE_USER`` variable is set up by many
    authentication providers. This environment variable is of course mandatory
    and it is used as an account username (login).

``cn``,``givenName``,``sn`` (*OPTIONAL*)
    The ``cn`` server variable is used to fill in user`s name, when available.
    When not available, user`s name is constructed as contatenation of ``givenName``
    and ``sn`` server variables. When none of the above is available, user has to
    input his/her name manually during registration process.

``perunPreferredMail``,``mail`` (*OPTIONAL*)
    The ``perunPreferredMail`` server variable is used to fill in user`s email
    address, when available. When not available, the first email address from
    ``email`` server variable is used. When none of the above is available, user
    has to input his/her email manually during registration process.

``perunOrganizationName``,``o`` (*OPTIONAL*)
    The ``perunOrganizationName`` server variable is used to fill in user`s home
    organization name, when available. When not available, the value of ``o``
    server variable is used. When none of the above is available, user
    has to input his/her home organization name manually during registration process.


Provided endpoints
--------------------------------------------------------------------------------

``/auth_env/login``
    Page providing login functionality via server set environment variables.

    * *Authentication:* no authentication
    * *Methods:* ``GET``

``/auth_env/register``
    User account registration using server set environment variables.

    * *Authentication:* no authentication
    * *Methods:* ``GET``, ``POST``
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask
from flask_babel import gettext

import vial.const
import vial.forms
import vial.db
import vial.blueprints.auth_env
from vial.blueprints.auth_env import BLUEPRINT_NAME, LoginView
from hawat.blueprints.auth_env.forms import RegisterUserAccountForm


class RegistrationException(Exception):
    """
    Exception describing problems with new user account registration.
    """
    def __init__(self, description):
        super().__init__()
        self.description = description

    def __str__(self):
        return str(self.description)


def get_login_from_environment():
    """
    Get user account login from appropriate environment variable(s).
    """
    return flask.request.environ.get(
        'eppn',
        flask.request.environ.get('REMOTE_USER', None)
    )


class RegisterView(vial.blueprints.auth_env.RegisterView):
    """
    View responsible for registering new user account into application.
    """

    def get_user_from_env(self):
        """
        Get user object populated with information gathered from server environment
        variables.
        """
        item = self.dbmodel()

        # Fetch login from server authentication headers (mandatory).
        item.login = get_login_from_environment()
        if not item.login:
            raise RegistrationException(
                gettext("Unable to retrieve account login from your authentication provider.")
            )

        # Try to fetch name from server authentication headers (optional).
        while True:
            try:
                item.fullname = flask.request.environ['cn']
                break
            except (KeyError, AttributeError):
                pass
            try:
                item.fullname = '{} {}'.format(
                    flask.request.environ['givenName'],
                    flask.request.environ['sn']
                )
                break
            except (KeyError, AttributeError):
                pass
            break

        # Try to fetch email from server authentication headers (optional).
        while True:
            try:
                item.email = flask.request.environ['perunPreferredMail']
                break
            except (KeyError, AttributeError):
                pass
            try:
                item.email = flask.request.environ['mail'].split(';')[0]
                break
            except (KeyError, AttributeError):
                pass
            break

        # Try to fetch organization from server authentication headers (optional).
        while True:
            try:
                item.organization = flask.request.environ['perunOrganizationName']
                break
            except (KeyError, AttributeError):
                pass
            try:
                item.organization = flask.request.environ['o']
                break
            except (KeyError, AttributeError):
                pass
            break

        return item

    def get_item(self):
        # Attempt to create user object from server environment variables.
        try:
            return self.get_user_from_env()
        except RegistrationException as exc:
            self.abort(500, exc)

    @staticmethod
    def get_item_form(item):
        locales = list(
            flask.current_app.config['SUPPORTED_LOCALES'].items()
        )

        return RegisterUserAccountForm(
            obj = item,
            choices_locales = locales
        )


#-------------------------------------------------------------------------------


class EnvAuthBlueprint(vial.blueprints.auth_env.EnvAuthBlueprint):
    """Pluggable module - environment authentication service (*auth_env*)."""

    def register_app(self, app):
        app.set_infomailer('auth_env.register', RegisterView.inform_admins)
        app.set_infomailer('auth_env.register', RegisterView.inform_managers)
        app.set_infomailer('auth_env.register', RegisterView.inform_user)


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = EnvAuthBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(LoginView,    '/login')
    hbp.register_view_class(RegisterView, '/register')

    return hbp

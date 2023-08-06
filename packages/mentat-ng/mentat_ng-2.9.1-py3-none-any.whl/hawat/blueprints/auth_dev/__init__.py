#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This Hawat pluggable module provides special authentication method, that is
particularly usable for developers and enables them to impersonate any user.

After enabling this module special authentication endpoint will be available
and will provide simple authentication form with list of all currently available
user accounts. It will be possible for that user to log in as any other user
without entering password.

This module is disabled by default in *production* environment and enabled by
default in *development* environment.

.. warning::

    This module must never ever be enabled on production systems, because it is
    a huge security risk and enables possible access control management violation.
    You have been warned!


Provided endpoints
--------------------------------------------------------------------------------

``/auth_dev/login``
    Page providing special developer login form.

    * *Authentication:* no authentication
    * *Methods:* ``GET``, ``POST``
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask

import vial.const
import vial.forms
import vial.db
import vial.blueprints.auth_dev
from vial.blueprints.auth_dev import BLUEPRINT_NAME, LoginView, DevAuthBlueprint
from hawat.blueprints.auth_dev.forms import RegisterUserAccountForm


class RegisterView(vial.blueprints.auth_dev.RegisterView):
    """
    View responsible for registering new user account into application.
    """

    @staticmethod
    def get_item_form(item):
        roles = list(
            zip(
                flask.current_app.config['ROLES'],
                flask.current_app.config['ROLES']
            )
        )
        locales = list(
            flask.current_app.config['SUPPORTED_LOCALES'].items()
        )

        return RegisterUserAccountForm(
            choices_roles = roles,
            choices_locales = locales
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = DevAuthBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(LoginView,    '/login')
    hbp.register_view_class(RegisterView, '/register')

    return hbp

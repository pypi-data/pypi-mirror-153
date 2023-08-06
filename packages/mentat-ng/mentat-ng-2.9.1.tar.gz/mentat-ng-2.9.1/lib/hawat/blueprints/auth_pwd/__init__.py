#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides classical web login form with password authentication
method.


Provided endpoints
--------------------------------------------------------------------------------

``/auth_pwd/login``
    Page providing classical web login form.

    * *Authentication:* no authentication
    * *Methods:* ``GET``, ``POST``
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask

import vial.const
import vial.forms
import vial.blueprints.auth_pwd
from vial.blueprints.auth_pwd import BLUEPRINT_NAME, LoginView, PwdAuthBlueprint
from hawat.blueprints.auth_pwd.forms import RegisterUserAccountForm



class RegisterView(vial.blueprints.auth_pwd.RegisterView):
    """
    View enabling classical password login.
    """

    @staticmethod
    def get_item_form(item):
        locales = list(
            flask.current_app.config['SUPPORTED_LOCALES'].items()
        )
        return RegisterUserAccountForm(
            choices_locales = locales
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = PwdAuthBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(LoginView,    '/login')
    hbp.register_view_class(RegisterView, '/register')

    return hbp

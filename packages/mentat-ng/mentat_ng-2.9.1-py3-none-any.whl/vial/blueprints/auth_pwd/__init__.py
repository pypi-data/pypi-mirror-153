#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
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


import flask
from flask_babel import lazy_gettext

import vial.const
import vial.forms
from vial.app import VialBlueprint
from vial.view import BaseLoginView, BaseRegisterView
from vial.view.mixin import HTMLMixin, SQLAlchemyMixin

from vial.blueprints.auth_pwd.forms import LoginForm, RegisterUserAccountForm


BLUEPRINT_NAME = 'auth_pwd'
"""Name of the blueprint as module global constant."""


class LoginView(HTMLMixin, SQLAlchemyMixin, BaseLoginView):
    """
    View enabling classical password login.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Password login')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Login (pwd)')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def search_by(self):
        return self.dbmodel.login

    def get_user_login(self):
        form = LoginForm()
        self.response_context.update(
            form = form
        )
        if form.validate_on_submit():
            return form.login.data
        return None

    def authenticate_user(self, user):
        return user.check_password(
            self.response_context['form'].password.data
        )


class RegisterView(HTMLMixin, SQLAlchemyMixin, BaseRegisterView):
    """
    View enabling classical password login.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Register (pwd)')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('User account registration (pwd)')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def search_by(self):
        return self.dbmodel.login

    @staticmethod
    def get_item_form(item):
        locales = list(
            flask.current_app.config['SUPPORTED_LOCALES'].items()
        )
        return RegisterUserAccountForm(
            choices_locales = locales
        )

    def do_before_action(self, item):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        super().do_before_action(item)
        item.set_password(item.password)


#-------------------------------------------------------------------------------


class PwdAuthBlueprint(VialBlueprint):
    """Pluggable module - classical authentication service (*auth_pwd*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Password authentication service')


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

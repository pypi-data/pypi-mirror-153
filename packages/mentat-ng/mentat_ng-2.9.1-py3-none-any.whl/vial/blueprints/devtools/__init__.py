#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides various utility and development tools.
"""


import flask_debugtoolbar
from flask_babel import lazy_gettext

import vial.acl
from vial.app import VialBlueprint
from vial.view import SimpleView
from vial.view.mixin import HTMLMixin


BLUEPRINT_NAME = 'devtools'
"""Name of the blueprint as module global constant."""


class ConfigView(HTMLMixin, SimpleView):
    """
    View for displaying current application configuration and environment.
    """

    authentication = True

    authorization = [vial.acl.PERMISSION_DEVELOPER]

    @classmethod
    def get_view_name(cls):
        return 'config'

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('System configuration')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('View system configuration')


#-------------------------------------------------------------------------------


class DevtoolsBlueprint(VialBlueprint):
    """Pluggable module - development tools (*devtools*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Development tools')

    def register_app(self, app):
        self.developer_toolbar.init_app(app)

        app.menu_main.add_entry(
            'view',
            'developer.devconfig',
            position = 10,
            view = ConfigView
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = DevtoolsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.developer_toolbar = flask_debugtoolbar.DebugToolbarExtension()  # pylint: disable=locally-disabled,attribute-defined-outside-init

    hbp.register_view_class(ConfigView, '/config')

    return hbp

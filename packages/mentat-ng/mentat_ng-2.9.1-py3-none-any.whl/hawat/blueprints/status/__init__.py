#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access Mentat system status information. The
following information is provided:

* current status of all configured real-time message processing modules
* current status of all configured cronjob message post-processing modules


Provided endpoints
------------------

``/status/view``
    Page providing read-only access various Mentat system status characteristics.

    *Authentication:* login required
    *Methods:* ``GET``

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask
from flask_babel import gettext, lazy_gettext

import pyzenkit.jsonconf
import mentat.system
import vial.acl
from vial.app import VialBlueprint
from vial.view import SimpleView
from vial.view.mixin import HTMLMixin


BLUEPRINT_NAME = 'status'
"""Name of the blueprint as module global constant."""


class ViewView(HTMLMixin, SimpleView):
    """
    Application view providing access Mentat system status information.
    """
    authentication = True

    authorization = [vial.acl.PERMISSION_ADMIN]

    @classmethod
    def get_view_name(cls):
        return 'view'

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('System status')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('System status')

    def do_before_response(self, **kwargs):
        try:
            controller_cfg = pyzenkit.jsonconf.json_load(
                flask.current_app.config['MENTAT_CONTROLLER_CFG'],
            )

            self.response_context['mentat_modules'] = mentat.system.make_module_list(
                controller_cfg.get('modules', {})
            )
            self.response_context['mentat_cronjobs'] = mentat.system.make_cronjob_list(
                controller_cfg.get('cronjobs', {})
            )

            self.response_context['mentat_runlogs'] = mentat.system.analyze_runlog_files(
                flask.current_app.config['MENTAT_PATHS']['path_run'],
                limit = 20
            )

            self.response_context['mentat_status'] = mentat.system.system_status(
                self.response_context['mentat_modules'],
                self.response_context['mentat_cronjobs'],
                flask.current_app.config['MENTAT_PATHS']['path_cfg'],
                flask.current_app.config['MENTAT_PATHS']['path_crn'],
                flask.current_app.config['MENTAT_PATHS']['path_log'],
                flask.current_app.config['MENTAT_PATHS']['path_run']
            )

        except FileNotFoundError:
            self.flash(
                gettext("Error when displaying system status, encountered file not found error.")
            )
            #flask.current_app.log_exception_with_label(
            #    traceback.TracebackException(*sys.exc_info()),
            #    "Error when displaying system performance"
            #)


#-------------------------------------------------------------------------------


class StatusBlueprint(VialBlueprint):
    """Pluggable module - Mentat system status (*status*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Mentat system status')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 20,
            group = lazy_gettext('Status overview'),
            view = ViewView
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = StatusBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ViewView, '/view')

    return hbp

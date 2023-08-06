#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module is a highly commented skeleton and an example implementation.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import flask_login
from flask_babel import lazy_gettext

from vial.app import VialBlueprint
from vial.view import SimpleView
from vial.view.mixin import HTMLMixin


BLUEPRINT_NAME = 'skeleton'
"""Name of the blueprint as module global constant."""


class ExampleView(HTMLMixin, SimpleView):
    """
    Example simple view.
    """
    decorators = [flask_login.login_required]
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return 'example'

    @classmethod
    def get_view_icon(cls):
        return 'example'

    @classmethod
    def get_menu_title(cls, **kwargs):
        return 'Example view'

    @classmethod
    def get_view_title(cls, **kwargs):
        return 'Example view'

    @classmethod
    def get_view_template(cls):
        return '{}/example.html'.format(BLUEPRINT_NAME)

    def do_before_response(self, **kwargs):
        pass


#-------------------------------------------------------------------------------


class SkeletonBlueprint(VialBlueprint):
    """Pluggable module - skeleton (*skeleton*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Skeleton module')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'more.{}'.format(BLUEPRINT_NAME),
            position = 1000,
            view = ExampleView
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = SkeletonBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ExampleView, '/example')

    return hbp

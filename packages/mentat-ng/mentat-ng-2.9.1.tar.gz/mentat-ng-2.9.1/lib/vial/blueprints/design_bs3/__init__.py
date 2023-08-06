#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides default application desing and style. Currently
there are no views provided by this module.


.. note::

    To completely change the design of the whole application you can implement
    your own custom _design_ module and replace this one. However this requires
    that you thoroughly study the design of this module and provide your own
    implementation for all API hooks, otherwise you may break the whole application.


Module content
--------------

#. Base Jinja2 template providing application layout.
#. Common macros for Jinja2 templates.
#. Common forms (delete, disable, enable).
#. HTML error pages (400, 403, 404, 410, 500).
#. Various images
#. Application CSS styles
#. Application Javascripts

"""


from flask_babel import lazy_gettext

from vial.app import VialBlueprint


#
# Name of the blueprint as module global constant.
#
BLUEPRINT_NAME = 'design'


#-------------------------------------------------------------------------------


class DesignBlueprint(VialBlueprint):
    """Pluggable module - application design and style (*design*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Application design and style template')

#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = DesignBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        static_folder = 'static',
        static_url_path = '/static/design')

    return hbp

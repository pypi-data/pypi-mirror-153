#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
This pluggable module provides default home page.


Provided endpoints
------------------

``/``
    Page providing home page.

    * *Authentication:* no authentication
    * *Methods:* ``GET``
"""


from flask_babel import lazy_gettext

from vial.app import VialBlueprint
from vial.view import SimpleView
from vial.view.mixin import HTMLMixin


BLUEPRINT_NAME = 'home'
"""Name of the blueprint as module global constant."""


class IndexView(HTMLMixin, SimpleView):
    """
    View presenting home page.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'index'

    @classmethod
    def get_view_icon(cls):
        return 'module-home'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Welcome!')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Home')


#-------------------------------------------------------------------------------


class HomeBlueprint(VialBlueprint):
    """Pluggable module - home page (*home*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Home page')


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = HomeBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(IndexView, '/')

    return hbp

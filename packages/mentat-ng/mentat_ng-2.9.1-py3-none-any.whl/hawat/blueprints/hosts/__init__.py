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
related to real time dashboard calculations for `IDEA <https://idea.cesnet.cz/en/index>`__
events. This module is currently experimental, because the searching and statistical
calculations can be very performance demanding.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import datetime
import pytz

import flask
from flask_babel import lazy_gettext

import mentat.stats.idea
import mentat.services.eventstorage
from mentat.const import tr_

import hawat.events
import vial.const
import vial.acl
from vial.app import VialBlueprint
from vial.view import BaseSearchView
from vial.view.mixin import HTMLMixin, AJAXMixin
from vial.utils import URLParamsBuilder
from hawat.base import PsycopgMixin
from hawat.blueprints.hosts.forms import SimpleHostSearchForm


BLUEPRINT_NAME = 'hosts'
"""Name of the blueprint as module global constant."""


class AbstractSearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching...
    """
    authentication = True

    authorization = [vial.acl.PERMISSION_DEVELOPER]

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Hosts')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search hosts')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @staticmethod
    def get_search_form(request_args):
        return SimpleHostSearchForm(
            request_args,
            meta = {'csrf': False}
        )

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating host statistics from %d records.",
            len(items)
        )
        if items:
            dt_from = self.response_context['form_data'].get('dt_from', None)
            if dt_from:
                dt_from = dt_from.astimezone(pytz.utc)
                dt_from = dt_from.replace(tzinfo = None)
            dt_to   = self.response_context['form_data'].get('dt_to', None)
            if dt_to:
                dt_to = dt_to.astimezone(pytz.utc)
                dt_to = dt_to.replace(tzinfo = None)

            if not dt_from and items:
                dt_from = self.get_db().search_column_with('detecttime')
            if not dt_to and items:
                dt_to = datetime.datetime.utcnow()

            self.response_context.update(
                statistics = mentat.stats.idea.evaluate_singlehost_events(
                    self.response_context['form_data'].get('host_addr'),
                    items,
                    dt_from = dt_from,
                    dt_to = dt_to,
                    max_count = flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS']
                )
            )
            self.response_context.pop('items', None)

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )

    @staticmethod
    def get_event_factory():
        return mentat.services.eventstorage.record_to_idea_ghost

    @staticmethod
    def get_event_columns():
        columns = list(mentat.services.eventstorage.EVENTS_COLUMNS)
        columns.remove('event')
        return columns


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_breadcrumbs_menu(cls):
        breadcrumbs_menu = vial.menu.Menu()
        breadcrumbs_menu.add_entry(
            'endpoint',
            'home',
            endpoint = flask.current_app.config['ENDPOINT_HOME']
        )
        breadcrumbs_menu.add_entry(
            'endpoint',
            'search',
            endpoint = '{}.search'.format(cls.module_name)
        )
        return breadcrumbs_menu


class APISearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'apisearch'


#-------------------------------------------------------------------------------


class HostsBlueprint(VialBlueprint):
    """Pluggable module - Host overview (*hosts*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Host overview')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'developer.{}'.format(BLUEPRINT_NAME),
            position = 80,
            view = SearchView
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> in host overview'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('host_addr').add_kwrule('dt_from', False, True).add_kwrule('dt_to', False, True)
        )

#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = HostsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(SearchView,    '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView, '/api/{}/search'.format(BLUEPRINT_NAME))

    return hbp

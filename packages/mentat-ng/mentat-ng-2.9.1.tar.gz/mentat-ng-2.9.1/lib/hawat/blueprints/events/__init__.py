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
related to `IDEA <https://idea.cesnet.cz/en/index>`__ events, database searching,
viewing event details and producing event dashboards.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import datetime

import flask
from flask_babel import lazy_gettext

import mentat.stats.idea
import mentat.services.eventstorage
from mentat.datatype.sqldb import EventStatisticsModel
from mentat.const import tr_

import hawat.const
import hawat.events
import vial.const
import vial.acl
from vial.app import VialBlueprint
from vial.view import BaseView, SimpleView, BaseSearchView, ItemShowView
from vial.view.mixin import HTMLMixin, AJAXMixin, SQLAlchemyMixin
from vial.utils import URLParamsBuilder
from hawat.base import PsycopgMixin
from hawat.blueprints.events.forms import SimpleEventSearchForm, EventDashboardForm


BLUEPRINT_NAME = 'events'
"""Name of the blueprint as module global constant."""


def _get_search_form(request_args = None):
    choices = hawat.events.get_event_form_choices()

    form = SimpleEventSearchForm(
        request_args,
        meta = {'csrf': False},
        choices_source_types    = choices['source_types'],
        choices_target_types    = choices['target_types'],
        choices_host_types      = choices['host_types'],
        choices_detectors       = choices['detectors'],
        choices_detector_types  = choices['detector_types'],
        choices_categories      = choices['categories'],
        choices_severities      = choices['severities'],
        choices_classes         = choices['classes'],
        choices_protocols       = choices['protocols'],
        choices_inspection_errs = choices['inspection_errs'],
    )

    # In case no time bounds were set adjust them manually.
    if request_args and not ('dt_from' in request_args or 'dt_to' in request_args or 'st_from' in request_args or 'st_to' in request_args):
        form.dt_from.process_data(vial.forms.default_dt_with_delta())
        form.dt_to.process_data(vial.forms.default_dt())

    return form


class AbstractSearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for all views responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database.
    """
    authentication = True

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event database')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Events')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        form_data['groups'] = [item.name for item in form_data['groups']]

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for searching the `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of HTML page.
    """
    methods = ['GET']

    has_help = True

    @staticmethod
    def get_qtype():
        """
        Get type of the event select query.
        """
        return mentat.services.eventstorage.QTYPE_SELECT_GHOST

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

    @classmethod
    def get_context_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'events.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint = 'events.download',
            hidetitle = True
        )
        return action_menu


class APISearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for searching the `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'apisearch'


class AbstractShowView(PsycopgMixin, ItemShowView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class responsible for fetching and presenting single `IDEA <https://idea.cesnet.cz/en/index>`__
    event.
    """
    authentication = True

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show event')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Show')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'View details of event &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].get_id())
        )


class ShowView(HTMLMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ event view that presents
    the result as HTML page.
    """
    methods = ['GET']

    has_help = True

    @classmethod
    def get_action_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint = 'events.download'
        )
        return action_menu


class APIShowView(AJAXMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ event view that presents
    the result as HTML page.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'apishow'


class DownloadView(PsycopgMixin, BaseView):
    """
    Download `IDEA <https://idea.cesnet.cz/en/index>`__ event as JSON file.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'download'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Download event')

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(
            cls.get_view_endpoint(),
            item_id = kwargs['item'].get_id()
        )

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Download')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Download event &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].get_id())
        )

    #---------------------------------------------------------------------------

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.

        Single item with given unique identifier will be retrieved from database
        and injected into template to be displayed to the user.
        """
        item = self.fetch(item_id)
        if not item:
            flask.abort(404)

        self.logger.debug(
            "Event %s is being downloaded as a standalone file.",
            item['ID']
        )

        response = flask.make_response(
            item.to_json(indent = 4, sort_keys = True)
        )
        response.mimetype = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename={}.idea.json'.format(item_id)
        return response


class AbstractDashboardView(SQLAlchemyMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard.
    """
    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Events')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Overall event dashboards')

    @classmethod
    def get_view_template(cls):
        return '{}/{}.html'.format(cls.module_name, cls.get_view_name())

    #---------------------------------------------------------------------------

    @property
    def dbmodel(self):
        return EventStatisticsModel

    @staticmethod
    def get_search_form(request_args):
        return EventDashboardForm(request_args, meta = {'csrf': False})

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.dt_from >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.dt_to <= form_args['dt_to'])

        # Return the result sorted by interval.
        return query.order_by(model.interval)

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating event dashboard overview from %d records.",
            len(items)
        )
        if items:
            dt_from = self.response_context['form_data'].get('dt_from', None)
            if dt_from:
                dt_from = dt_from.replace(tzinfo = None)
            dt_to   = self.response_context['form_data'].get('dt_to', None)
            if dt_to:
                dt_to = dt_to.replace(tzinfo = None)

            if not dt_from:
                dt_from = self.dbcolumn_min(self.dbmodel.createtime)
            if not dt_to:
                dt_to = datetime.datetime.utcnow()

            self.response_context.update(
                statistics = mentat.stats.idea.aggregate_timeline_groups(
                    items,
                    dt_from = dt_from,
                    dt_to = dt_to,
                    max_count = flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS'],
                    min_step = 300
                )
            )

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )


class DashboardView(HTMLMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return 'dashboard'


class APIDashboardView(AJAXMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of JSON document.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'apidashboard'

    def process_response_context(self):
        super().process_response_context()
        # Prevent certain response context keys to appear in final response.
        for key in ('items', 'quicksearch_list'):
            try:
                del self.response_context[key]
            except KeyError:
                pass
        return self.response_context


class APIMetadataView(AJAXMixin, SimpleView):
    """
    Application view providing access event metadata information.
    """
    authentication = True

    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'metadata'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Event metadata')

    def do_before_response(self, **kwargs):
        self.response_context.update(**hawat.events.get_event_enums())


#-------------------------------------------------------------------------------


class EventsBlueprint(VialBlueprint):
    """Pluggable module - `IDEA <https://idea.cesnet.cz/en/index>`__ event database (*events*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('<a href="https://idea.cesnet.cz/en/index">IDEA</a> event database')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'dashboards.{}'.format(BLUEPRINT_NAME),
            position = 10,
            view = DashboardView
        )
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position = 140,
            view = SearchView,
            resptitle = True
        )

        def _get_upb():
            return URLParamsBuilder(
                {'submit': tr_('Search')}
            ).add_kwrule(
                'dt_from', False, True
            ).add_kwrule(
                'dt_to', False, True
            )

        # Register context search actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('Search for abuse group <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('groups', True)
        )

        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_addrs', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for target <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_addrs', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for host <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_addrs', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_CATEGORY,
            tr_('Search for category <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('categories', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_CLASS,
            tr_('Search for class <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('classes', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_DETECTOR,
            tr_('Search for detector <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('detectors', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_DETTYPE,
            tr_('Search for detector type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('detector_types', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for source type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_types', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for target type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_types', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for host type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_types', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for source port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_ports', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for target port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_ports', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for host port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_ports', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_PROTOCOL,
            tr_('Search for protocol <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('protocols', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_SEVERITY,
            tr_('Search for severity <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('severities', True).add_kwrule('groups', True, True)
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = EventsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        static_folder   = 'static',
        static_url_path = '/{}/static'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(SearchView,       '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(ShowView,         '/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DownloadView,     '/{}/<item_id>/download'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DashboardView,    '/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView,    '/api/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIShowView,      '/api/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIDashboardView, '/api/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIMetadataView,  '/api/{}/metadata'.format(BLUEPRINT_NAME))

    return hbp

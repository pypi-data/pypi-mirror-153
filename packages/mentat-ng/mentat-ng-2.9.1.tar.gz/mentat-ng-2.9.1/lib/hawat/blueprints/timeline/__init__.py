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
related to `IDEA <https://idea.cesnet.cz/en/index>`__ event timeline based
visualisations.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import copy
import datetime
import pytz

import flask
from flask_babel import lazy_gettext

import mentat.stats.idea
import mentat.services.eventstorage
from mentat.const import tr_
from mentat.services.eventstorage import QTYPE_TIMELINE

import hawat.events
import vial.const
import vial.acl
from vial.app import VialBlueprint
from vial.view import BaseSearchView, CustomSearchView
from vial.view.mixin import HTMLMixin, AJAXMixin
from vial.utils import URLParamsBuilder
from hawat.base import PsycopgMixin
from hawat.blueprints.timeline.forms import SimpleTimelineSearchForm


BLUEPRINT_NAME = 'timeline'
"""Name of the blueprint as module global constant."""

AGGREGATIONS = (
    (mentat.stats.idea.ST_SKEY_CATEGORIES,  {}, {"aggr_set": "category"}),
    (mentat.stats.idea.ST_SKEY_IPS,         {}, {"aggr_set": "source_ip"}),
    #('', {"aggr_set": "target_ip"}),
    (mentat.stats.idea.ST_SKEY_SRCPORTS,    {}, {"aggr_set": "source_port"}),
    (mentat.stats.idea.ST_SKEY_TGTPORTS,    {}, {"aggr_set": "target_port"}),
    (mentat.stats.idea.ST_SKEY_SRCTYPES,    {}, {"aggr_set": "source_type"}),
    (mentat.stats.idea.ST_SKEY_TGTTYPES,    {}, {"aggr_set": "target_type"}),
    (mentat.stats.idea.ST_SKEY_PROTOCOLS,   {}, {"aggr_set": "protocol"}),
    (mentat.stats.idea.ST_SKEY_DETECTORS,   {}, {"aggr_set": "node_name"}),
    (mentat.stats.idea.ST_SKEY_DETECTORTPS, {}, {"aggr_set": "node_type"}),
    (mentat.stats.idea.ST_SKEY_ABUSES,      {}, {"aggr_set": "resolvedabuses"}),
    (mentat.stats.idea.ST_SKEY_CLASSES,     {}, {"aggr_set": "eventclass"}),
    (mentat.stats.idea.ST_SKEY_SEVERITIES,  {}, {"aggr_set": "eventseverity"}),
)


def _get_search_form(request_args = None):
    choices = hawat.events.get_event_form_choices()
    aggrchc = list(
        zip(
            map(lambda x: x[0], AGGREGATIONS),
            map(lambda x: x[0], AGGREGATIONS)
        )
    )

    form = SimpleTimelineSearchForm(
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
        choices_aggregations    = aggrchc
    )

    # In case no time bounds were set adjust them manually.
    if request_args and not ('dt_from' in request_args or 'dt_to' in request_args or 'st_from' in request_args or 'st_to' in request_args):
        form.dt_from.process_data(vial.forms.default_dt_with_delta())
        form.dt_to.process_data(vial.forms.default_dt())

    return form


class AbstractSearchView(PsycopgMixin, CustomSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in timeline-based manner.
    """
    authentication = True

    url_params_unsupported = ('page', 'sortby')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event timeline')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Timeline')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        self.response_context.update(
            sqlqueries = []
        )

        form_data['groups'] = [item.name for item in form_data['groups']]

        # Timestamp timezone mangling magic. Convert everything to UTC naive.
        dt_from = form_data.get('dt_from', None)
        if dt_from:
            dt_from = dt_from.astimezone(pytz.utc)
            dt_from = dt_from.replace(tzinfo = None)
        dt_to   = form_data.get('dt_to', None)
        if dt_to:
            dt_to = dt_to.astimezone(pytz.utc)
            dt_to = dt_to.replace(tzinfo = None)
        else:
            dt_to = datetime.datetime.utcnow()
        form_data['dt_from'] = dt_from
        form_data['dt_to'] = dt_to

        # Determine configurations for timelines.
        timeline_cfg = mentat.stats.idea.calculate_timeline_config(
            form_data['dt_from'],
            form_data['dt_to'],
            flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS']
        )
        bucket_list = self.get_db().query_direct(
            'SELECT generate_series(%s, %s, %s) AS bucket ORDER BY bucket',
            None,
            [
                timeline_cfg['dt_from'],
                timeline_cfg['dt_to'],
                timeline_cfg['step']
            ]
        )
        timeline_cfg['buckets'] = [x[0] for x in bucket_list]
        self.response_context['sqlqueries'].append(
            self.get_db().cursor.lastquery.decode('utf-8')
        )
        self.response_context.update(
            timeline_cfg = timeline_cfg
        )

        # Put calculated parameters together with other search form parameters.
        form_data['dt_from'] = timeline_cfg['dt_from']
        form_data['dt_to']   = timeline_cfg['dt_to']
        form_data['step']    = timeline_cfg['step']

    def _search_events_aggr(self, form_args, qtype, aggr_name, enable_toplist = True):
        self.mark_time(
            '{}_{}'.format(qtype, aggr_name),
            'begin',
            tag = 'search',
            label = 'Begin aggregation calculations "{}:{}"'.format(
                qtype,
                aggr_name
            ),
            log = True
        )
        search_result = self.get_db().search_events_aggr(
            form_args,
            qtype = qtype,
            dbtoplist = enable_toplist
        )
        self.mark_time(
            '{}_{}'.format(qtype, aggr_name),
            'end',
            tag = 'search',
            label = 'Finished aggregation calculations "{}:{}" [yield {} row(s)]'.format(
                qtype,
                aggr_name,
                len(search_result)
            ),
            log = True
        )

        self.response_context['sqlqueries'].append(
            self.get_db().cursor.lastquery.decode('utf-8')
        )
        self.response_context['search_result']["{}:{}".format(qtype, aggr_name)] = search_result

    def custom_search(self, form_args):
        self.response_context.update(
            search_result = {},  # Raw database query results (rows).
            aggregations = []    # Note all performed aggregations for further processing.
        )

        # Always perform total event count timeline calculations.
        fargs = copy.deepcopy(form_args)
        fargs.update({"aggr_set": None})
        self._search_events_aggr(
            fargs,
            QTYPE_TIMELINE,
            mentat.stats.idea.ST_SKEY_CNT_EVENTS,
            False
        )

        # Perform only timeline aggregations for the rest of selected aggragtions, aggregation
        # aggregations will be computed from timelines later.
        qtype = QTYPE_TIMELINE
        for aggr_name, _, faupdates in AGGREGATIONS:
            if 'aggregations' in form_args and form_args['aggregations'] and aggr_name not in form_args['aggregations']:
                self.logger.debug(
                    "Skipping aggregation search {}:{}.".format(qtype, aggr_name)
                )
            else:
                fargs = copy.deepcopy(form_args)
                fargs.update(faupdates)
                self._search_events_aggr(fargs, qtype, aggr_name)
                self.response_context['aggregations'].append(aggr_name)


    def do_after_search(self):
        self.response_context.update(
            statistics = {
                'timeline_cfg': self.response_context['timeline_cfg']
            }
        )

        # Convert raw database rows into dataset structures.
        self.mark_time(
            'result_convert',
            'begin',
            tag = 'calculate',
            label = 'Converting result from database rows to statistical dataset',
            log = True
        )
        key = "{}:{}".format(QTYPE_TIMELINE, mentat.stats.idea.ST_SKEY_CNT_EVENTS)
        mentat.stats.idea.aggregate_dbstats_events(
            QTYPE_TIMELINE,
            mentat.stats.idea.ST_SKEY_CNT_EVENTS,
            self.response_context['search_result'][key],
            0,
            self.response_context['timeline_cfg'],
            self.response_context['statistics']
        )
        for aggr_name, default_val, _ in AGGREGATIONS:
            key = "{}:{}".format(QTYPE_TIMELINE, aggr_name)
            if key in self.response_context['search_result']:
                mentat.stats.idea.aggregate_dbstats_events(
                    QTYPE_TIMELINE,
                    aggr_name,
                    self.response_context['search_result'][key],
                    default_val,
                    self.response_context['timeline_cfg'],
                    self.response_context['statistics']
                )
        self.mark_time(
            'result_convert',
            'end',
            tag = 'calculate',
            label = 'Done converting result from database rows to statistical dataset',
            log = True
        )

        # Calculate aggregation aggregations from timeline aggregations.
        aggr_name = mentat.stats.idea.ST_SKEY_CNT_EVENTS
        self.mark_time(
            'result_calculate',
            'begin',
            tag = 'calculate',
            label = 'Calculating aggregation aggregations from timeline aggregations',
            log = True
        )
        mentat.stats.idea.postcalculate_dbstats_events(
            aggr_name,
            self.response_context['statistics']
        )
        for aggr_name, default_val, _ in AGGREGATIONS:
            if aggr_name in self.response_context['aggregations']:
                mentat.stats.idea.postcalculate_dbstats_events(
                    aggr_name,
                    self.response_context['statistics']
                )
        self.mark_time(
            'result_calculate',
            'end',
            tag = 'calculate',
            label = 'Done calculating aggregation aggregations from timeline aggregations',
            log = True
        )

        # Truncate all datasets
        self.mark_time(
            'result_truncate',
            'begin',
            tag = 'calculate',
            label = 'Truncating datasets',
            log = True
        )
        self.response_context['statistics'] = mentat.stats.idea.evaluate_dbstats_events(
            self.response_context['statistics']
        )
        self.mark_time(
            'result_truncate',
            'end',
            tag = 'calculate',
            label = 'Done truncating datasets',
            log = True
        )

        self.response_context.update(
            items_count = self.response_context['statistics'].get('cnt_events', 0)
        )
        self.response_context.pop('search_result', None)

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )


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


class AbstractLegacySearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in timeline-based manner.
    """
    authentication = True

    url_params_unsupported = ('page', 'limit', 'sortby')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event timeline')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Timeline')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        form_data['groups'] = [item.name for item in form_data['groups']]

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating IDEA event timeline from %d records.",
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
                statistics = mentat.stats.idea.evaluate_timeline_events(
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
    def get_qtype():
        """
        Get type of the event select query.
        """
        return mentat.services.eventstorage.QTYPE_SELECT_GHOST

class APILegacySearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.

    *Deprecated legacy implementation, kept only for the purposes of comparison.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        return 'apilegacysearch'


#-------------------------------------------------------------------------------


class TimelineBlueprint(VialBlueprint):
    """Pluggable module - IDEA event timelines (*timeline*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('<a href="https://idea.cesnet.cz/en/index">IDEA</a> event timelines')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position = 150,
            view = SearchView,
            resptitle = True
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> on IDEA event timeline'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('source_addrs', True).add_kwrule('dt_from', False, True).add_kwrule('dt_to', False, True)
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = TimelineBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(SearchView,          '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView,       '/api/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APILegacySearchView, '/api/{}/legacysearch'.format(BLUEPRINT_NAME))

    return hbp

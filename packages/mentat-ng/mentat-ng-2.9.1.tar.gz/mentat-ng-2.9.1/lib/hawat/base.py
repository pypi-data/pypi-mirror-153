#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import re
import datetime

#
# Flask related modules.
#
import flask
import flask.app
import flask.views
import flask_login
from flask_babel import gettext

#
# Custom modules.
#
import vial.app
import vial.const
import vial.menu
import vial.errors
import hawat.events

import mentat
import mentat._buildmeta
import mentat.const
import mentat.services.sqlstorage
import mentat.services.eventstorage
import mentat.idea.internal
import mentat.idea.jsondict
import mentat.datatype.sqldb


CRE_QNAME = re.compile(r'^([\d]+)_([a-z]{6})$')
RE_UQUERY = ' AS "_mentatq\\({:d}_[^)]+\\)_"'


class HawatApp(vial.app.Vial):
    """
    Custom implementation of :py:class:`flask.Flask` class. This class extends the
    capabilities of the base class with following additional features:

    Configuration based blueprint registration
        The application configuration file contains a directive describing list
        of requested blueprints/modules, that should be registered into the
        application. This enables administrator to very easily fine tune the
        application setup for each installation. See the :py:func:`hawat.base.HawatApp.register_blueprints`
        for more information on the topic.

    Application main menu management
        The application provides three distinct menus, that are at a disposal for
        blueprint/module designer.

    Mentat config access
        The application provides access to Mentat`s core configurations.
    """

    def __init__(self, import_name, **kwargs):
        super().__init__(import_name, **kwargs)

        self.csag = {}
        self.oads = {}

    @property
    def mconfig(self):
        """
        Return Mentat specific configuration sub-dictionary.
        """
        return self.config[hawat.const.CFGKEY_MENTAT_CORE]

    def get_csag(self, group_name):
        """
        Return list of all registered context search actions for given group name
        (CSAG: Context Search Action Group).

        :param str group_name: Name of the group.
        :return: List of all registered context search actions.
        :rtype: list
        """
        return self.csag.get(group_name, [])

    def set_csag(self, group_name, title, view_class, params_builder):
        """
        Store new context search action for given group name (CSAG: Context Search
        Action Group).

        :param str group_name: Name of the group.
        :param str title: Title for the search action.
        :param class view_class: Associated view class.
        :param URLParamsBuilder params_builder: URL parameter builder for this action.
        """
        self.csag.setdefault(group_name, []).append({
            'title':  title,
            'view':   view_class,
            'params': params_builder
        })

    def set_csag_url(self, group_name, title, icon, url_builder):
        """
        Store new URL based context search action for given group name (CSAG: Context
        Search Action Group).

        :param str group_name: Name of the group.
        :param str title: Title for the search action.
        :param str icon: Icon for the search action.
        :param func url_builder: URL builder for this action.
        """
        self.csag.setdefault(group_name, []).append({
            'title': title,
            'icon':  icon,
            'url':   url_builder
        })

    def get_oads(self, group_name):
        """
        Return list of all registered object additional data services for given
        object group name (OADS: Additional Object Data Service).

        :param str group_name: Name of the group.
        :return: List of all object additional data services.
        :rtype: list
        """
        return self.oads.get(group_name, [])

    def set_oads(self, group_name, view_class, params_builder):
        """
        Store new object additional data services for given object group name
        (OADS: Additional Object Data Service).

        :param str group_name: Name of the group.
        :param class view_class: Associated view class.
        :param URLParamsBuilder params_builder: URL parameter builder for this action.
        """
        self.oads.setdefault(group_name, []).append({
            'view':     view_class,
            'params':   params_builder
        })


    #--------------------------------------------------------------------------


    def setup_app(self):
        super().setup_app()

        self._setup_app_eventdb()


    def _setup_app_core(self):
        super()._setup_app_core()

        @self.context_processor
        def jinja_inject_variables():  # pylint: disable=locally-disabled,unused-variable
            """
            Inject additional variables into Jinja2 global template namespace.
            """
            return dict(
                hawat_version       = mentat.__version__,
                hawat_bversion      = mentat._buildmeta.__bversion__,  # pylint: disable=locally-disabled,protected-access
                hawat_bversion_full = mentat._buildmeta.__bversion_full__,  # pylint: disable=locally-disabled,protected-access
                hawat_chart_dimensions  = 'height:700px',
            )

        @self.context_processor
        def jinja2_inject_functions():  # pylint: disable=locally-disabled,unused-variable,too-many-locals

            def get_csag(group):
                """
                Return list of all registered context search actions under given group.

                :param str group: Name of the group.
                :return: List of all registered context search actions.
                :rtype: list
                """
                return self.get_csag(group)

            def get_reporting_interval_name(seconds):
                """
                Get a name of reporting interval for given time delta.

                :param int seconds: Time interval delta in seconds.
                :return: Name of the reporting interval.
                :rtype: str
                """
                return mentat.const.REPORTING_INTERVALS_INV[seconds]

            def get_limit_counter(limit = None):
                """
                Get fresh instance of limit counter.
                """
                if not limit:
                    limit = flask.current_app.config['HAWAT_LIMIT_AODS']
                return vial.utils.LimitCounter(limit)

            return dict(
                get_csag                    = get_csag,
                get_reporting_interval_name = get_reporting_interval_name,
                get_limit_counter           = get_limit_counter,
            )

        class HawatJSONEncoder(flask.json.JSONEncoder):
            """
            Custom JSON encoder for converting anything into JSON strings.
            """
            def default(self, obj):  # pylint: disable=locally-disabled,method-hidden,arguments-differ
                try:
                    if isinstance(obj, mentat.idea.internal.Idea):
                        return mentat.idea.jsondict.Idea(obj).data
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                try:
                    if isinstance(obj, datetime.datetime):
                        return obj.isoformat() + 'Z'
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                try:
                    return obj.to_dict()
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                try:
                    return str(obj)
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                return flask.json.JSONEncoder.default(self, obj)

        self.json_encoder = HawatJSONEncoder

        return self

    def _setup_app_db(self):
        super()._setup_app_db()

        class StorageService:  # pylint: disable=locally-disabled,too-few-public-methods
            """
            This is a thin proxy class, that can be used in place of :py:class:`mentat.services.sqlstorage.StorageService`.
            This is necessary for certain services like :py:mod:`mentat.services.whois`, that require
            some access to database storage service and are hardcoded to use :py:class:`mentat.services.sqlstorage.StorageService`.
            This is necessary when using the services from Flask framework, because there
            is another storage service management feature in place using the py:mod:`flask_sqlalchemy`
            module.
            """
            @property
            def session(self):
                """
                Thin proxy property for retrieving reference to current database session.
                """
                return vial.db.db_session()


        class StorageServiceManager:  # pylint: disable=locally-disabled,too-few-public-methods
            """
            This is a thin proxy class, that can be used in place of :py:class:`mentat.services.sqlstorage.StorageServiceManager`.
            This is necessary for certain services like :py:mod:`mentat.services.whois`, that require
            some access to database storage service manager and are hardcoded to use :py:class:`mentat.services.sqlstorage.StorageServiceManager`.
            This is necessary when using the services from Flask framework, because there
            is another storage service management feature in place using the py:mod:`flask_sqlalchemy`
            module.
            """
            @staticmethod
            def service():
                """
                Thin proxy property for retrieving reference to current database storage
                service.
                """
                return StorageService()


        mentat.services.sqlstorage.set_manager(StorageServiceManager())

    def _setup_app_eventdb(self):
        """
        Setup application database service for given Vial application.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        hawat.events.db_init(self)
        self.logger.info("Connected to event database")

        return self


class PsycopgMixin:
    """
    Mixin class providing generic interface for interacting with SQL database
    backend through SQLAlchemy library.
    """
    SEARCH_QUERY_QUOTA_CHECK = True

    def fetch(self, item_id):  # pylint: disable=locally-disabled,no-self-use
        """
        Fetch item with given primary identifier from the database.
        """
        return hawat.events.db_get().fetch_event(item_id)

    @staticmethod
    def get_db():
        """
        Get database connection service.

        :return: database connection service.
        :rtype: mentat.services.eventstorage.EventStorageService
        """
        return hawat.events.db_get()

    @staticmethod
    def get_qtype():
        """
        Get type of the event select query.
        """
        return mentat.services.eventstorage.QTYPE_SELECT

    @staticmethod
    def get_qname():
        """
        Get unique name for the event select query.
        """
        return '{}_{}'.format(
            flask_login.current_user.get_id(),
            mentat.const.random_str(6)
        )

    @staticmethod
    def parse_qname(qname):
        """
        Get unique name for the event select query.
        """
        match = CRE_QNAME.match(qname)
        if match is None:
            return None, None
        return match.group(1), match.group(2)

    def _check_search_query_quota(self):
        limit = flask.current_app.config['HAWAT_SEARCH_QUERY_QUOTA']
        qlist = hawat.events.db_get().queries_status(
            RE_UQUERY.format(
                int(flask_login.current_user.get_id())
            )
        )
        if len(qlist) >= limit:
            self.abort(
                400,
                gettext(
                    "You have reached your event search query quota: %(limit)s queries. Please wait for your queries to finish and try again. You may also review all your <a href=\"%(url)s\">currently running queries</a>.",
                    limit = limit,
                    url = flask.url_for('dbstatus.queries_my')
                )
            )

    def search(self, form_args):
        """
        Perform actual search of IDEA events using provided query arguments.

        :param dict form_args: Search query arguments.
        :return: Tuple containing number of items as integer and list of searched items.
        :rtype: tuple
        """
        if self.SEARCH_QUERY_QUOTA_CHECK:
            self._check_search_query_quota()

        query_name = self.get_qname()
        items_count_total, items = self.get_db().search_events(
            form_args,
            qtype = self.get_qtype(),
            qname = query_name
        )
        self.response_context.update(
            sqlquery = self.get_db().cursor.lastquery.decode('utf-8'),
            sqlquery_name = query_name
        )
        return items

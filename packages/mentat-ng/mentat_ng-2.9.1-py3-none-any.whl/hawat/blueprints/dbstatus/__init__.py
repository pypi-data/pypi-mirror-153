#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access to database status information. The
following information is provided:

* general statistics of event database:

  * general statistics of *events* table

    * estimated number of records
    * table size, index size, tablespace size and total size
    * oldest and youngest record timestamp, record timespan

  * general statistics of *event_thresholds* table

    * estimated number of records
    * table size, index size, tablespace size and total size
    * oldest and youngest record timestamp, record timespan

  * general statistics of *thresholds* table

    * estimated number of records
    * table size, index size, tablespace size and total size
    * oldest and youngest record timestamp, record timespan

* PostgreSQL configurations


Provided endpoints
------------------

``/dbstatus/view``
    Page providing read-only access various database status characteristics.

    *Authentication:* login required
    *Authorization:* ``admin`` role only
    *Methods:* ``GET``

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sys
import datetime
import traceback

import werkzeug.routing
import flask
import flask_login
from flask_babel import gettext, lazy_gettext
from sqlalchemy import or_

import mentat.const
import mentat.system
from mentat.datatype.sqldb import UserModel, GroupModel, FilterModel, SettingsReportingModel

import vial.menu
import vial.acl
from vial.app import VialBlueprint
from vial.view import RenderableView, SimpleView
from vial.view.mixin import HTMLMixin, AJAXMixin, SQLAlchemyMixin
from vial.forms import ItemActionConfirmForm
from hawat.base import PsycopgMixin
from hawat.base import RE_UQUERY


BLUEPRINT_NAME = 'dbstatus'
"""Name of the blueprint as module global constant."""


class ViewView(HTMLMixin, PsycopgMixin, SimpleView):
    """
    Application view providing access event database status information.
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
        return lazy_gettext('Database status')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Database status')

    def _enrich_result_queries(self, result):
        """
        Enrich query status result with information about the user running the query.
        """
        cache = {}
        for record in result:
            if 'query_name' not in record:
                continue
            user_id, query_id = self.parse_qname(record['query_name'])
            record['user_id'] = user_id
            record['query_id'] = query_id
            if user_id not in cache:
                cache[user_id] = vial.db.db_get().session.query(UserModel).filter(UserModel.id == int(user_id)).one_or_none()
            record['user'] = cache[user_id]
        return result

    def do_before_response(self, **kwargs):
        self.response_context.update(
            query_status_events = self._enrich_result_queries(self.get_db().queries_status()),
            database_status_events = self.get_db().database_status(),
            sw_versions = mentat.system.analyze_versions()
        )

        dbstatistics_events = {
            'total_bytes': {
                x: y['total_bytes'] for x, y in self.response_context['database_status_events']['tables'].items()
            },
            'table_bytes': {
                x: y['table_bytes'] for x, y in self.response_context['database_status_events']['tables'].items()
            },
            'index_bytes': {
                x: y['index_bytes'] for x, y in self.response_context['database_status_events']['tables'].items()
            },
            'row_estimate': {
                x: y['row_estimate'] for x, y in self.response_context['database_status_events']['tables'].items()
            }
        }
        self.response_context.update(
            database_statistics_events = dbstatistics_events
        )

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'stop',
            endpoint = 'dbstatus.query-stop',
            hidetitle = True,
            legend = lambda **x: lazy_gettext('Stop user query &quot;%(item)s&quot;', item = x['item']['query_name']),
            cssclass = 'action-ajax'
        )
        self.response_context['context_action_menu_query'] = action_menu


class MyQueriesView(HTMLMixin, PsycopgMixin, SimpleView):
    """
    Application view providing access status information of given single query.
    """
    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'queries_my'

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('My queries')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('My currently running queries')

    def _enrich_result_queries(self, result):
        """
        Enrich query status result with information about the user running the query.
        """
        cache = {}
        for record in result:
            if 'query_name' not in record:
                continue
            user_id, query_id = self.parse_qname(record['query_name'])
            record['user_id'] = user_id
            record['query_id'] = query_id
            if user_id not in cache:
                cache[user_id] = vial.db.db_get().session.query(UserModel).filter(UserModel.id == int(user_id)).one_or_none()
            record['user'] = cache[user_id]
        return result

    def do_before_response(self, **kwargs):
        self.response_context.update(
            query_status_events = self._enrich_result_queries(
                self.get_db().queries_status(
                    RE_UQUERY.format(
                        int(flask_login.current_user.get_id())
                    )
                )
            )
        )

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'stop',
            endpoint = 'dbstatus.query-stop',
            hidetitle = True,
            legend = lambda **x: lazy_gettext('Stop user query &quot;%(item)s&quot;', item = x['item']['query_name']),
            cssclass = 'action-ajax'
        )
        self.response_context['context_action_menu_query'] = action_menu


class QueryStatusView(AJAXMixin, PsycopgMixin, RenderableView):
    """
    Application view providing access status information of given single query.
    """
    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'query-status'

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Query status')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Query status')

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(
            cls.get_view_endpoint(),
            item_id = kwargs['item']['query_name']
        )

    def do_before_response(self, **kwargs):
        query_status = self.get_db().query_status(kwargs['item_id'])
        if not query_status:
            self.abort(404)

        self.response_context.update(
            user_id = kwargs['user_id'],
            query_name = kwargs['item_id'],
            query_status = query_status
        )

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the **Flask** framework to service the request.
        """
        user_id, _ = self.parse_qname(item_id)
        if flask_login.current_user.get_id() != user_id and not vial.acl.PERMISSION_POWER.can():
            self.abort(
                403,
                gettext('You are not allowed to view status of this query.')
            )

        self.do_before_response(item_id = item_id, user_id = user_id)
        return self.generate_response()


class AbstractQueryStopView(PsycopgMixin, RenderableView):  # pylint: disable=locally-disabled,abstract-method
    """
    Application view providing ability to stop given query.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'action-stop'

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Stop query')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Stop query')

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(
            cls.get_view_endpoint(),
            item_id = kwargs['item']['query_name']
        )

    @classmethod
    def authorize_item_action(cls, **kwargs):
        user_id, _ = cls.parse_qname(kwargs['item']['query_name'])
        return vial.acl.PERMISSION_POWER.can() or flask_login.current_user.get_id() == user_id

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Query <strong>%(item_id)s</strong> was successfully stopped.',
            item_id = flask.escape(str(kwargs['item']['query_name']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to stop query <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']['query_name']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled stopping query <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']['query_name']))
        )

    def get_url_next(self):
        try:
            return flask.url_for(
                '{}.{}'.format(self.module_name, 'view')
            )
        except werkzeug.routing.BuildError:
            return flask.url_for(
                flask.current_app.config['ENDPOINT_HOME']
            )

    def check_action_cancel(self, form, **kwargs):
        """
        Check the form for *cancel* button press and cancel the action.
        """
        if hasattr(form, vial.const.FORM_ACTION_CANCEL):
            if getattr(form, vial.const.FORM_ACTION_CANCEL).data:
                self.flash(
                    flask.Markup(self.get_message_cancel(**kwargs)),
                    vial.const.FLASH_INFO
                )
                return self.redirect(default_url = self.get_url_next())

        return None

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the **Flask** framework to service the request.
        """
        item = self.get_db().query_status(item_id)
        if not item:
            self.abort(404)

        if not self.authorize_item_action(item = item):
            self.abort(403)

        form = ItemActionConfirmForm()

        cancel_response = self.check_action_cancel(form, item = item)
        if cancel_response:
            return cancel_response

        if form.validate_on_submit():
            form_data = form.data

            if form_data[vial.const.FORM_ACTION_SUBMIT]:
                try:
                    action_status = self.get_db().query_cancel(item_id)
                    if action_status:
                        self.flash(
                            flask.Markup(self.get_message_success(item = item)),
                            vial.const.FLASH_SUCCESS
                        )
                    else:
                        self.flash(
                            flask.Markup(self.get_message_failure(item = item)),
                            vial.const.FLASH_FAILURE
                        )
                    self.get_db().commit()
                    return self.redirect(default_url = self.get_url_next())

                except Exception:  # pylint: disable=locally-disabled,broad-except
                    self.get_db().commit()
                    self.flash(
                        flask.Markup(self.get_message_failure(item = item)),
                        vial.const.FLASH_FAILURE
                    )
                    flask.current_app.log_exception_with_label(
                        traceback.TracebackException(*sys.exc_info()),
                        self.get_message_failure(item = item)
                    )
                    return self.redirect(default_url = self.get_url_next())

        self.response_context.update(
            confirm_form = form,
            confirm_url  = flask.url_for(
                '{}.{}'.format(
                    self.module_name,
                    self.get_view_name()
                ),
                item_id = item_id
            ),
            item_id      = item_id,
            item         = item
        )

        self.do_before_response()
        return self.generate_response()


class QueryStopView(HTMLMixin, AbstractQueryStopView):
    """
    Application view providing ability to stop given query.
    """
    @classmethod
    def get_view_name(cls):
        return 'query-stop'

    @classmethod
    def get_view_template(cls):
        return '{}/query_stop.html'.format(cls.module_name)


class ApiQueryStopView(AJAXMixin, AbstractQueryStopView):
    """
    Application view providing ability to stop given query.
    """
    @classmethod
    def get_view_name(cls):
        return 'api-query-stop'


class DashboardView(HTMLMixin, SQLAlchemyMixin, SimpleView):  # pylint: disable=locally-disabled,abstract-method
    """
    View responsible for presenting database dashboard.
    """
    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_name(cls):
        return 'dashboard'

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Object management')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Object management dashboards')

    @classmethod
    def get_view_template(cls):
        return '{}/dashboard.html'.format(cls.module_name)

    #---------------------------------------------------------------------------


    def do_before_response(self, **kwargs):
        """*Implementation* of :py:func:`vial.view.RenderableView.do_before_response`."""
        self.response_context['users_disabled'] = self.dbquery(UserModel).\
            filter(UserModel.enabled == False).\
            order_by(UserModel.createtime.desc()).\
            all()
        self.response_context['users_nomemberships'] = self.dbquery(UserModel).\
            filter(~UserModel.memberships.any()).\
            order_by(UserModel.createtime.desc()).\
            all()
        self.response_context['users_noroles'] = self.dbquery(UserModel).\
            filter(UserModel.roles == []).\
            order_by(UserModel.createtime.desc()).\
            all()
        self.response_context['users_nologin'] = self.dbquery(UserModel).\
            filter(
                or_(
                    UserModel.logintime.is_(None),
                    UserModel.logintime <= (datetime.datetime.utcnow() - datetime.timedelta(days = 365))
                )
            ).\
            order_by(UserModel.createtime.desc()).\
            all()

        self.response_context['groups_disabled'] = self.dbquery(GroupModel).\
            filter(GroupModel.enabled == False).\
            order_by(GroupModel.createtime.desc()).\
            all()
        self.response_context['groups_nomembers'] = self.dbquery(GroupModel).\
            filter(~GroupModel.members.any()).\
            order_by(GroupModel.createtime.desc()).\
            all()
        self.response_context['groups_nomanagers'] = self.dbquery(GroupModel).\
            filter(~GroupModel.members.any()).\
            order_by(GroupModel.createtime.desc()).\
            all()
        self.response_context['groups_nonetworks'] = self.dbquery(GroupModel).\
            filter(~GroupModel.networks.any()).\
            order_by(GroupModel.createtime.desc()).\
            all()

        self.response_context['filters_disabled'] = self.dbquery(FilterModel).\
            filter(FilterModel.enabled == False).\
            order_by(FilterModel.createtime.desc()).\
            all()
        self.response_context['filters_nohits'] = self.dbquery(FilterModel).\
            filter(FilterModel.hits == 0).\
            order_by(FilterModel.createtime.desc()).\
            all()
        self.response_context['filters_future'] = self.dbquery(FilterModel).\
            filter(FilterModel.valid_from > (datetime.datetime.utcnow() + datetime.timedelta(days = 14))).\
            order_by(FilterModel.createtime.desc()).\
            all()
        self.response_context['filters_expired'] = self.dbquery(FilterModel).\
            filter(FilterModel.valid_to < datetime.datetime.utcnow()).\
            order_by(FilterModel.createtime.desc()).\
            all()

        self.response_context['settingsrep_redirected'] = self.dbquery(SettingsReportingModel).\
            filter(SettingsReportingModel.redirect == True).\
            order_by(SettingsReportingModel.createtime.desc()).\
            all()
        self.response_context['settingsrep_modenone'] = self.dbquery(SettingsReportingModel).\
            filter(SettingsReportingModel.mode == mentat.const.REPORTING_MODE_NONE).\
            order_by(SettingsReportingModel.createtime.desc()).\
            all()
        self.response_context['settingsrep_emailscust'] = self.dbquery(SettingsReportingModel).\
            filter(SettingsReportingModel.emails_low != [] or SettingsReportingModel.emails_medium != [] or
                   SettingsReportingModel.emails_high != [] or SettingsReportingModel.emails_critical != []).\
            order_by(SettingsReportingModel.createtime.desc()).\
            all()

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'users.show',
            hidetitle = True,
            legend = lambda **x: lazy_gettext('View details of user account &quot;%(item)s&quot;', item = flask.escape(x['item'].login))
        )
        action_menu.add_entry(
            'submenu',
            'more',
            legend = lazy_gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'users.update',
            legend = lambda **x: lazy_gettext('Update details of user account &quot;%(item)s&quot;', item = flask.escape(x['item'].login))
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'users.disable',
            icon = 'action-disable-user',
            legend = lambda **x: lazy_gettext('Disable user account &quot;%(item)s&quot;', item = flask.escape(x['item'].login))
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'users.enable',
            icon = 'action-enable-user',
            legend = lambda **x: lazy_gettext('Enable user account &quot;%(item)s&quot;', item = flask.escape(x['item'].login))
        )
        action_menu.add_entry(
            'endpoint',
            'more.delete',
            endpoint = 'users.delete',
            icon = 'action-delete-user',
            legend = lambda **x: lazy_gettext('Delete user account &quot;%(item)s&quot;', item = flask.escape(x['item'].login))
        )
        self.response_context['context_action_menu_user'] = action_menu

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'groups.show',
            hidetitle = True,
            legend = lambda **x: lazy_gettext('View details of group &quot;%(item)s&quot;', item = flask.escape(str(x['item'])))
        )
        action_menu.add_entry(
            'submenu',
            'more',
            legend = lazy_gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'groups.update',
            legend = lambda **x: lazy_gettext('Update details of group &quot;%(item)s&quot;', item = flask.escape(str(x['item'])))
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'groups.disable',
            legend = lambda **x: lazy_gettext('Disable group &quot;%(item)s&quot;', item = flask.escape(str(x['item'])))
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'groups.enable',
            legend = lambda **x: lazy_gettext('Enable group &quot;%(item)s&quot;', item = flask.escape(str(x['item'])))
        )
        action_menu.add_entry(
            'endpoint',
            'more.delete',
            endpoint = 'groups.delete',
            legend = lambda **x: lazy_gettext('Delete group &quot;%(item)s&quot;', item = flask.escape(str(x['item'])))
        )
        self.response_context['context_action_menu_group'] = action_menu

        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'filters.show',
            hidetitle = True,
            legend = lambda **x: lazy_gettext('View details of reporting filter &quot;%(item)s&quot;', item = flask.escape(x['item'].name))
        )
        action_menu.add_entry(
            'submenu',
            'more',
            legend = lazy_gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'filters.update',
            legend = lambda **x: lazy_gettext('Update details of reporting filter &quot;%(item)s&quot;', item = flask.escape(x['item'].name))
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'filters.disable',
            legend = lambda **x: lazy_gettext('Disable reporting filter &quot;%(item)s&quot;', item = flask.escape(x['item'].name))
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'filters.enable',
            legend = lambda **x: lazy_gettext('Enable reporting filter &quot;%(item)s&quot;', item = flask.escape(x['item'].name))
        )
        action_menu.add_entry(
            'endpoint',
            'more.delete',
            endpoint = 'filters.delete',
            legend = lambda **x: lazy_gettext('Delete reporting filter &quot;%(item)s&quot;', item = flask.escape(x['item'].name))
        )
        self.response_context['context_action_menu_filter'] = action_menu


#-------------------------------------------------------------------------------


class DatabaseStatusBlueprint(VialBlueprint):
    """Pluggable module - database status overview (*dbstatus*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Database status overview')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'dashboards.dbstatus',
            position = 100,
            view = DashboardView
        )
        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 30,
            view = ViewView
        )
        app.menu_auth.add_entry(
            'view',
            'queries_my',
            position = 50,
            view = MyQueriesView
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = DatabaseStatusBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(ViewView,         '/{}/view'.format(BLUEPRINT_NAME))
    hbp.register_view_class(MyQueriesView,    '/{}/query/my'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DashboardView,    '/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(QueryStatusView,  '/api/{}/query/<item_id>/status'.format(BLUEPRINT_NAME))
    hbp.register_view_class(QueryStopView,    '/{}/query/<item_id>/stop'.format(BLUEPRINT_NAME))
    hbp.register_view_class(ApiQueryStopView, '/api/{}/query/<item_id>/stop'.format(BLUEPRINT_NAME))

    return hbp

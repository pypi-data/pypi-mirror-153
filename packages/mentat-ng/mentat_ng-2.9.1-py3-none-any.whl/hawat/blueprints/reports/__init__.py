#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access to periodical event reports.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import re
import os.path
import datetime
import dateutil.parser
import pytz

from jinja2.loaders import ChoiceLoader, FileSystemLoader
import flask
from flask.helpers import locked_cached_property
import flask_login
import flask_principal
import flask_mail
from flask_babel import gettext, lazy_gettext, force_locale, format_datetime

import mentat.const
import mentat.stats.idea
from mentat.datatype.sqldb import EventReportModel, GroupModel, UserModel, ItemChangeLogModel, \
    _asoc_groups_reports
from mentat.const import tr_

import hawat.const

import vial.menu
import vial.acl
from vial.app import VialBlueprint
from vial.view import RenderableView, FileIdView, BaseSearchView, ItemShowView, ItemDeleteView
from vial.view.mixin import HTMLMixin, AJAXMixin, SQLAlchemyMixin
from vial.utils import URLParamsBuilder
from hawat.blueprints.reports.forms import EventReportSearchForm, ReportingDashboardForm, \
    FeedbackForm

BLUEPRINT_NAME = 'reports'
"""Name of the blueprint as module global constant."""

BABEL_RFC3339_FORMAT = "yyyy-MM-ddTHH:mm:ssZZZ"


def build_related_search_params(item):
    """
    Build dictionary containing parameters for searching related report events.
    """
    related_events_search_params = {
        'st_from': item.dt_from,
        'st_to': item.dt_to,
        'severities': item.severity,
        'categories': 'Test',
        'groups': [group.name for group in item.groups],
        'submit': gettext('Search')
    }
    if not item.flag_testdata:
        related_events_search_params.update(
            {
                'not_categories': 'True'
            }
        )
    return related_events_search_params

def adjust_query_for_groups(query, groups):
    """
    Adjust given SQLAlchemy query for current user. In case user specified set of
    groups, perform query filtering. In case no groups were selected, restrict
    non-administrators only to groups they are member of.
    """

    # Adjust query to filter only selected groups.
    if groups:
        # Naive approach.
        #query = query.filter(model.group_id.in_([grp.id for grp in groups]))
        # "Joined" approach.
        return query.join(_asoc_groups_reports).join(GroupModel).filter(GroupModel.id.in_([grp.id for grp in groups]))

    # For non-administrators restrict query only to groups they are member of.
    if not flask_login.current_user.has_role(vial.const.ROLE_ADMIN):
        # Naive approach.
        #query = query.filter(model.group.has(GroupModel.members.any(UserModel.id == flask_login.current_user.id)))
        # "Joined" approach.
        return query.join(_asoc_groups_reports).join(GroupModel).filter(GroupModel.members.any(UserModel.id == flask_login.current_user.id))

    return query


class SearchView(HTMLMixin, SQLAlchemyMixin, BaseSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for searching IDEA event report database and presenting result.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event reports')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Reports')

    @property
    def dbmodel(self):
        return EventReportModel

    @staticmethod
    def get_search_form(request_args):
        return EventReportSearchForm(request_args, meta = {'csrf': False})

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on group selection.
        query = adjust_query_for_groups(query, form_args.get('groups', None))
        # Adjust query based on text search string.
        if 'label' in form_args and form_args['label']:
            query = query.filter(model.label.like('%{}%'.format(form_args['label'])))
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.createtime >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.createtime <= form_args['dt_to'])
        # Adjust query based on report severity selection.
        if 'types' in form_args and form_args['severities']:
            query = query.filter(model.severity.in_(form_args['severities']))
        # Adjust query based on report type selection.
        if 'severities' in form_args and form_args['types']:
            query = query.filter(model.type.in_(form_args['types']))

        # Return the result sorted by creation time in descending order and by label.
        return query.order_by(model.createtime.desc()).order_by(model.label.desc())

    def do_after_search(self, items):
        if items:
            self.response_context.update(
                max_evcount_rep = max([x.evcount_rep for x in items])
            )


class ShowView(HTMLMixin, SQLAlchemyMixin, ItemShowView):
    """
    Detailed report view.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Show report')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'View details of event report &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show report')

    @property
    def dbmodel(self):
        return EventReportModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        for group in kwargs['item'].groups:
            permission_mm = flask_principal.Permission(
                vial.acl.MembershipNeed(group.id),
                vial.acl.ManagementNeed(group.id)
            )
            if permission_mm.can():
                return permission_mm.can()
        return vial.acl.PERMISSION_POWER.can()

    @classmethod
    def get_breadcrumbs_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'home',
            endpoint = flask.current_app.config['ENDPOINT_HOME']
        )
        action_menu.add_entry(
            'endpoint',
            'search',
            endpoint = '{}.search'.format(cls.module_name)
        )
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = '{}.show'.format(cls.module_name),
        )
        return action_menu

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'search',
            endpoint = 'events.search',
            title = lazy_gettext('Search'),
            legend = lambda **x: lazy_gettext('Search for all events related to report &quot;%(item)s&quot;', item = flask.escape(x['item'].label)),
            url = lambda **x: flask.url_for('events.search', **build_related_search_params(x['item']))
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'reports.delete'
        )
        action_menu.add_entry(
            'submenu',
            'more',
            align_right = True,
            legend = lazy_gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.downloadjson',
            endpoint = 'reports.data',
            title = lazy_gettext('Download data in JSON format'),
            url = lambda **x: flask.url_for('reports.data', fileid = x['item'].label, filetype = 'json'),
            icon = 'action-download',
            hidelegend = True
        )
        action_menu.add_entry(
            'endpoint',
            'more.downloadjsonzip',
            endpoint = 'reports.data',
            title = lazy_gettext('Download compressed data in JSON format'),
            url = lambda **x: flask.url_for('reports.data', fileid = x['item'].label, filetype = 'jsonzip'),
            icon = 'action-download-zip',
            hidelegend = True
        )
        return action_menu

    @staticmethod
    def format_datetime(val, tzone):
        """
        Static method that take string with isoformat datetime in utc and return
        string with BABEL_RFC3339_FORMAT formated datetime in tz timezone
        """
        return format_datetime(
            dateutil.parser.parse(val).replace(tzinfo=pytz.utc).astimezone(tzone),
            BABEL_RFC3339_FORMAT,
            rebase = False
        )

    @staticmethod
    def format_datetime_wz(val, format_str, tzone):
        """
        Static method that take string with isoformat datetime in utc and return
        string with BABEL_RFC3339_FORMAT formated datetime in tz timezone
        """
        return format_datetime(
            dateutil.parser.parse(val).replace(tzinfo=pytz.utc).astimezone(tzone),
            format_str,
            rebase = False
        )

    @staticmethod
    def escape_id(ident):
        """
        Escape id for use in bootstrap
        """
        return re.sub(r"[^A-Za-z0-9-_]", (lambda x: '\{:X} '.format(ord(x.group()))), ident)

    def do_before_response(self, **kwargs):
        if 'item' in self.response_context and self.response_context['item']:
            self.response_context.update(
                statistics         = self.response_context['item'].statistics,
                template_vars      = flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_TEMPLATEVARS],
                form               = FeedbackForm(),
                format_datetime    = ShowView.format_datetime,
                format_datetime_wz = ShowView.format_datetime_wz,
                tz                 = pytz.timezone(self.response_context['item'].structured_data["timezone"]) if self.response_context['item'].structured_data else None,
                tz_utc             = pytz.utc,
                event_classes_dir  = flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_EVENTCLASSESDIR],
                escape_id          = ShowView.escape_id
            )
            if self.response_context['item'].mail_to:
                mails = self.response_context['item'].mail_to
                self.response_context.update(
                    to_mails = [x[3:] if x.startswith('to:') else x for x in mails if not x.startswith('cc:')],
                    cc_mails = [x[3:] for x in mails if x.startswith('cc:')]
                )


class UnauthShowView(ShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Unauthorized access to report detail view.
    """
    methods = ['GET']

    authentication = False

    @classmethod
    def get_view_name(cls):
        return 'unauth'

    @classmethod
    def get_view_template(cls):
        return '{}/show.html'.format(cls.module_name)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        return True

    @property
    def search_by(self):
        return self.dbmodel.label


class DataView(FileIdView):
    """
    View responsible for providing access to report data.
    """
    methods = ['GET']

    authentication = False

    @classmethod
    def get_view_name(cls):
        return 'data'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Event report data')

    @classmethod
    def get_directory_path(cls, fileid, filetype):
        return mentat.const.construct_report_dirpath(
            flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_REPORTSDIR],
            fileid,
            True
        )

    def get_filename(self, fileid, filetype):
        fileext = ''
        if filetype == 'json':
            fileext = 'json'
        elif filetype == 'jsonzip':
            fileext = 'json.zip'
        else:
            raise ValueError("Requested invalid data file type '{}'".format(filetype))
        return 'security-report-{}.{}'.format(fileid, fileext)


class AbstractDashboardView(SQLAlchemyMixin, BaseSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Base class responsible for presenting reporting dashboard.
    """
    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Reporting')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Event reporting dashboards')

    @classmethod
    def get_view_template(cls):
        return '{}/dashboard.html'.format(cls.module_name)

    @property
    def dbmodel(self):
        return EventReportModel

    @staticmethod
    def get_search_form(request_args):
        return ReportingDashboardForm(request_args, meta = {'csrf': False})

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on group selection.
        query = adjust_query_for_groups(query, form_args.get('groups', None))
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.createtime >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.createtime <= form_args['dt_to'])

        # Return the result sorted by label.
        return query.order_by(model.label)

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating event reporting dashboard overview from %d records.",
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

            stats = mentat.stats.idea.aggregate_stats_reports(items, dt_from, dt_to)

            # Remove to: and cc: prefixes from emails.
            if 'emails' in stats:
                d = {}
                for k, v in stats['emails'].items():
                    key = k[3:] if k.startswith('to:') or k.startswith('cc:') else k
                    if not key in d:
                        d[key] = 0
                    d[key] += v
                stats['emails'] = d

            self.response_context.update(
                statistics = stats
            )

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )


class DashboardView(HTMLMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting reporting dashboard in the form of HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return 'dashboard'


class APIDashboardView(AJAXMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting reporting dashboard in the form of JSON document.
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


class DeleteView(HTMLMixin, SQLAlchemyMixin, ItemDeleteView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for deleting existing user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_ADMIN]

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Delete event report &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    def get_url_next(self):
        return flask.url_for(
            '{}.{}'.format(self.module_name, 'search')
        )

    @property
    def dbmodel(self):
        return EventReportModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Event report <strong>%(item_id)s</strong> was successfully and permanently deleted.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to delete event report <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled deleting event report <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


class FeedbackView(AJAXMixin, RenderableView):
    """
    View for sending feedback for reports.
    """
    methods = ['POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'feedback'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Report feedback')

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.

        Feedback for report with label *item_id*.
        More specific part like section and ip can be send in POST data.
        """
        form = FeedbackForm(flask.request.form)
        if form.validate():
            mail_locale = flask.current_app.config['BABEL_DEFAULT_LOCALE']
            link = flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_TEMPLATEVARS]["report_access_url"] + \
                item_id + "/unauth" + "#" + form.section.data
            feedback_for = item_id + " (" + form.section.data + ", ip: " + form.ip.data + ")"

            with force_locale(mail_locale):
                msg = flask_mail.Message(
                    gettext(
                        "[Mentat] Feedback for report - %(item_id)s",
                        item_id=item_id
                    ),
                    recipients=flask.current_app.config['HAWAT_REPORT_FEEDBACK_MAILS'],
                    reply_to=flask_login.current_user.email
                )
                msg.body = flask.render_template(
                    'reports/email_report_feedback.txt',
                    account=flask_login.current_user,
                    text=form.text.data,
                    feedback_for=feedback_for,
                    link=link
                )
                flask.current_app.mailer.send(msg)
            self.response_context["message"] = gettext('Thank you. Your feedback was sent to administrators.')
        else:
            self.response_context.update(
                form_errors=[(field_name, err) for field_name, error_messages in form.errors.items() for err in error_messages]
            )
            self.response_context["message"] = "<br />".join([": ".join(err) for err in self.response_context["form_errors"]])
        return self.generate_response()


#-------------------------------------------------------------------------------


class ReportsBlueprint(VialBlueprint):
    """Pluggable module - periodical event reports (*reports*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Event reports')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'dashboards.reporting',
            position = 20,
            view = DashboardView
        )
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position = 120,
            view = SearchView,
            resptitle = True
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('Search for abuse group <strong>%(name)s</strong> in report database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('groups', True).add_kwrule('dt_from', False, True).add_kwrule('dt_to', False, True)
        )

        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('Search for abuse group <strong>%(name)s</strong> in reporting dashboards'),
            DashboardView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('groups', True).add_kwrule('dt_from', False, True).add_kwrule('dt_to', False, True)
        )

    @locked_cached_property
    def jinja_loader(self):
        """The Jinja loader for this package bound object.

        .. versionadded:: 0.5
        """
        return ChoiceLoader([FileSystemLoader(os.path.join(self.root_path, self.template_folder)),
                             FileSystemLoader(flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_TEMPLATESDIR]),
                             FileSystemLoader(flask.current_app.mconfig[mentat.const.CKEY_CORE_REPORTER][mentat.const.CKEY_CORE_REPORTER_EVENTCLASSESDIR])])

#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = ReportsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(SearchView,       '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(ShowView,         '/{}/<int:item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(UnauthShowView,   '/{}/<item_id>/unauth'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DataView,         '/{}/data/<fileid>/<filetype>'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DashboardView,    '/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DeleteView,       '/{}/<int:item_id>/delete'.format(BLUEPRINT_NAME))
    hbp.register_view_class(FeedbackView,     '/{}/<item_id>/feedback'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIDashboardView, '/api/{}/dashboard'.format(BLUEPRINT_NAME))

    return hbp

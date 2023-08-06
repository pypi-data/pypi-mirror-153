#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access to reporting filter management features. These
features include:

* general reporting filter listing
* detailed reporting filter view
* creating new reporting filters
* updating existing reporting filters
* deleting existing reporting filters
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sys
import traceback

import flask
import flask_login
import flask_principal
from flask_babel import gettext, lazy_gettext

from sqlalchemy import or_

import ipranges
import pynspect.gparser
import pynspect.traversers
import pynspect.filters
from pynspect.gparser import PynspectFilterParser
from pynspect.filters import DataObjectFilter

from mentat.const import REPORTING_FILTER_BASIC
from mentat.datatype.sqldb import FilterModel, GroupModel, ItemChangeLogModel
from mentat.idea.internal import Idea, IDEAFilterCompiler

import vial.const
import vial.db
from vial.app import VialBlueprint
from vial.view import RenderableView, ItemListView, ItemShowView, ItemCreateView, ItemCreateForView, ItemUpdateView, ItemDeleteView, ItemEnableView, ItemDisableView
from vial.view.mixin import HTMLMixin, SQLAlchemyMixin
import hawat.events
from hawat.blueprints.filters.forms import BaseFilterForm, AdminFilterForm, PlaygroundFilterForm, FilterSearchForm


_PARSER = PynspectFilterParser()
_PARSER.build()

_COMPILER = IDEAFilterCompiler()
_FILTER = DataObjectFilter()


BLUEPRINT_NAME = 'filters'
"""Name of the blueprint as module global constant."""


def process_rule(item):
    """
    Process given event report filtering rule and generate advanced single rule
    string from simple filtering form data.
    """
    if item.type == REPORTING_FILTER_BASIC:
        rules = []
        if item.detectors:
            rules.append('Node.Name IN ["{}"]'.format('","'.join(item.detectors)))

        if item.categories:
            rules.append('Category IN ["{}"]'.format('","'.join(item.categories)))

        if item.ips:
            ip4s = []
            ip6s = []
            for ipa in item.ips:
                ipobj = ipranges.from_str(ipa)
                if isinstance(ipobj, (ipranges.IP4, ipranges.IP4Range, ipranges.IP4Net)):
                    ip4s.append(ipa)
                else:
                    ip6s.append(ipa)
            if ip4s:
                rules.append('Source.IP4 IN ["{}"]'.format('","'.join(ip4s)))
            if ip6s:
                rules.append('Source.IP6 IN ["{}"]'.format('","'.join(ip6s)))

        item.filter = ' AND '.join(rules)


def to_tree(rule):
    """
    Parse given filtering rule to object tree.
    """
    if rule:
        return _PARSER.parse(rule)
    return None

def tree_compile(rule_tree):
    """
    Compile given filtering rule tree.
    """
    if rule_tree:
        return _COMPILER.compile(rule_tree)
    return None

def tree_html(rule_tree):
    """
    Render given rule object tree to HTML formatted content.
    """
    if rule_tree:
        return rule_tree.traverse(pynspect.traversers.HTMLTreeTraverser())
    return None

def tree_check(rule_tree, data):
    """
    Check given event against given rule tree.
    """
    return _FILTER.filter(rule_tree, data)


class ListView(HTMLMixin, SQLAlchemyMixin, ItemListView):
    """
    General reporting filter listing.
    """
    methods = ['GET']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Filter management')

    #---------------------------------------------------------------------------

    @property
    def dbmodel(self):
        return FilterModel

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'create',
            endpoint = 'filters.create',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'playground',
            endpoint = 'filters.playground',
            resptitle = True
        )
        return action_menu

    @classmethod
    def get_context_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'filters.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'filters.update',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'filters.disable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'filters.enable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'filters.delete',
            hidetitle = True
        )
        return action_menu

    @staticmethod
    def get_search_form(request_args):
        """
        Must return instance of :py:mod:`flask_wtf.FlaskForm` appropriate for
        searching given type of items.
        """
        return FilterSearchForm(
            request_args,
            meta = {'csrf': False}
        )

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on text search string.
        if 'search' in form_args and form_args['search']:
            query = query\
                .filter(
                    or_(
                        model.name.like('%{}%'.format(form_args['search'])),
                        model.filter.like('%{}%'.format(form_args['search'])),
                        model.description.like('%{}%'.format(form_args['search'])),
                    )
                )
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.createtime >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.createtime <= form_args['dt_to'])
        # Adjust query based on item state selection.
        if 'state' in form_args and form_args['state']:
            if form_args['state'] == 'enabled':
                query = query.filter(model.enabled == True)
            elif form_args['state'] == 'disabled':
                query = query.filter(model.enabled == False)
        # Adjust query based on upper time boudary selection.
        if 'type' in form_args and form_args['type']:
            query = query.filter(model.type == form_args['type'])
        # Adjust query based on user membership selection.
        if 'group' in form_args and form_args['group']:
            query = query\
                .filter(model.group_id == form_args['group'].id)
        if 'sortby' in form_args and form_args['sortby']:
            sortmap = {
                'createtime.desc': lambda x, y: x.order_by(y.createtime.desc()),
                'createtime.asc': lambda x, y: x.order_by(y.createtime.asc()),
                'name.desc': lambda x, y: x.order_by(y.name.desc()),
                'name.asc': lambda x, y: x.order_by(y.name.asc()),
                'hits.desc': lambda x, y: x.order_by(y.hits.desc()),
                'hits.asc': lambda x, y: x.order_by(y.hits.asc()),
                'last_hit.desc': lambda x, y: x.order_by(y.last_hit.desc()),
                'last_hit.asc': lambda x, y: x.order_by(y.last_hit.asc())
            }
            query = sortmap[form_args['sortby']](query, model)
        return query


class ShowView(HTMLMixin, SQLAlchemyMixin, ItemShowView):
    """
    Detailed reporting filter view.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'View details of reporting filter &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].name)
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show reporting filter details')

    @property
    def dbmodel(self):
        return FilterModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_mm = flask_principal.Permission(
            vial.acl.MembershipNeed(kwargs['item'].group.id),
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_mm.can()

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'filters.update',
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'filters.disable',
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'filters.enable',
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'filters.delete',
        )
        action_menu.add_entry(
            'endpoint',
            'playground',
            endpoint = 'filters.playground',
        )
        return action_menu

    def do_before_response(self, **kwargs):
        item = self.response_context['item']
        filter_tree = to_tree(item.filter)
        filter_compiled = tree_compile(filter_tree)
        self.response_context.update(
            filter_tree = filter_tree,
            filter_compiled = filter_compiled,
            filter_preview = tree_html(filter_tree),
            filter_compiled_preview = tree_html(filter_compiled)
        )

        if self.can_access_endpoint('filters.update', item = item) and self.has_endpoint('changelogs.search'):
            self.response_context.update(
                context_action_menu_changelogs = self.get_endpoint_class(
                    'changelogs.search'
                ).get_context_action_menu()
            )

            item_changelog = self.dbsession.query(ItemChangeLogModel).\
                filter(ItemChangeLogModel.model == item.__class__.__name__).\
                filter(ItemChangeLogModel.model_id == item.id).\
                order_by(ItemChangeLogModel.createtime.desc()).\
                limit(100).\
                all()
            self.response_context.update(item_changelog = item_changelog)


class CreateView(HTMLMixin, SQLAlchemyMixin, ItemCreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new reporting filters for any groups.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Create reporting filter')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Create new reporting filter')

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        return vial.acl.PERMISSION_POWER.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully created.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to create new reporting filter for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled creating new reporting filter for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_item_form(item):
        detectors  = hawat.events.get_event_detectors()
        categories = hawat.events.get_event_categories()

        return AdminFilterForm(
            choices_detectors  = list(zip(detectors,detectors)),
            choices_categories = list(zip(categories,categories))
        )

    def do_before_action(self, item):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        process_rule(item)

    def do_before_response(self, **kwargs):
        item = self.response_context.get('item', None)
        if item:
            filter_tree = to_tree(item.filter)
            self.response_context.update(
                filter_tree = filter_tree,
                filter_preview = tree_html(filter_tree)
            )


class CreateForView(HTMLMixin, SQLAlchemyMixin, ItemCreateForView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new reporting filters for given groups.
    """
    methods = ['GET','POST']

    authentication = True

    module_name_par = 'groups'

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Create reporting filter')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Create reporting filter for group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(
            cls.get_view_endpoint(),
            parent_id = kwargs['item'].id
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Create new reporting filter for group')

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbmodel_par(self):
        return GroupModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully created.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['parent']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to create new reporting filter for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['parent']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled creating new reporting filter for group <strong>%(parent_id)s</strong>.',
            parent_id = flask.escape(str(kwargs['parent']))
        )

    @staticmethod
    def get_item_form(item):
        detectors  = hawat.events.get_event_detectors()
        categories = hawat.events.get_event_categories()

        return BaseFilterForm(
            choices_detectors  = list(zip(detectors,detectors)),
            choices_categories = list(zip(categories,categories))
        )

    @staticmethod
    def add_parent_to_item(item, parent):
        item.group = parent

    def do_before_action(self, item):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        process_rule(item)

    def do_before_response(self, **kwargs):
        item = self.response_context.get('item', None)
        if item:
            filter_tree = to_tree(item.filter)
            self.response_context.update(
                filter_tree = filter_tree,
                filter_preview = tree_html(filter_tree)
            )


class UpdateView(HTMLMixin, SQLAlchemyMixin, ItemUpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing reporting filters.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Update details of reporting filter &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].name)
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Update reporting filter details')

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully updated.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to update reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled updating reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_item_form(item):
        detectors  = hawat.events.get_event_detectors()
        categories = hawat.events.get_event_categories()

        admin = flask_login.current_user.has_role('admin')
        if not admin:
            return BaseFilterForm(
                obj = item,
                choices_detectors  = list(zip(detectors,detectors)),
                choices_categories = list(zip(categories,categories))
            )

        return AdminFilterForm(
            obj = item,
            choices_detectors  = list(zip(detectors,detectors)),
            choices_categories = list(zip(categories,categories))
        )

    def do_before_action(self, item):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        process_rule(item)

    def do_before_response(self, **kwargs):
        item = self.response_context['item']
        filter_tree = to_tree(item.filter)
        self.response_context.update(
            filter_tree = filter_tree,
            filter_preview = tree_html(filter_tree)
        )


class EnableView(HTMLMixin, SQLAlchemyMixin, ItemEnableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for enabling existing reporting filters.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Enable reporting filter &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].name)
        )

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully enabled.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to enable reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled enabling reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )


class DisableView(HTMLMixin, SQLAlchemyMixin, ItemDisableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for disabling existing reporting filters.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Disable reporting filter &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].name)
        )

    #---------------------------------------------------------------------------

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully disabled.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to disable reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled disabling reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )


class DeleteView(HTMLMixin, SQLAlchemyMixin, ItemDeleteView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for deleting existing reporting filters.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Delete reporting filter &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].name)
        )

    @property
    def dbmodel(self):
        return FilterModel

    @property
    def dbchlogmodel(self):
        return ItemChangeLogModel

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].group.id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong> was successfully and permanently deleted.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to permanently delete reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled deleting reporting filter <strong>%(item_id)s</strong> for group <strong>%(parent_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item'])),
            parent_id = flask.escape(str(kwargs['item'].group))
        )


class PlaygroundView(HTMLMixin, RenderableView):
    """
    Reporting filter playground view.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'playground'

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Filter playground')

    @classmethod
    def get_view_icon(cls):
        return 'playground'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext('Reporting filter playground')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Reporting filter rule playground')

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
            'list',
            endpoint = '{}.{}'.format(cls.module_name, 'list')
        )
        breadcrumbs_menu.add_entry(
            'endpoint',
            'playground',
            endpoint = cls.get_view_endpoint()
        )
        return breadcrumbs_menu

    def dispatch_request(self):
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.
        """
        form = PlaygroundFilterForm()

        if form.validate_on_submit():
            form_data = form.data

            try:
                event                   = Idea.from_json(form.event.data)
                filter_tree             = to_tree(form.filter.data)
                filter_preview          = tree_html(filter_tree)
                filter_compiled         = tree_compile(filter_tree)
                filter_compiled_preview = tree_html(filter_compiled)
                filter_result           = tree_check(filter_compiled, event)

                self.response_context.update(
                    form_data               = form_data,
                    event                   = event,
                    filter_tree             = filter_tree,
                    filter_preview          = filter_preview,
                    filter_compiled         = filter_compiled,
                    filter_compiled_preview = filter_compiled_preview,
                    filter_result           = filter_result,
                    flag_filtered           = True
                )

            except Exception as err:  # pylint: disable=locally-disabled,broad-except
                self.flash(
                    flask.Markup(gettext(
                        '<strong>%(error)s</strong>.',
                        error = str(err)
                    )),
                    vial.const.FLASH_FAILURE
                )

                tbexc = traceback.TracebackException(*sys.exc_info())
                self.response_context.update(
                    filter_exception    = err,
                    filter_exception_tb = ''.join(tbexc.format())
                )


        self.response_context.update(
            form_url = flask.url_for(self.get_view_endpoint()),
            form     = form,
        )
        return self.generate_response()


#-------------------------------------------------------------------------------


class FiltersBlueprint(VialBlueprint):
    """Pluggable module - reporting filter management (*filters*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Reporting filter management pluggable module')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 60,
            view = ListView
        )
        app.menu_main.add_entry(
            'view',
            'more.{}_playground'.format(BLUEPRINT_NAME),
            position = 1,
            group = lazy_gettext('Tools'),
            view = PlaygroundView
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = FiltersBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ListView,       '/list')
    hbp.register_view_class(CreateView,     '/create')
    hbp.register_view_class(CreateForView,  '/createfor/<int:parent_id>')
    hbp.register_view_class(ShowView,       '/<int:item_id>/show')
    hbp.register_view_class(UpdateView,     '/<int:item_id>/update')
    hbp.register_view_class(EnableView,     '/<int:item_id>/enable')
    hbp.register_view_class(DisableView,    '/<int:item_id>/disable')
    hbp.register_view_class(DeleteView,     '/<int:item_id>/delete')
    hbp.register_view_class(PlaygroundView, '/playground')

    return hbp

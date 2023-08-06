#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This file contains pluggable module for Vial application containing features
related to user group management. These features include:

* general group listing
* detailed group view
* creating new groups
* updating existing groups
* deleting existing groups
* enabling existing groups
* disabling existing groups
* adding group members
* removing group members
* rejecting group membership requests
"""


import flask
import flask_login
import flask_principal
from flask_babel import gettext, lazy_gettext

from sqlalchemy import and_, or_

import vial.acl
import vial.menu
from vial.app import VialBlueprint
from vial.view import ItemListView, ItemShowView, ItemCreateView, ItemUpdateView, ItemDeleteView, ItemEnableView, ItemDisableView, ItemObjectRelationView
from vial.view.mixin import HTMLMixin, SQLAlchemyMixin
from vial.blueprints.groups.forms import AdminCreateGroupForm, AdminUpdateGroupForm, UpdateGroupForm, GroupSearchForm


BLUEPRINT_NAME = 'groups'
"""Name of the blueprint as module global constant."""


class ListView(HTMLMixin, SQLAlchemyMixin, ItemListView):
    """
    General group listing.
    """

    methods = ['GET']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Group management')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'create',
            endpoint = 'groups.create',
            resptitle = True
        )
        return action_menu

    @classmethod
    def get_context_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'groups.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'groups.update',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'groups.disable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'groups.enable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'groups.delete',
            hidetitle = True
        )
        return action_menu

    @staticmethod
    def get_search_form(request_args):
        """
        Must return instance of :py:mod:`flask_wtf.FlaskForm` appropriate for
        searching given type of items.
        """
        return GroupSearchForm(
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
                        model.description.like('%{}%'.format(form_args['search'])),
                    )
                )
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.createtime >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.createtime <= form_args['dt_to'])
        # Adjust query based on user state selection.
        if 'state' in form_args and form_args['state']:
            if form_args['state'] == 'enabled':
                query = query.filter(model.enabled == True)
            elif form_args['state'] == 'disabled':
                query = query.filter(model.enabled == False)
        # Adjust query based on record source selection.
        if 'source' in form_args and form_args['source']:
            query = query\
                .filter(model.source == form_args['source'])
        # Adjust query based on user membership selection.
        if 'member' in form_args and form_args['member']:
            query = query\
                .join(model.members)\
                .filter(model.members.any(id = form_args['member'].id))
        # Adjust query based on user membership selection.
        if 'manager' in form_args and form_args['manager']:
            query = query\
                .join(model.managers)\
                .filter(model.managers.any(id = form_args['managers'].id))
        if 'sortby' in form_args and form_args['sortby']:
            sortmap = {
                'createtime.desc': lambda x, y: x.order_by(y.createtime.desc()),
                'createtime.asc': lambda x, y: x.order_by(y.createtime.asc()),
                'name.desc': lambda x, y: x.order_by(y.name.desc()),
                'name.asc': lambda x, y: x.order_by(y.name.asc())
            }
            query = sortmap[form_args['sortby']](query, model)
        return query

class ShowView(HTMLMixin, SQLAlchemyMixin, ItemShowView):
    """
    Detailed group view.
    """

    methods = ['GET']

    authentication = True

    @classmethod
    def get_menu_legend(cls, **kwargs):
        if isinstance(kwargs['item'], cls.get_model(vial.const.MODEL_GROUP)):
            return lazy_gettext(
                'View details of group &quot;%(item)s&quot;',
                item = flask.escape(str(kwargs['item']))
            )
        return lazy_gettext(
            'View details of group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item'].group))
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show group details')

    @classmethod
    def get_view_url(cls, **kwargs):
        if isinstance(kwargs['item'], cls.get_model(vial.const.MODEL_GROUP)):
            return flask.url_for(
                cls.get_view_endpoint(),
                item_id = kwargs['item'].get_id()
            )
        return flask.url_for(
            cls.get_view_endpoint(),
            item_id = kwargs['item'].group.get_id()
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_mm = flask_principal.Permission(
            vial.acl.MembershipNeed(kwargs['item'].id),
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_mm.can()

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'groups.update',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'groups.disable',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'groups.enable',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'groups.delete',
            resptitle = True
        )
        return action_menu

    def do_before_response(self, **kwargs):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'users.show',
            hidetitle = True,
        )
        action_menu.add_entry(
            'submenu',
            'more',
            align_right = True,
            legend = gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_membership',
            endpoint = 'users.addmembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.reject_membership',
            endpoint = 'users.rejectmembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_membership',
            endpoint = 'users.removemembership'
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_management',
            endpoint = 'users.addmanagement'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_management',
            endpoint = 'users.removemanagement'
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'users.enable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'users.disable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'users.update'
        )
        self.response_context.update(
            context_action_menu_users = action_menu
        )

        item = self.response_context['item']
        if self.can_access_endpoint('groups.update', item = item) and self.has_endpoint('changelogs.search'):
            self.response_context.update(
                context_action_menu_changelogs = self.get_endpoint_class(
                    'changelogs.search'
                ).get_context_action_menu()
            )
            item_changelog_model = self.get_model(vial.const.MODEL_ITEM_CHANGELOG)
            item_changelog = self.dbsession.query(item_changelog_model).\
                filter(
                    or_(
                        # Changelogs related directly to group item.
                        and_(
                            item_changelog_model.model == item.__class__.__name__,
                            item_changelog_model.model_id == item.id
                        )
                    )
                ).\
                order_by(item_changelog_model.createtime.desc()).\
                limit(100).\
                all()
            self.response_context.update(item_changelog = item_changelog)


class ShowByNameView(ShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed group view by group name.
    """

    @classmethod
    def get_view_name(cls):
        return 'show_by_name'

    @classmethod
    def get_view_template(cls):
        return '{}/show.html'.format(cls.module_name)

    @property
    def search_by(self):
        return self.dbmodel.name


class CreateView(HTMLMixin, SQLAlchemyMixin, ItemCreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new groups.
    """

    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Create group')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Create new group')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Group <strong>%(item_id)s</strong> was successfully created.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext('Unable to create new group.')

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext('Canceled creating new group.')

    @staticmethod
    def get_item_form(item):
        return AdminCreateGroupForm()


class UpdateView(HTMLMixin, SQLAlchemyMixin, ItemUpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing groups.
    """

    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Update')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Update details of group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Update group details')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Group <strong>%(item_id)s</strong> was successfully updated.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to update group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled updating group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_item_form(item):
        admin = flask_login.current_user.has_role('admin')
        if not admin:
            form = UpdateGroupForm(obj = item)
        else:
            form = AdminUpdateGroupForm(db_item_id = item.id, obj = item)
        return form


class AddMemberView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for adding group members.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'addmember'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Add group member')

    @classmethod
    def get_view_icon(cls):
        return 'action-add-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Add user &quot;%(user_id)s&quot; to group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] in kwargs['item'].members:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].members.append(kwargs['other'])
        try:
            kwargs['item'].members_wanted.remove(kwargs['other'])
        except ValueError:
            pass
        if kwargs['other'].is_state_disabled():
            kwargs['other'].set_state_enabled()
            flask.current_app.send_infomail(
                'users.enable',
                account = kwargs['other']
            )

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully added as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to add user <strong>%(user_id)s</strong> as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled adding user <strong>%(user_id)s</strong> as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )


class RejectMemberView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for rejecting group membership reuests.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'rejectmember'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Reject group member')

    @classmethod
    def get_view_icon(cls):
        return 'action-rej-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Reject user`s &quot;%(user_id)s&quot; membership request for group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] not in kwargs['item'].members_wanted:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].members_wanted.remove(kwargs['other'])

    #---------------------------------------------------------------------------

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong> was successfully rejected.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to reject user`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled rejecting user`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )


class RemoveMemberView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for removing group members.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'removemember'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Remove group member')

    @classmethod
    def get_view_icon(cls):
        return 'action-rem-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Remove user &quot;%(user_id)s&quot; from group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] not in kwargs['item'].members:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].members.remove(kwargs['other'])

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully removed as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to remove user <strong>%(user_id)s</strong> as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled removing user <strong>%(user_id)s</strong> as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )


class AddManagerView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for adding group managers.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'addmanager'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Add group manager')

    @classmethod
    def get_view_icon(cls):
        return 'action-add-manager'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Add user &quot;%(user_id)s&quot; to group &quot;%(group_id)s&quot; as manager',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already manager.
        if kwargs['other'] in kwargs['item'].managers:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].managers.append(kwargs['other'])
        if kwargs['other'].is_state_disabled():
            kwargs['other'].set_state_enabled()
            flask.current_app.send_infomail(
                'users.enable',
                account = kwargs['other']
            )

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully added as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to add user <strong>%(user_id)s</strong> as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled adding user <strong>%(user_id)s</strong> as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )


class RemoveManagerView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for removing group managers.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'removemanager'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Remove group manager')

    @classmethod
    def get_view_icon(cls):
        return 'action-rem-manager'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Remove user &quot;%(user_id)s&quot; from group &quot;%(group_id)s&quot; as manager',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is not already manager.
        if kwargs['other'] not in kwargs['item'].managers:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        try:
            kwargs['item'].managers.remove(kwargs['other'])
        except ValueError:
            pass

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully removed as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to remove user <strong>%(user_id)s</strong> as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled removing user <strong>%(user_id)s</strong> as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['other'])),
            group_id = flask.escape(str(kwargs['item']))
        )


class EnableView(HTMLMixin, SQLAlchemyMixin, ItemEnableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for enabling existing groups.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Enable group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Group <strong>%(item_id)s</strong> was successfully enabled.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to enable group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled enabling group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


class DisableView(HTMLMixin, SQLAlchemyMixin, ItemDisableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for disabling groups.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Disable group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Group <strong>%(item_id)s</strong> was successfully disabled.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to disable group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled disabling group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


class DeleteView(HTMLMixin, SQLAlchemyMixin, ItemDeleteView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for deleting existing groups.
    """

    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_ADMIN]

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Delete group &quot;%(item)s&quot;',
            item = flask.escape(str(kwargs['item']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'Group <strong>%(item_id)s</strong> was successfully and permanently deleted.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to delete group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled deleting group <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


#-------------------------------------------------------------------------------


class GroupsBlueprint(VialBlueprint):
    """Pluggable module - user groups (*groups*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Group management')

    def register_app(self, app):

        def _fetch_my_groups():
            groups = {}
            for i in list(flask_login.current_user.memberships) + list(flask_login.current_user.managements):
                groups[str(i)] = i
            return list(sorted(groups.values(), key = str))

        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 50,
            view = ListView
        )
        app.menu_auth.add_entry(
            'submenudb',
            'my_groups',
            position = 20,
            title = lazy_gettext('My groups'),
            resptitle = True,
            icon = 'module-groups',
            align_right = True,
            entry_fetcher = _fetch_my_groups,
            entry_builder = lambda x, y: vial.menu.EndpointEntry(x, endpoint = 'groups.show', params = {'item': y}, title = x, icon = 'module-groups')
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = GroupsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ListView,          '/list')
    hbp.register_view_class(CreateView,        '/create')
    hbp.register_view_class(ShowView,          '/<int:item_id>/show')
    hbp.register_view_class(ShowByNameView,    '/<item_id>/show_by_name')
    hbp.register_view_class(UpdateView,        '/<int:item_id>/update')
    hbp.register_view_class(AddMemberView,     '/<int:item_id>/add_member/<int:other_id>')
    hbp.register_view_class(RejectMemberView,  '/<int:item_id>/reject_member/<int:other_id>')
    hbp.register_view_class(RemoveMemberView,  '/<int:item_id>/remove_member/<int:other_id>')
    hbp.register_view_class(AddManagerView,    '/<int:item_id>/add_manager/<int:other_id>')
    hbp.register_view_class(RemoveManagerView, '/<int:item_id>/remove_manager/<int:other_id>')
    hbp.register_view_class(EnableView,        '/<int:item_id>/enable')
    hbp.register_view_class(DisableView,       '/<int:item_id>/disable')
    hbp.register_view_class(DeleteView,        '/<int:item_id>/delete')

    return hbp

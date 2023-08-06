#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This file contains pluggable module for Vial application containing features
related to user account management. These features include:

* general user account listing
* detailed user account view
* creating new user accounts
* updating existing user accounts
* deleting existing user accounts
* enabling existing user accounts
* disabling existing user accounts
* adding group memberships
* removing group memberships
* rejecting group membership requests
"""


import flask
import flask_login
import flask_principal
import flask_mail
from flask_babel import gettext, lazy_gettext, force_locale
from sqlalchemy import or_

import vial.const
import vial.acl
from vial.app import VialBlueprint
from vial.view import ItemListView, ItemShowView, ItemCreateView, ItemUpdateView, ItemDeleteView, ItemEnableView, ItemDisableView, ItemObjectRelationView
from vial.view.mixin import HTMLMixin, SQLAlchemyMixin
from vial.blueprints.users.forms import CreateUserAccountForm, UpdateUserAccountForm, AdminUpdateUserAccountForm, UserSearchForm


BLUEPRINT_NAME = 'users'
"""Name of the blueprint as module global constant."""


class ListView(HTMLMixin, SQLAlchemyMixin, ItemListView):
    """
    General user account listing.
    """
    methods = ['GET']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('User management')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'create',
            endpoint = 'users.create',
            resptitle = True
        )
        return action_menu

    @classmethod
    def get_context_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'users.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'users.update',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'users.disable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'users.enable',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'users.delete',
            hidetitle = True
        )
        return action_menu

    @staticmethod
    def get_search_form(request_args):
        """
        Must return instance of :py:mod:`flask_wtf.FlaskForm` appropriate for
        searching given type of items.
        """
        roles = list(zip(flask.current_app.config['ROLES'], flask.current_app.config['ROLES']))
        return UserSearchForm(
            request_args,
            meta = {'csrf': False},
            choices_roles = roles
        )

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on text search string.
        if 'search' in form_args and form_args['search']:
            query = query\
                .filter(
                    or_(
                        model.login.like('%{}%'.format(form_args['search'])),
                        model.fullname.like('%{}%'.format(form_args['search'])),
                        model.email.like('%{}%'.format(form_args['search'])),
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
        # Adjust query based on user role selection.
        if 'role' in form_args and form_args['role']:
            if form_args['role'] == vial.const.NO_ROLE:
                query = query.filter(model.roles == [])
            else:
                query = query.filter(model.roles.any(form_args['role']))
        # Adjust query based on user membership selection.
        if 'membership' in form_args and form_args['membership']:
            query = query\
                .join(model.memberships)\
                .filter(model.memberships.any(id = form_args['membership'].id))
        # Adjust query based on user management selection.
        if 'management' in form_args and form_args['management']:
            query = query\
                .join(model.managements)\
                .filter(model.managements.any(id = form_args['management'].id))
        if 'sortby' in form_args and form_args['sortby']:
            sortmap = {
                'createtime.desc': lambda x, y: x.order_by(y.createtime.desc()),
                'createtime.asc': lambda x, y: x.order_by(y.createtime.asc()),
                'login.desc': lambda x, y: x.order_by(y.login.desc()),
                'login.asc': lambda x, y: x.order_by(y.login.asc()),
                'fullname.desc': lambda x, y: x.order_by(y.fullname.desc()),
                'fullname.asc': lambda x, y: x.order_by(y.fullname.asc()),
                'email.desc': lambda x, y: x.order_by(y.email.desc()),
                'email.asc': lambda x, y: x.order_by(y.email.asc()),
                'logintime.desc': lambda x, y: x.order_by(y.logintime.desc()),
                'logintime.asc': lambda x, y: x.order_by(y.logintime.asc()),
            }
            query = sortmap[form_args['sortby']](query, model)
        return query


class ShowView(HTMLMixin, SQLAlchemyMixin, ItemShowView):
    """
    Detailed user account view.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'action-show-user'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Show details of user account &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].login)
        )

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show user account details')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        # Each user must be able to view his/her account.
        permission_me = flask_principal.Permission(
            flask_principal.UserNeed(kwargs['item'].id)
        )
        # Managers of the groups the user is member of may view his/her account.
        needs = [vial.acl.ManagementNeed(x.id) for x in kwargs['item'].memberships]
        permission_mngr = flask_principal.Permission(*needs)
        return vial.acl.PERMISSION_POWER.can() or permission_mngr.can() or permission_me.can()

    @classmethod
    def get_action_menu(cls):
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'update',
            endpoint = 'users.update',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'disable',
            endpoint = 'users.disable',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'enable',
            endpoint = 'users.enable',
            resptitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'delete',
            endpoint = 'users.delete',
            resptitle = True
        )
        return action_menu

    def do_before_response(self, **kwargs):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        item = self.response_context['item']
        action_menu = vial.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'groups.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'submenu',
            'more',
            align_right = True,
            legend = gettext('More actions')
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_member',
            endpoint = 'groups.addmember'
        )
        action_menu.add_entry(
            'endpoint',
            'more.reject_member',
            endpoint = 'groups.rejectmember'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_member',
            endpoint = 'groups.removemember'
        )
        action_menu.add_entry(
            'endpoint',
            'more.add_manager',
            endpoint = 'groups.addmanager'
        )
        action_menu.add_entry(
            'endpoint',
            'more.remove_manager',
            endpoint = 'groups.removemanager'
        )
        action_menu.add_entry(
            'endpoint',
            'more.enable',
            endpoint = 'groups.enable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.disable',
            endpoint = 'groups.disable'
        )
        action_menu.add_entry(
            'endpoint',
            'more.update',
            endpoint = 'groups.update'
        )
        self.response_context.update(
            context_action_menu_groups = action_menu
        )

        if self.has_endpoint('changelogs.search'):
            self.response_context.update(
                context_action_menu_changelogs = self.get_endpoint_class(
                    'changelogs.search'
                ).get_context_action_menu()
            )

            if self.can_access_endpoint('users.update', item = item) and self.has_endpoint('changelogs.search'):
                item_changelog_model = self.get_model(vial.const.MODEL_ITEM_CHANGELOG)
                item_changelog = self.dbsession.query(item_changelog_model).\
                    filter(item_changelog_model.model == item.__class__.__name__).\
                    filter(item_changelog_model.model_id == item.id).\
                    order_by(item_changelog_model.createtime.desc()).\
                    limit(100).\
                    all()
                self.response_context.update(
                    item_changelog = item_changelog
                )

                user_changelog = self.dbsession.query(item_changelog_model).\
                    filter(item_changelog_model.author_id == item.id).\
                    order_by(item_changelog_model.createtime.desc()).\
                    limit(100).\
                    all()
                self.response_context.update(
                    user_changelog = user_changelog
                )


class MeView(ShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed user account view for currently logged-in user (profile page).
    """
    methods = ['GET']

    authentication = True

    authorization = [vial.acl.PERMISSION_ANY]

    @classmethod
    def get_view_name(cls):
        return 'me'

    @classmethod
    def get_view_icon(cls):
        return 'profile'

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('My account')

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(cls.get_view_endpoint())

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('My user account')

    @classmethod
    def get_view_template(cls):
        return '{}/show.html'.format(BLUEPRINT_NAME)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        return True

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
            'show',
            endpoint = '{}.me'.format(cls.module_name)
        )
        return action_menu

    def dispatch_request(self):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.

        Single item with given unique identifier will be retrieved from database
        and injected into template to be displayed to the user.
        """
        item_id = flask_login.current_user.get_id()
        item = self.dbquery().filter(self.dbmodel.id == item_id).first()
        if not item:
            self.abort(404)

        self.response_context.update(
            item_id = item_id,
            item = item,
            breadcrumbs_menu = self.get_breadcrumbs_menu(),
            action_menu = self.get_action_menu()
        )

        self.do_before_response()

        return self.generate_response()


class CreateView(HTMLMixin, SQLAlchemyMixin, ItemCreateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for creating new user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_icon(cls):
        return 'action-create-user'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Create new user account')

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User account <strong>%(item_id)s</strong> was successfully created.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext('Unable to create new user account.')

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext('Canceled creating new user account.')

    @staticmethod
    def get_item_form(item):
        #
        # Inject list of choices for supported locales and roles. Another approach
        # would be to let the form get the list on its own, however that would create
        # dependency on application object.
        #
        roles = list(zip(flask.current_app.config['ROLES'], flask.current_app.config['ROLES']))
        locales = list(flask.current_app.config['SUPPORTED_LOCALES'].items())

        return CreateUserAccountForm(
            choices_roles = roles,
            choices_locales = locales
        )


class UpdateView(HTMLMixin, SQLAlchemyMixin, ItemUpdateView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for updating existing user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_icon(cls):
        return 'action-update-user'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Update user account details')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Update details of user account &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].login)
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_me = flask_principal.Permission(
            flask_principal.UserNeed(kwargs['item'].id)
        )
        return vial.acl.PERMISSION_ADMIN.can() or permission_me.can()

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User account <strong>%(item_id)s</strong> was successfully updated.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to update user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled updating user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_item_form(item):
        #
        # Inject list of choices for supported locales and roles. Another approach
        # would be to let the form get the list on its own, however that would create
        # dependency on application object.
        #
        roles = list(zip(flask.current_app.config['ROLES'], flask.current_app.config['ROLES']))
        locales = list(flask.current_app.config['SUPPORTED_LOCALES'].items())

        admin = flask_login.current_user.has_role('admin')
        if not admin:
            form = UpdateUserAccountForm(
                choices_roles = roles,
                choices_locales = locales,
                obj = item
            )
        else:
            form = AdminUpdateUserAccountForm(
                choices_roles = roles,
                choices_locales = locales,
                db_item_id = item.id,
                obj = item
            )
        return form


class AddMembershipView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for adding group memberships.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'addmembership'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Add group membership')

    @classmethod
    def get_view_icon(cls):
        return 'action-add-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Add user &quot;%(user_id)s&quot; to group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['other'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] in kwargs['item'].memberships:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].memberships.append(kwargs['other'])
        try:
            kwargs['item'].memberships_wanted.remove(kwargs['other'])
        except ValueError:
            pass
        if kwargs['item'].is_state_disabled():
            kwargs['item'].set_state_enabled()
            flask.current_app.send_infomail(
                'users.enable',
                account = kwargs['item']
            )

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully added as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to add user <strong>%(user_id)s</strong> as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled adding user <strong>%(user_id)s</strong> as a member to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )


class RejectMembershipView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for rejecting group membership requests.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'rejectmembership'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Reject group membership')

    @classmethod
    def get_view_icon(cls):
        return 'action-rej-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Reject user`s &quot;%(user_id)s&quot; membership request for group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['other'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] not in kwargs['item'].memberships_wanted:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].memberships_wanted.remove(kwargs['other'])

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong> was successfully rejected.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to reject user`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled rejecting user`s <strong>%(user_id)s</strong> membership request for group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )


class RemoveMembershipView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for removing group memberships.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'removemembership'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Remove group membership')

    @classmethod
    def get_view_icon(cls):
        return 'action-rem-member'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Remove user &quot;%(user_id)s&quot; from group &quot;%(group_id)s&quot;',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['other'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already enabled.
        if kwargs['other'] not in kwargs['item'].memberships:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        try:
            kwargs['item'].memberships.remove(kwargs['other'])
        except ValueError:
            pass

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully removed as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to remove user <strong>%(user_id)s</strong> as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled removing user <strong>%(user_id)s</strong> as a member from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )


class AddManagementView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for adding group managements.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'addmanagement'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Add group management')

    @classmethod
    def get_view_icon(cls):
        return 'action-add-manager'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Add user &quot;%(user_id)s&quot; to group &quot;%(group_id)s&quot; as manager',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['other'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is already manager.
        if kwargs['other'] in kwargs['item'].managements:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        kwargs['item'].managements.append(kwargs['other'])
        if kwargs['item'].is_state_disabled():
            kwargs['item'].set_state_enabled()
            flask.current_app.send_infomail(
                'users.enable',
                account = kwargs['item']
            )

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully added as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to add user <strong>%(user_id)s</strong> as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled adding user <strong>%(user_id)s</strong> as a manager to group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )


class RemoveManagementView(HTMLMixin, SQLAlchemyMixin, ItemObjectRelationView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for removing group managements.
    """
    methods = ['GET','POST']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'removemanagement'

    @classmethod
    def get_view_title(cls, **kwargs):
        return gettext('Remove group management')

    @classmethod
    def get_view_icon(cls):
        return 'action-rem-manager'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Remove user &quot;%(user_id)s&quot; from group &quot;%(group_id)s&quot; as manager',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbmodel_other(self):
        return self.get_model(vial.const.MODEL_GROUP)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @classmethod
    def authorize_item_action(cls, **kwargs):
        permission_m = flask_principal.Permission(
            vial.acl.ManagementNeed(kwargs['other'].id)
        )
        return vial.acl.PERMISSION_POWER.can() or permission_m.can()

    @classmethod
    def validate_item_change(cls, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        # Reject item change in case given item is not already manager.
        if kwargs['other'] not in kwargs['item'].managements:
            return False
        return True

    @classmethod
    def change_item(cls, **kwargs):
        try:
            kwargs['item'].managements.remove(kwargs['other'])
        except ValueError:
            pass

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User <strong>%(user_id)s</strong> was successfully removed as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to remove user <strong>%(user_id)s</strong> as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled removing user <strong>%(user_id)s</strong> as a manager from group <strong>%(group_id)s</strong>.',
            user_id  = flask.escape(str(kwargs['item'])),
            group_id = flask.escape(str(kwargs['other']))
        )


class EnableView(HTMLMixin, SQLAlchemyMixin, ItemEnableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for enabling existing user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_icon(cls):
        return 'action-enable-user'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Enable user account &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].login)
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User account <strong>%(item_id)s</strong> was successfully enabled.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to enable user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled enabling user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @classmethod
    def inform_user(cls, account):
        """Send infomail about user account activation."""
        mail_locale = account.locale
        if not mail_locale:
            mail_locale = flask.current_app.config['BABEL_DEFAULT_LOCALE']

        with force_locale(mail_locale):
            msg = flask_mail.Message(
                gettext(
                    "[%(app_name)s] Account activation - %(item_id)s",
                    app_name = flask.current_app.config['APPLICATION_NAME'],
                    item_id = account.login
                ),
                recipients = [account.email],
                bcc = flask.current_app.config['EMAIL_ADMINS']
            )
            msg.body = flask.render_template(
                'users/email_activation.txt',
                account = account
            )
            flask.current_app.mailer.send(msg)

    def do_after_action(self, item):
        self.inform_user(item)


class DisableView(HTMLMixin, SQLAlchemyMixin, ItemDisableView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for disabling user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_POWER]

    @classmethod
    def get_view_icon(cls):
        return 'action-disable-user'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Disable user account &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].login)
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User account <strong>%(item_id)s</strong> was successfully disabled.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to disable user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled disabling user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


class DeleteView(HTMLMixin, SQLAlchemyMixin, ItemDeleteView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View for deleting existing user accounts.
    """
    methods = ['GET','POST']

    authentication = True

    authorization = [vial.acl.PERMISSION_ADMIN]

    @classmethod
    def get_view_icon(cls):
        return 'action-delete-user'

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Delete user account &quot;%(item)s&quot;',
            item = flask.escape(kwargs['item'].login)
        )

    @property
    def dbmodel(self):
        return self.get_model(vial.const.MODEL_USER)

    @property
    def dbchlogmodel(self):
        return self.get_model(vial.const.MODEL_ITEM_CHANGELOG)

    @staticmethod
    def get_message_success(**kwargs):
        return gettext(
            'User account <strong>%(item_id)s</strong> was successfully and permanently deleted.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_failure(**kwargs):
        return gettext(
            'Unable to delete user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )

    @staticmethod
    def get_message_cancel(**kwargs):
        return gettext(
            'Canceled deleting user account <strong>%(item_id)s</strong>.',
            item_id = flask.escape(str(kwargs['item']))
        )


#-------------------------------------------------------------------------------


class UsersBlueprint(VialBlueprint):
    """Pluggable module - user account management (*users*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('User account management')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'admin.{}'.format(BLUEPRINT_NAME),
            position = 40,
            group = lazy_gettext('Object management'),
            view = ListView
        )
        app.menu_auth.add_entry(
            'view',
            'my_account',
            position = 10,
            view = MeView,
            params = lambda: {'item': flask_login.current_user}
        )

        app.set_infomailer('users.enable', EnableView.inform_user)


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = UsersBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ListView,             '/list')
    hbp.register_view_class(CreateView,           '/create')
    hbp.register_view_class(ShowView,             '/<int:item_id>/show')
    hbp.register_view_class(MeView,               '/me')
    hbp.register_view_class(UpdateView,           '/<int:item_id>/update')
    hbp.register_view_class(AddMembershipView,    '/<int:item_id>/add_membership/<int:other_id>')
    hbp.register_view_class(RemoveMembershipView, '/<int:item_id>/remove_membership/<int:other_id>')
    hbp.register_view_class(RejectMembershipView, '/<int:item_id>/reject_membership/<int:other_id>')
    hbp.register_view_class(AddManagementView,    '/<int:item_id>/add_management/<int:other_id>')
    hbp.register_view_class(RemoveManagementView, '/<int:item_id>/remove_management/<int:other_id>')
    hbp.register_view_class(EnableView,           '/<int:item_id>/enable')
    hbp.register_view_class(DisableView,          '/<int:item_id>/disable')
    hbp.register_view_class(DeleteView,           '/<int:item_id>/delete')

    return hbp

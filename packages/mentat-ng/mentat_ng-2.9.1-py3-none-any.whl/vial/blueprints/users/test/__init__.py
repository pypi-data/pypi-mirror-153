#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`vial.blueprints.users`.
"""


import sys
import unittest

import vial.const
import vial.db
import vial.test
import vial.test.fixtures
import vial.test.runner
from vial.test import VialTestCase, ItemCreateVialTestCase
from vial.test.runner import TestRunnerMixin
from vial.blueprints.users.test.utils import UsersTestCaseMixin

_IS_NOSE = sys.argv[0].endswith('nosetests')

@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersListTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.list`` endpoint."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """
        Test access as user ``user``.

        Only power user is able to list all available user accounts.
        """
        self._attempt_fail_list()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """
        Test access as user ``developer``.

        Only power user is able to list all available user accounts.
        """
        self._attempt_fail_list()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """
        Test access as user ``maintainer``.

        Only power user is able to list all available user accounts.
        """
        self._attempt_succeed_list()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """
        Test access as user ``admin``.

        Only power user is able to list all available user accounts.
        """
        self._attempt_succeed_list()


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersShowOwnTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """
    Class for testing ``users.show`` endpoint: access to user`s own accounts.

    Each user must be able to access his own account.
    """

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_succeed_show(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed_show(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed_show(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed_show(vial.const.ROLE_ADMIN)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersShowOtherTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.show`` endpoint: access to other user`s accounts."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user_developer(self):
        """
        Test access to 'developer' account as user 'user'.

        Regular user may view only his own account.
        """
        self._attempt_fail_show(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user_maintainer(self):
        """
        Test access to 'maintainer' account as user 'user'.

        Regular user may view only his own account.
        """
        self._attempt_fail_show(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_03_as_user_admin(self):
        """
        Test access to 'admin' account as user 'user'.

        Regular user may view only his own account.
        """
        self._attempt_fail_show(vial.const.ROLE_ADMIN)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_04_as_developer_user(self):
        """
        Test access to 'user' account as user 'developer'.

        Developer should be able to access because he is a manager of group of
        which all other users are members.
        """
        self._attempt_succeed_show(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_05_as_developer_maintainer(self):
        """
        Test access to 'maintainer' account as user 'developer'.

        Developer should be able to access because he is a manager of group of
        which all other users are members.
        """
        self._attempt_succeed_show(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_06_as_developer_admin(self):
        """
        Test access to 'admin' account as user 'developer'.

        Developer should be able to access because he is a manager of group of
        which all other users are members.
        """
        self._attempt_succeed_show(vial.const.ROLE_ADMIN)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_07_as_maintainer_user(self):
        """
        Test access to 'user' account as user 'maintainer'.

        Maintainer should be allowed access, because he is a power user like admin.
        """
        self._attempt_succeed_show(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_08_as_maintainer_developer(self):
        """
        Test access to 'developer' account as user 'maintainer'.

        Maintainer should be allowed access, because he is a power user like admin.
        """
        self._attempt_succeed_show(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_09_as_maintainer_admin(self):
        """
        Test access to 'maintainer' account as user 'maintainer'.

        Maintainer should be allowed access, because he is a power user like admin.
        """
        self._attempt_succeed_show(vial.const.ROLE_MAINTAINER)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_10_as_admin_user(self):
        """Test access to 'user' account as user 'admin'."""
        self._attempt_succeed_show(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_11_as_admin_developer(self):
        """Test access to 'developer' account as user 'admin'."""
        self._attempt_succeed_show(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_12_as_admin_maintainer(self):
        """Test access to 'maintainer' account as user 'admin'."""
        self._attempt_succeed_show(vial.const.ROLE_MAINTAINER)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersCreateTestCase(UsersTestCaseMixin, TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``users.create`` endpoint."""

    user_data_fixture = [
        ('login', 'test'),
        ('fullname', 'Test User'),
        ('email', 'test.user@domain.org'),
        ('enabled', True)
    ]

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail_create()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail_create()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed_create(self.user_data_fixture)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed_create(self.user_data_fixture)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersUpdateOwnTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.update`` endpoint: access to user`s own accounts."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_succeed_update(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed_update(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed_update(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed_update(vial.const.ROLE_ADMIN)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersUpdateOtherTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.update`` endpoint: access to other user`s accounts."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user_developer(self):
        """Test access to 'developer' account as user 'user'."""
        self._attempt_fail_update(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user_maintainer(self):
        """Test access to 'maintainer' account as user 'user'."""
        self._attempt_fail_update(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_03_as_user_admin(self):
        """Test access to 'admin' account as user 'user'."""
        self._attempt_fail_update(vial.const.ROLE_ADMIN)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_04_as_developer_user(self):
        """Test access to 'user' account as user 'developer'."""
        self._attempt_fail_update(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_05_as_developer_maintainer(self):
        """Test access to 'maintainer' account as user 'developer'."""
        self._attempt_fail_update(vial.const.ROLE_MAINTAINER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_06_as_developer_admin(self):
        """Test access to 'admin' account as user 'developer'."""
        self._attempt_fail_update(vial.const.ROLE_ADMIN)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_07_as_maintainer_user(self):
        """Test access to 'user' account as user 'maintainer'."""
        self._attempt_fail_update(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_08_as_maintainer_developer(self):
        """Test access to 'developer' account as user 'maintainer'."""
        self._attempt_fail_update(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_09_as_maintainer_admin(self):
        """Test access to 'admin' account as user 'maintainer'."""
        self._attempt_fail_update(vial.const.ROLE_ADMIN)

    #--------------------------------------------------------------------------

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_10_as_admin_user(self):
        """Test access to 'user' account as user 'admin'."""
        self._attempt_succeed_update(vial.const.ROLE_USER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_11_as_admin_developer(self):
        """Test access to 'developer' account as user 'admin'."""
        self._attempt_succeed_update(vial.const.ROLE_DEVELOPER)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_12_as_admin_maintainer(self):
        """Test access to 'maintainer' account as user 'admin'."""
        self._attempt_succeed_update(vial.const.ROLE_MAINTAINER)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersEnableDisableTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.enable`` and ``users.disable`` endpoint."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail_disable(uname)
            self._attempt_fail_enable(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail_disable(uname)
            self._attempt_fail_enable(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_succeed_disable(uname)
            self._attempt_succeed_enable(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER
            ):
            self._attempt_succeed_disable(uname)
            self._attempt_succeed_enable(uname)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersAddRemRejMembershipTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``users.add_membership``, ``users.reject_membership`` and ``users.remove_membership`` endpoint."""

    def _attempt_fail(self, uname, gname):
        with self.app.app_context():
            uid = self.user_id(uname)
            gid = self.group_id(gname)
        self.assertGetURL(
            '/users/{}/remove_membership/{}'.format(uid, gid),
            403
        )
        self.assertGetURL(
            '/users/{}/reject_membership/{}'.format(uid, gid),
            403
        )
        self.assertGetURL(
            '/users/{}/add_membership/{}'.format(uid, gid),
            403
        )

    def _attempt_succeed(self, uname, gname, print_response = False):
        # Additional test preparations.
        with self.app.app_context():
            uid = self.user_id(uname)
            gid = self.group_id(gname)
            self.user_enabled(uname, False)
        self.mailbox_monitoring('on')

        #
        # First check the removal of existing membership.
        #
        self.assertGetURL(
            '/users/{}/remove_membership/{}'.format(uid, gid),
            200,
            [
                b'Are you really sure you want to remove user'
            ],
            print_response
        )
        self.assertPostURL(
            '/users/{}/remove_membership/{}'.format(uid, gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully removed as a member from group'
            ],
            print_response
        )

        #
        # Add user back to group.
        #
        self.assertGetURL(
            '/users/{}/add_membership/{}'.format(uid, gid),
            200,
            [
                b'Are you really sure you want to add user'
            ],
            print_response
        )
        self.assertPostURL(
            '/users/{}/add_membership/{}'.format(uid, gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully added as a member to group'
            ],
            print_response
        )
        self.assertMailbox(
            {
                'subject': [
                    '[{}] Account activation - {}'.format(self.app.config['APPLICATION_NAME'], uname)
                ],
                'sender': [
                    'root@unittest'
                ],
                'recipients': [
                    ['{}@bogus-domain.org'.format(uname)]
                ],
                'cc': [[]],
                'bcc': [['admin@unittest']]
            }
        )
        self.mailbox_clear()

        # Additional test preparations.
        with self.app.app_context():
            uobj = self.user_get(uname)
            gobj = self.group_get(gname)
            uid = uobj.id
            gid = gobj.id
            uobj.enabled = False
            uobj.memberships.remove(gobj)
            uobj.memberships_wanted.append(gobj)
            self.user_save(uobj)

        #
        # Check membership request rejection feature.
        #
        self.assertGetURL(
            '/users/{}/reject_membership/{}'.format(uid, gid),
            200,
            [
                b'Are you really sure you want to reject membership request of user'
            ],
            print_response
        )
        self.assertPostURL(
            '/users/{}/reject_membership/{}'.format(uid, gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully rejected.'
            ],
            print_response
        )
        self.mailbox_monitoring('off')

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail(uname, vial.test.fixtures.DEMO_GROUP_A)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_succeed(uname, vial.test.fixtures.DEMO_GROUP_A)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_succeed(uname, vial.test.fixtures.DEMO_GROUP_A)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER
            ):
            self._attempt_succeed(uname, vial.test.fixtures.DEMO_GROUP_A)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class UsersDeleteTestCase(UsersTestCaseMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``users.delete`` endpoint."""

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail_delete(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail_delete(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER,
                vial.const.ROLE_ADMIN
            ):
            self._attempt_fail_delete(uname)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        for uname in (
                vial.const.ROLE_USER,
                vial.const.ROLE_DEVELOPER,
                vial.const.ROLE_MAINTAINER
            ):
            self._attempt_succeed_delete(uname)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

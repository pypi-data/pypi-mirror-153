#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`vial.blueprints.groups`.
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


_IS_NOSE = sys.argv[0].endswith('nosetests')

@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsListTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``groups.list`` endpoint."""

    def _attempt_fail(self):
        self.assertGetURL(
            '/groups/list',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/groups/list',
            200,
            [
                b'View details of group &quot;DEMO_GROUP_A&quot;',
                b'View details of group &quot;DEMO_GROUP_B&quot;',
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user ``user``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_succeed()


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsShowTestCase(TestRunnerMixin, VialTestCase):
    """Base class for testing ``groups.show`` and ``groups.show_by_name`` endpoints."""

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/show'.format(gid),
            403
        )
        self.assertGetURL(
            '/groups/{}/show_by_name'.format(gname),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/show'.format(gid),
            200,
            [
                '<h3>{} '.format(gname).encode('utf8'),
                b'<strong>Group created:</strong>'
            ]
        )
        self.assertGetURL(
            '/groups/{}/show_by_name'.format(gname),
            200,
            [
                '<h3>{} '.format(gname).encode('utf8'),
                b'<strong>Group created:</strong>'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """
        Test access as user 'user'.

        Only power user is able to view all available groups.
        """
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """
        Test access as user 'developer'.

        Only power user is able to view all available groups.
        """
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """
        Test access as user 'maintainer'.

        Only power user is able to view all available groups.
        """
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """
        Test access as user 'admin'.

        Only power user is able to view all available groups.
        """
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsCreateTestCase(TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``groups.create`` endpoint."""

    group_data_fixture = [
        ('name', 'TEST_GROUP'),
        ('description', 'Test group for unit testing purposes.'),
        ('enabled', True)
    ]

    def _attempt_fail(self):
        self.assertGetURL(
            '/groups/create',
            403
        )

    def _attempt_succeed(self):
        self.assertCreate(
            self.group_model(),
            '/groups/create',
            self.group_data_fixture,
            [
                b'Group <strong>TEST_GROUP</strong> was successfully created.'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed()


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsUpdateTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``groups.update`` endpoint."""

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/update'.format(gid),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/update'.format(gid),
            200,
            [
                b'Update group details'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_04_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_05_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_06_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsEnableDisableTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``groups.enable`` and ``groups.disable`` endpoint."""

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/disable'.format(gid),
            403
        )
        self.assertGetURL(
            '/groups/{}/enable'.format(gid),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/disable'.format(gid),
            200,
            [
                b'Are you really sure you want to disable following item:'
            ]
        )
        self.assertPostURL(
            '/groups/{}/disable'.format(gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully disabled.'
            ]
        )
        self.assertGetURL(
            '/groups/{}/enable'.format(gid),
            200,
            [
                b'Are you really sure you want to enable following item:'
            ]
        )
        self.assertPostURL(
            '/groups/{}/enable'.format(gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully enabled.'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)


@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class GroupsAddRemRejMemberTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``groups.add_member``, ``groups.reject_member`` and ``groups.remove_member`` endpoint."""

    def _attempt_fail(self, uname, gname):
        with self.app.app_context():
            uid = self.user_id(uname)
            gid = self.group_id(gname)
        self.assertGetURL(
            '/groups/{}/remove_member/{}'.format(gid, uid),
            403
        )
        self.assertGetURL(
            '/groups/{}/reject_member/{}'.format(gid, uid),
            403
        )
        self.assertGetURL(
            '/groups/{}/add_member/{}'.format(gid, uid),
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
            '/groups/{}/remove_member/{}'.format(gid, uid),
            200,
            [
                b'Are you really sure you want to remove user'
            ],
            print_response
        )
        self.assertPostURL(
            '/groups/{}/remove_member/{}'.format(gid, uid),
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
            '/groups/{}/add_member/{}'.format(gid, uid),
            200,
            [
                b'Are you really sure you want to add user'
            ],
            print_response
        )
        self.assertPostURL(
            '/groups/{}/add_member/{}'.format(gid, uid),
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
            '/groups/{}/reject_member/{}'.format(gid, uid),
            200,
            [
                b'Are you really sure you want to reject membership request of user'
            ],
            print_response
        )
        self.assertPostURL(
            '/groups/{}/reject_member/{}'.format(gid, uid),
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
class GroupsDeleteTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``groups.delete`` endpoint."""

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/delete'.format(gid),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/groups/{}/delete'.format(gid),
            200,
            [
                b'Are you really sure you want to permanently remove following item:'
            ]
        )
        self.assertPostURL(
            '/groups/{}/delete'.format(gid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully and permanently deleted.'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_fail(vial.test.fixtures.DEMO_GROUP_B)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_B)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

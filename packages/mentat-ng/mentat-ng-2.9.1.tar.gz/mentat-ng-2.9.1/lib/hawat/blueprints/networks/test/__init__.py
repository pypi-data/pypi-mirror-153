#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`hawat.blueprints.networks`.
"""


import unittest

from mentat.datatype.sqldb import NetworkModel

import vial.const
import vial.test
import vial.test.fixtures
import vial.db
from vial.test import VialTestCase, ItemCreateVialTestCase
from hawat.test.runner import TestRunnerMixin


class NetworkTestMixin:
    """
    Mixin class for network specific tests.
    """

    @staticmethod
    def _nname(gname):
        return 'NET_{}'.format(gname)

    def network_get(self, network_name, with_app_context = False):
        """
        Get given network.
        """
        if not with_app_context:
            return vial.db.db_session().query(NetworkModel).filter(NetworkModel.netname == network_name).one_or_none()
        with self.app.app_context():
            return vial.db.db_session().query(NetworkModel).filter(NetworkModel.netname == network_name).one_or_none()

    def network_save(self, network_object, with_app_context = False):
        """
        Update given network.
        """
        if not with_app_context:
            vial.db.db_session().add(network_object)
            vial.db.db_session().commit()
        with self.app.app_context():
            vial.db.db_session().add(network_object)
            vial.db.db_session().commit()

    def network_id(self, network_type, with_app_context = False):
        """
        Get ID of given network.
        """
        if not with_app_context:
            fobj = self.network_get(network_type)
            return fobj.id
        with self.app.app_context():
            fobj = self.network_get(network_type)
            return fobj.id


class NetworksListTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``networks.list`` endpoint."""

    def _attempt_fail(self):
        self.assertGetURL(
            '/networks/list',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/networks/list',
            200,
            [
                b'View details of network record &quot;NET_DEMO_GROUP_A&quot;',
                b'View details of network record &quot;NET_DEMO_GROUP_B&quot;',
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


class NetworksShowTestCase(NetworkTestMixin, TestRunnerMixin, VialTestCase):
    """Base class for testing ``networks.show`` endpoint."""

    def _attempt_fail(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/show'.format(nid),
            403
        )

    def _attempt_succeed(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/show'.format(nid),
            200,
            [
                '<h3>{}</h3>'.format(nname).encode('utf8'),
                b'<strong>Network created:</strong>'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """
        Test access as user 'user'.

        Only power user is able to view all available networks.
        """
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """
        Test access as user 'developer'.

        Only power user is able to view all available networks.
        """
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """
        Test access as user 'maintainer'.

        Only power user is able to view all available networks.
        """
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """
        Test access as user 'admin'.

        Only power user is able to view all available networks.
        """
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))


class NetworksCreateTestCase(NetworkTestMixin, TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``networks.create`` endpoint."""

    network_data_fixture = [
        ('group', 1),
        ('netname', 'TEST_NETWORK'),
        ('network', '191.168.1.0/24'),
        ('description', 'Test network for unit testing purposes.')
    ]

    def _attempt_fail(self):
        self.assertGetURL(
            '/networks/create',
            403
        )

    def _attempt_succeed(self):
        self.assertCreate(
            NetworkModel,
            '/networks/create',
            self.network_data_fixture,
            [
                b'Network record <strong>TEST_NETWORK</strong> for group ',
                b' was successfully created.'
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


class NetworksCreateForTestCase(NetworkTestMixin, TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``networks.createfor`` endpoint."""

    network_data_fixture = [
        ('netname', 'TEST_NETWORK'),
        ('network', '191.168.1.0/24'),
        ('description', 'Test network for unit testing purposes.')
    ]

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/networks/createfor/{}'.format(gid),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertCreate(
            NetworkModel,
            '/networks/createfor/{}'.format(gid),
            self.network_data_fixture,
            [
                b'Network record <strong>TEST_NETWORK</strong> for group ',
                b' was successfully created.'
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
        self._attempt_succeed(vial.test.fixtures.DEMO_GROUP_A)
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


class NetworksUpdateTestCase(NetworkTestMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``networks.update`` endpoint."""

    def _attempt_fail(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/update'.format(nid),
            403
        )

    def _attempt_succeed(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/update'.format(nid),
            200,
            [
                b'Update network record details'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_04_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_05_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_06_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))


class NetworksDeleteTestCase(NetworkTestMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``networks.delete`` endpoint."""

    def _attempt_fail(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/delete'.format(nid),
            403
        )

    def _attempt_succeed(self, nname):
        nid = self.network_id(nname, True)
        self.assertGetURL(
            '/networks/{}/delete'.format(nid),
            200,
            [
                b'Are you really sure you want to permanently remove following item:'
            ]
        )
        self.assertPostURL(
            '/networks/{}/delete'.format(nid),
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
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._nname(vial.test.fixtures.DEMO_GROUP_B))


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

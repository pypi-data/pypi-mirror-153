#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`hawat.blueprints.filters`.
"""


import unittest

from mentat.datatype.sqldb import FilterModel

import vial.const
import vial.test
import vial.test.fixtures
import vial.db
from vial.test import VialTestCase, ItemCreateVialTestCase
from hawat.test.runner import TestRunnerMixin


class FilterTestMixin:
    """
    Mixin class for filter specific tests.
    """

    @staticmethod
    def _fname(gname):
        return 'FLT_{}'.format(gname)

    def filter_get(self, filter_name, with_app_context = False):
        """
        Get given filter.
        """
        if not with_app_context:
            return vial.db.db_session().query(FilterModel).filter(FilterModel.name == filter_name).one_or_none()
        with self.app.app_context():
            return vial.db.db_session().query(FilterModel).filter(FilterModel.name == filter_name).one_or_none()

    def filter_save(self, filter_object, with_app_context = False):
        """
        Update given filter.
        """
        if not with_app_context:
            vial.db.db_session().add(filter_object)
            vial.db.db_session().commit()
        with self.app.app_context():
            vial.db.db_session().add(filter_object)
            vial.db.db_session().commit()

    def filter_id(self, filter_type, with_app_context = False):
        """
        Get ID of given filter.
        """
        if not with_app_context:
            fobj = self.filter_get(filter_type)
            return fobj.id
        with self.app.app_context():
            fobj = self.filter_get(filter_type)
            return fobj.id


class FiltersListTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``filters.list`` endpoint."""

    def _attempt_fail(self):
        self.assertGetURL(
            '/filters/list',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/filters/list',
            200,
            [
                b'View details of reporting filter &quot;FLT_DEMO_GROUP_A&quot;',
                b'View details of reporting filter &quot;FLT_DEMO_GROUP_B&quot;',
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


class FiltersShowTestCase(FilterTestMixin, TestRunnerMixin, VialTestCase):
    """Base class for testing ``filters.show`` endpoint."""

    def _attempt_fail(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/show'.format(fid),
            403
        )

    def _attempt_succeed(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/show'.format(fid),
            200,
            [
                '<h3>{}</h3>'.format(fname).encode('utf8'),
                b'<strong>Filter created:</strong>'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """
        Test access as user 'user'.

        Only power user is able to view all available filters.
        """
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """
        Test access as user 'developer'.

        Only power user is able to view all available filters.
        """
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """
        Test access as user 'maintainer'.

        Only power user is able to view all available filters.
        """
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """
        Test access as user 'admin'.

        Only power user is able to view all available filters.
        """
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))


class FiltersCreateTestCase(FilterTestMixin, TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``filters.create`` endpoint."""

    filter_data_fixture = [
        ('name', 'TEST_FILTER'),
        ('type', 'basic'),
        ('group', 1),
        ('description', 'Test filter for unit testing purposes.'),
        ('filter', 'Category IN ["Recon.Scanning"] AND Target.IP4 IN ["191.168.1.1", "10.0.0.1"]'),
        ('enabled', True)
    ]

    def _attempt_fail(self):
        self.assertGetURL(
            '/filters/create',
            403
        )

    def _attempt_succeed(self):
        self.assertCreate(
            FilterModel,
            '/filters/create',
            self.filter_data_fixture,
            [
                b'Reporting filter <strong>TEST_FILTER</strong> for group ',
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


class FiltersCreateForTestCase(FilterTestMixin, TestRunnerMixin, ItemCreateVialTestCase):
    """Class for testing ``filters.createfor`` endpoint."""

    filter_data_fixture = [
        ('name', 'TEST_FILTER'),
        ('type', 'basic'),
        ('description', 'Test filter for unit testing purposes.'),
        ('filter', 'Category IN ["Recon.Scanning"] AND Target.IP4 IN ["191.168.1.1", "10.0.0.1"]'),
        ('enabled', True)
    ]

    def _attempt_fail(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertGetURL(
            '/filters/createfor/{}'.format(gid),
            403
        )

    def _attempt_succeed(self, gname):
        gid = self.group_id(gname, with_app_ctx = True)
        self.assertCreate(
            FilterModel,
            '/filters/createfor/{}'.format(gid),
            self.filter_data_fixture,
            [
                b'Reporting filter <strong>TEST_FILTER</strong> for group ',
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


class FiltersUpdateTestCase(FilterTestMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``filters.update`` endpoint."""

    def _attempt_fail(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/update'.format(fid),
            403
        )

    def _attempt_succeed(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/update'.format(fid),
            200,
            [
                b'Update reporting filter details'
            ]
        )

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_04_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_05_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_06_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))


class FiltersEnableDisableTestCase(FilterTestMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``filters.enable`` and ``filters.disable`` endpoint."""

    def _attempt_fail(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/disable'.format(fid),
            403
        )
        self.assertGetURL(
            '/filters/{}/enable'.format(fid),
            403
        )

    def _attempt_succeed(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/disable'.format(fid),
            200,
            [
                b'Are you really sure you want to disable following item:'
            ]
        )
        self.assertPostURL(
            '/filters/{}/disable'.format(fid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully disabled.'
            ]
        )
        self.assertGetURL(
            '/filters/{}/enable'.format(fid),
            200,
            [
                b'Are you really sure you want to enable following item:'
            ]
        )
        self.assertPostURL(
            '/filters/{}/enable'.format(fid),
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
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))


class FiltersDeleteTestCase(FilterTestMixin, TestRunnerMixin, VialTestCase):
    """Class for testing ``filters.delete`` endpoint."""

    def _attempt_fail(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/delete'.format(fid),
            403
        )

    def _attempt_succeed(self, fname):
        fid = self.filter_id(fname, True)
        self.assertGetURL(
            '/filters/{}/delete'.format(fid),
            200,
            [
                b'Are you really sure you want to permanently remove following item:'
            ]
        )
        self.assertPostURL(
            '/filters/{}/delete'.format(fid),
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
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_fail(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_A))
        self._attempt_succeed(self._fname(vial.test.fixtures.DEMO_GROUP_B))


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

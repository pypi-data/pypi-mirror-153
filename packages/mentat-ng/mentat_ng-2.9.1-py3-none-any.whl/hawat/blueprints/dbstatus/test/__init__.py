#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`hawat.blueprints.dbstatus`.
"""


import unittest

import vial.const
import vial.test
import vial.db
from vial.test import VialTestCase
from hawat.test.runner import TestRunnerMixin


class DBStatusViewTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``dbstatus.view`` endpoint."""

    def _attempt_fail_redirect(self):
        self.assertGetURL(
            '/dbstatus/view',
            302,
            [
                b'Redirecting...',
                b'login?next='
            ],
            follow_redirects = False
        )

    def _attempt_fail(self):
        self.assertGetURL(
            '/dbstatus/view',
            403,
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/dbstatus/view',
            200,
            [
                b'Database status',
                b'<strong>Event database</strong>',
                b'<strong>PostgreSQL</strong>',
            ]
        )

    def test_01_as_anonymous(self):
        """Test access as anonymous user."""
        self._attempt_fail_redirect()

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user(self):
        """Test access as user ``user``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_03_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_04_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_05_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_succeed()


class DBStatusMyQueriesTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``dbstatus.queries_my`` endpoint."""

    def _attempt_fail(self):
        self.assertGetURL(
            '/dbstatus/query/my',
            302,
            [
                b'Redirecting...',
                b'login?next='
            ],
            follow_redirects = False
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/dbstatus/query/my',
            200,
            [
                b'My currently running queries'
            ]
        )

    def test_01_as_anonymous(self):
        """Test access as anonymous user."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user(self):
        """Test access as user ``user``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_03_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_04_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_05_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_succeed()


class DBStatusDashboardTestCase(TestRunnerMixin, VialTestCase):
    """Class for testing ``dbstatus.dashboard`` endpoint."""

    def _attempt_fail_redirect(self):
        self.assertGetURL(
            '/dbstatus/dashboard',
            302,
            [
                b'Redirecting...',
                b'login?next='
            ],
            follow_redirects = False
        )

    def _attempt_fail(self):
        self.assertGetURL(
            '/dbstatus/dashboard',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/dbstatus/dashboard',
            200,
            [
                b'Object management dashboards'
            ]
        )

    def test_01_as_anonymous(self):
        """Test access as anonymous user."""
        self._attempt_fail_redirect()

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user(self):
        """Test access as user ``user``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_03_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_04_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_05_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_succeed()


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

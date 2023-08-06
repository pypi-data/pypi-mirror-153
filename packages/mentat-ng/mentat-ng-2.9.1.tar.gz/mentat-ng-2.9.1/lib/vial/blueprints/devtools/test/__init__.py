#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`vial.blueprints.devtools`.
"""


import sys
import unittest

import vial.const
import vial.test
import vial.db
from vial.test import VialTestCase
from vial.test.runner import TestRunnerMixin


_IS_NOSE = sys.argv[0].endswith('nosetests')

@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class ConfigTestCase(TestRunnerMixin, VialTestCase):
    """
    Class for testing ``devtools.config`` endpoint.

    This endpoint is for developers only.
    """

    def _attempt_fail(self):
        self.assertGetURL(
            '/devtools/config',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/devtools/config',
            200,
            [
                b'View system configuration',
                b'Enabled modules',
                b'Endpoint permissions',
                b'Timezone settings',
                b'Configuration'
            ]
        )

    def test_01_as_anonymous(self):
        """Test access as anonymous user."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_as_user(self):
        """Test access as user ``user``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_03_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_succeed()

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_04_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_fail()

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_05_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_fail()


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

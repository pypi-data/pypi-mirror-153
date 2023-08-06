#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`vial.blueprints.auth`.
"""


import sys
import unittest

from vial.test import VialTestCase
from vial.test.runner import TestRunnerMixin


_IS_NOSE = sys.argv[0].endswith('nosetests')

@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class AuthTestCase(TestRunnerMixin, VialTestCase):
    """
    Class for testing :py:mod:`vial.blueprints.auth` blueprint.
    """

    def test_01_login(self):
        """
        Test login directional page.
        """
        response = self.client.get(
            '/auth/login',
            follow_redirects = True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Following is a list of all available user login options. Please choose the one appropriate for you.' in response.data)

    def test_02_register(self):
        """
        Test registration directional page.
        """
        response = self.client.get(
            '/auth/register',
            follow_redirects = True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Following is a list of all available user account registration options. Please choose the one most suitable for your needs.' in response.data)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

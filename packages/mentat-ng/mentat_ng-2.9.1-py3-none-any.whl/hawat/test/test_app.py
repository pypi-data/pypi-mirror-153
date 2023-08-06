#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Basic proof of concept for Hawat unit tests.
"""


import unittest
#import logging

from mentat.datatype.sqldb import UserModel, GroupModel

import vial.const
import vial.test
import vial.db
from vial.test import VialTestCase
from hawat.test.runner import TestRunnerMixin


#logging.disable(logging.CRITICAL+1000)


class AppTestCase(TestRunnerMixin, VialTestCase):
    """
    Class for testing :py:class:`hawat.base.HawatApp` application.
    """

    def test_testenv(self):
        """
        Test the test environment.
        """
        with self.app.app_context():
            result_users = vial.db.db_session().query(UserModel).order_by(UserModel.login).all()
            self.assertEqual(
                len(result_users),
                4
            )
            self.assertEqual(
                list(map(lambda x: x.login, result_users)),
                ['admin', 'developer', 'maintainer', 'user']
            )
            result_groups = vial.db.db_session().query(GroupModel).order_by(GroupModel.name).all()
            self.assertEqual(
                len(result_groups),
                2
            )
            self.assertEqual(
                list(map(lambda x: x.name, result_groups)),
                ['DEMO_GROUP_A', 'DEMO_GROUP_B']
            )

    def test_main_page(self):
        """
        Test application homepage.
        """
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Welcome!' in response.data)

    def test_login_dev(self):
        """
        Test login/logout with *auth_dev* module.
        """
        response = self.login_dev(vial.const.ROLE_ADMIN)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

    def test_modules_mgmt(self):
        """
        Basic tests of various pluggable modules.
        """
        modlist = ('/users/list', '/groups/list', '/filters/list', '/networks/list')

        response = self.login_dev(vial.const.ROLE_ADMIN)
        self.assertEqual(response.status_code, 200)
        for mod in modlist:
            response = self.client.get(mod, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_modules_mgmt_user(self):
        """
        Basic tests of various pluggable modules.
        """
        modlist = ('/users/list', '/groups/list', '/filters/list', '/networks/list')
        for mod in modlist:
            response = self.client.get(mod, follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_modules_mgmt_developer(self):
        """
        Basic tests of various pluggable modules.
        """
        modlist = ('/users/list', '/groups/list', '/filters/list', '/networks/list')
        for mod in modlist:
            response = self.client.get(mod, follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    @vial.test.do_as_user_decorator(vial.const.ROLE_MAINTAINER)
    def test_modules_mgmt_maintainer(self):
        """
        Basic tests of various pluggable modules.
        """
        modlist = ('/users/list', '/groups/list', '/filters/list', '/networks/list')
        for mod in modlist:
            response = self.client.get(mod, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_modules_mgmt_admin(self):
        """
        Basic tests of various pluggable modules.
        """
        modlist = ('/users/list', '/groups/list', '/filters/list', '/networks/list')
        for mod in modlist:
            response = self.client.get(mod, follow_redirects=True)
            self.assertEqual(response.status_code, 200)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base library for Hawat unit tests.
"""

from vial.test import RegistrationVialTestCase

class RegistrationHawatTestCase(RegistrationVialTestCase):
    user_fixture = {
        'apikey': None,
        'email': 'test.user@domain.org',
        'enabled': False,
        'fullname': 'Test User',
        'id': 5,
        'locale': None,
        'login': 'test',
        'logintime': 'None',
        'managements': [],
        'memberships': [],
        'memberships_wanted': [],
        'organization': 'TEST, org.',
        'roles': ['user'],
        'timezone': None
    }

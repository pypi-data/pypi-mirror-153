#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit test module for testing the :py:mod:`mentat.daemon.piper` module.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import unittest

#import mentat.daemon.piper


class TestMentatBackupScript(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_basic(self):
        """Perform the basic operativity tests."""
        self.assertTrue(True)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

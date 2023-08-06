#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


import unittest

import os
import time
import shutil
import random

import mentat.stats.rrd


RRD_STATS_DIR   = '/var/tmp/utest_rrdstats'
RRD_REPORTS_DIR = '/var/tmp'
TEST_DATA_SIZE  = 5000
TIME_START      = int(time.time())
TIME_START      = TIME_START - (TIME_START % mentat.stats.rrd.DFLT_STEP) - (TEST_DATA_SIZE * mentat.stats.rrd.DFLT_STEP)


class TestMentatStatsRrd(unittest.TestCase):

    #
    # Turn on more verbose output, which includes print-out of constructed
    # objects. This will really clutter your console, usable only for test
    # debugging.
    #
    verbose = False

    def setUp(self):
        os.mkdir(RRD_STATS_DIR)
        self.stats = mentat.stats.rrd.RrdStats(RRD_STATS_DIR, RRD_REPORTS_DIR)

    def tearDown(self):
        shutil.rmtree(RRD_STATS_DIR)

    def test_01_internals(self):
        """
        Perform the basic operativity tests of internal and helper methods.
        """
        self.assertEqual(self.stats.clean('abcDEF123-_'), 'abcDEF123-_')
        self.assertEqual(self.stats.clean('abcDEF123-_<,>./?;:"[]{}()=+*!@#$%^&*'), 'abcDEF123-___________________________')

        self.assertEqual(self.stats._color_for_ds('typea', 'testa'), 'FF0000')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typea', 'testb'), 'FFFF00')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typea', 'testc'), '0000FF')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typea', 'testa'), 'FF0000')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typea', 'testb'), 'FFFF00')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typea', 'testc'), '0000FF')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testa'), 'FF0000')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testb'), 'FFFF00')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testc'), '0000FF')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testa'), 'FF0000')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testb'), 'FFFF00')  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(self.stats._color_for_ds('typeb', 'testc'), '0000FF')  # pylint: disable=locally-disabled,protected-access

    def test_02_prepare_db(self):
        """
        Test creation of RRD database files.
        """
        self.maxDiff = None

        tst = TIME_START - mentat.stats.rrd.DFLT_STEP

        #
        # Create RRD databases for three different datasets of two different types.
        #
        self.assertEqual(self.stats.prepare_db('typea.{}'.format(mentat.stats.rrd.DB_TOTALS_NAME), tst), ('/var/tmp/utest_rrdstats/typea._totals.rrd', True))
        self.assertEqual(self.stats.prepare_db('typeb.{}'.format(mentat.stats.rrd.DB_TOTALS_NAME), tst), ('/var/tmp/utest_rrdstats/typeb._totals.rrd', True))

        self.assertEqual(self.stats.prepare_db('typea.testa', tst), ('/var/tmp/utest_rrdstats/typea.testa.rrd', True))
        self.assertEqual(self.stats.prepare_db('typea.testb', tst), ('/var/tmp/utest_rrdstats/typea.testb.rrd', True))
        self.assertEqual(self.stats.prepare_db('typea.testc', tst), ('/var/tmp/utest_rrdstats/typea.testc.rrd', True))

        self.assertEqual(self.stats.prepare_db('typeb.testa', tst), ('/var/tmp/utest_rrdstats/typeb.testa.rrd', True))
        self.assertEqual(self.stats.prepare_db('typeb.testb', tst), ('/var/tmp/utest_rrdstats/typeb.testb.rrd', True))
        self.assertEqual(self.stats.prepare_db('typeb.testc', tst), ('/var/tmp/utest_rrdstats/typeb.testc.rrd', True))

        #
        # Create same RRD databases again, but the files already exist, and will not be created.
        #
        self.assertEqual(self.stats.prepare_db('typea.{}'.format(mentat.stats.rrd.DB_TOTALS_NAME), tst), ('/var/tmp/utest_rrdstats/typea._totals.rrd', False))
        self.assertEqual(self.stats.prepare_db('typeb.{}'.format(mentat.stats.rrd.DB_TOTALS_NAME), tst), ('/var/tmp/utest_rrdstats/typeb._totals.rrd', False))

        self.assertEqual(self.stats.prepare_db('typea.testa', tst), ('/var/tmp/utest_rrdstats/typea.testa.rrd', False))
        self.assertEqual(self.stats.prepare_db('typea.testb', tst), ('/var/tmp/utest_rrdstats/typea.testb.rrd', False))
        self.assertEqual(self.stats.prepare_db('typea.testc', tst), ('/var/tmp/utest_rrdstats/typea.testc.rrd', False))

        self.assertEqual(self.stats.prepare_db('typeb.testa', tst), ('/var/tmp/utest_rrdstats/typeb.testa.rrd', False))
        self.assertEqual(self.stats.prepare_db('typeb.testb', tst), ('/var/tmp/utest_rrdstats/typeb.testb.rrd', False))
        self.assertEqual(self.stats.prepare_db('typeb.testc', tst), ('/var/tmp/utest_rrdstats/typeb.testc.rrd', False))

        #
        # Check the existence of database files.
        #
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typea.{}.rrd'.format(mentat.stats.rrd.DB_TOTALS_NAME))))
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typeb.{}.rrd'.format(mentat.stats.rrd.DB_TOTALS_NAME))))

        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typea.testa.rrd')))
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typea.testb.rrd')))
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typea.testc.rrd')))

        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typeb.testa.rrd')))
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typeb.testb.rrd')))
        self.assertTrue(os.path.isfile(os.path.join(RRD_STATS_DIR, 'typeb.testc.rrd')))

    def test_03_find_dbs(self):
        """
        Test the lookup of RRD database files.
        """
        self.maxDiff = None

        self.test_02_prepare_db()

        self.assertEqual(self.stats.find_dbs(), {
            'typea': [
                (
                    'typea._totals',
                    'typea',
                    '_totals',
                    '/var/tmp/utest_rrdstats/typea._totals.rrd',
                    True
                ),
                (
                    'typea.testa',
                    'typea',
                    'testa',
                    '/var/tmp/utest_rrdstats/typea.testa.rrd',
                    False
                ),
                (
                    'typea.testb',
                    'typea',
                    'testb',
                    '/var/tmp/utest_rrdstats/typea.testb.rrd',
                    False
                ),
                (
                    'typea.testc',
                    'typea',
                    'testc',
                    '/var/tmp/utest_rrdstats/typea.testc.rrd',
                    False
                )
            ],
            'typeb': [
                (
                    'typeb._totals',
                    'typeb',
                    '_totals',
                    '/var/tmp/utest_rrdstats/typeb._totals.rrd',
                    True
                ),
                (
                    'typeb.testa',
                    'typeb',
                    'testa',
                    '/var/tmp/utest_rrdstats/typeb.testa.rrd',
                    False
                ),
                (
                    'typeb.testb',
                    'typeb',
                    'testb',
                    '/var/tmp/utest_rrdstats/typeb.testb.rrd',
                    False
                ),
                (
                    'typeb.testc',
                    'typeb',
                    'testc',
                    '/var/tmp/utest_rrdstats/typeb.testc.rrd',
                    False
                )
            ]
        })

        self.assertEqual(self.stats.find_dbs('typea'), {
            'typea': [
                (
                    'typea._totals',
                    'typea',
                    '_totals',
                    '/var/tmp/utest_rrdstats/typea._totals.rrd',
                    True
                ),
                (
                    'typea.testa',
                    'typea',
                    'testa',
                    '/var/tmp/utest_rrdstats/typea.testa.rrd',
                    False
                ),
                (
                    'typea.testb',
                    'typea',
                    'testb',
                    '/var/tmp/utest_rrdstats/typea.testb.rrd',
                    False
                ),
                (
                    'typea.testc',
                    'typea',
                    'testc',
                    '/var/tmp/utest_rrdstats/typea.testc.rrd',
                    False
                )
            ]
        })

        self.assertEqual(self.stats.find_dbs('typeb'), {
            'typeb': [
                (
                    'typeb._totals',
                    'typeb',
                    '_totals',
                    '/var/tmp/utest_rrdstats/typeb._totals.rrd',
                    True
                ),
                (
                    'typeb.testa',
                    'typeb',
                    'testa',
                    '/var/tmp/utest_rrdstats/typeb.testa.rrd',
                    False
                ),
                (
                    'typeb.testb',
                    'typeb',
                    'testb',
                    '/var/tmp/utest_rrdstats/typeb.testb.rrd',
                    False
                ),
                (
                    'typeb.testc',
                    'typeb',
                    'testc',
                    '/var/tmp/utest_rrdstats/typeb.testc.rrd',
                    False
                )
            ]
        })

    def test_04_update(self):
        """
        Test update of RRD database files.
        """
        self.maxDiff = None

        self.test_02_prepare_db()

        rrd_dbs = self.stats.find_dbs()

        for idx in range(TEST_DATA_SIZE):

            tstamp = TIME_START + (idx * mentat.stats.rrd.DFLT_STEP)
            total  = 0

            for (rrddbt, rrddb_list) in rrd_dbs.items():
                for rrddb in rrddb_list:
                    value = random.randint(0, 1000)
                    total += value
                    if not rrddb[4]:
                        self.assertEqual(self.stats.update(rrddb[0], value, tst=tstamp), (rrddb[3], False))

                # Store summaries into '_totals' database.
                for rrddb in rrddb_list:
                    if rrddb[4]:
                        self.assertEqual(self.stats.update(rrddb[0], total, tst=tstamp), (rrddb[3], False))

    def test_05_update_all(self):
        """
        Test global update of all RRD database files.
        """
        self.maxDiff = None

        self.test_02_prepare_db()

        for idx in range(TEST_DATA_SIZE):

            tstamp = TIME_START + (idx * mentat.stats.rrd.DFLT_STEP)
            self.assertEqual(self.stats.update_all(random.randint(0, 1000), tst=tstamp), [
                ('/var/tmp/utest_rrdstats/typea._totals.rrd', False),
                ('/var/tmp/utest_rrdstats/typea.testa.rrd',   False),
                ('/var/tmp/utest_rrdstats/typea.testb.rrd',   False),
                ('/var/tmp/utest_rrdstats/typea.testc.rrd',   False),
                ('/var/tmp/utest_rrdstats/typeb._totals.rrd', False),
                ('/var/tmp/utest_rrdstats/typeb.testa.rrd',   False),
                ('/var/tmp/utest_rrdstats/typeb.testb.rrd',   False),
                ('/var/tmp/utest_rrdstats/typeb.testc.rrd',   False)
            ])

    def test_06_export(self):
        """
        Test exporting of RRD database files.
        """
        self.maxDiff = None

        self.test_04_update()

        rrd_dbs = self.stats.find_dbs()

        for (rrddbt, rrddb_list) in rrd_dbs.items():
            for rrddb in rrddb_list:
                (rrddbf, flag_new, result) = self.stats.export(rrddb[0])
                self.assertEqual(rrddbf, rrddb[3])
                self.assertFalse(flag_new)
                self.assertTrue(result)

    def test_07_lookup(self):
        """
        Test lookup of all RRD charts, spark charts and JSON export files.
        """
        self.test_04_update()

        result = self.stats.lookup()
        self.assertIsInstance(result, list)
        self.assertTrue(result)     # Not empty

    def test_08_generate(self):
        """
        Test generating all RRD charts, spark charts and JSON export files.
        """
        self.test_04_update()

        time_end = (TIME_START + (mentat.stats.rrd.DFLT_STEP * TEST_DATA_SIZE))
        result = self.stats.generate(time_end)

        for res in result:
            self.assertTrue(os.path.isfile(res))

        self.assertEqual(result, [
            '/var/tmp/typea.l6hours.meta.json',
            '/var/tmp/typea.l6hours.png',
            '/var/tmp/typea.l6hours.spark.png',
            '/var/tmp/typea.l6hours.xport.json',
            '/var/tmp/typea.l6hours-t.meta.json',
            '/var/tmp/typea.l6hours-t.png',
            '/var/tmp/typea.l6hours-t.spark.png',
            '/var/tmp/typea.l6hours-t.xport.json',
            '/var/tmp/typea.l24hours.meta.json',
            '/var/tmp/typea.l24hours.png',
            '/var/tmp/typea.l24hours.spark.png',
            '/var/tmp/typea.l24hours.xport.json',
            '/var/tmp/typea.l24hours-t.meta.json',
            '/var/tmp/typea.l24hours-t.png',
            '/var/tmp/typea.l24hours-t.spark.png',
            '/var/tmp/typea.l24hours-t.xport.json',
            '/var/tmp/typea.l72hours.meta.json',
            '/var/tmp/typea.l72hours.png',
            '/var/tmp/typea.l72hours.spark.png',
            '/var/tmp/typea.l72hours.xport.json',
            '/var/tmp/typea.l72hours-t.meta.json',
            '/var/tmp/typea.l72hours-t.png',
            '/var/tmp/typea.l72hours-t.spark.png',
            '/var/tmp/typea.l72hours-t.xport.json',
            '/var/tmp/typea.lweek.meta.json',
            '/var/tmp/typea.lweek.png',
            '/var/tmp/typea.lweek.spark.png',
            '/var/tmp/typea.lweek.xport.json',
            '/var/tmp/typea.lweek-t.meta.json',
            '/var/tmp/typea.lweek-t.png',
            '/var/tmp/typea.lweek-t.spark.png',
            '/var/tmp/typea.lweek-t.xport.json',
            '/var/tmp/typea.l2weeks.meta.json',
            '/var/tmp/typea.l2weeks.png',
            '/var/tmp/typea.l2weeks.spark.png',
            '/var/tmp/typea.l2weeks.xport.json',
            '/var/tmp/typea.l2weeks-t.meta.json',
            '/var/tmp/typea.l2weeks-t.png',
            '/var/tmp/typea.l2weeks-t.spark.png',
            '/var/tmp/typea.l2weeks-t.xport.json',
            '/var/tmp/typea.l4weeks.meta.json',
            '/var/tmp/typea.l4weeks.png',
            '/var/tmp/typea.l4weeks.spark.png',
            '/var/tmp/typea.l4weeks.xport.json',
            '/var/tmp/typea.l4weeks-t.meta.json',
            '/var/tmp/typea.l4weeks-t.png',
            '/var/tmp/typea.l4weeks-t.spark.png',
            '/var/tmp/typea.l4weeks-t.xport.json',
            '/var/tmp/typea.l3months.meta.json',
            '/var/tmp/typea.l3months.png',
            '/var/tmp/typea.l3months.spark.png',
            '/var/tmp/typea.l3months.xport.json',
            '/var/tmp/typea.l3months-t.meta.json',
            '/var/tmp/typea.l3months-t.png',
            '/var/tmp/typea.l3months-t.spark.png',
            '/var/tmp/typea.l3months-t.xport.json',
            '/var/tmp/typea.l6months.meta.json',
            '/var/tmp/typea.l6months.png',
            '/var/tmp/typea.l6months.spark.png',
            '/var/tmp/typea.l6months.xport.json',
            '/var/tmp/typea.l6months-t.meta.json',
            '/var/tmp/typea.l6months-t.png',
            '/var/tmp/typea.l6months-t.spark.png',
            '/var/tmp/typea.l6months-t.xport.json',
            '/var/tmp/typea.lyear.meta.json',
            '/var/tmp/typea.lyear.png',
            '/var/tmp/typea.lyear.spark.png',
            '/var/tmp/typea.lyear.xport.json',
            '/var/tmp/typea.lyear-t.meta.json',
            '/var/tmp/typea.lyear-t.png',
            '/var/tmp/typea.lyear-t.spark.png',
            '/var/tmp/typea.lyear-t.xport.json',
            '/var/tmp/typea.l2years.meta.json',
            '/var/tmp/typea.l2years.png',
            '/var/tmp/typea.l2years.spark.png',
            '/var/tmp/typea.l2years.xport.json',
            '/var/tmp/typea.l2years-t.meta.json',
            '/var/tmp/typea.l2years-t.png',
            '/var/tmp/typea.l2years-t.spark.png',
            '/var/tmp/typea.l2years-t.xport.json',
            '/var/tmp/typeb.l6hours.meta.json',
            '/var/tmp/typeb.l6hours.png',
            '/var/tmp/typeb.l6hours.spark.png',
            '/var/tmp/typeb.l6hours.xport.json',
            '/var/tmp/typeb.l6hours-t.meta.json',
            '/var/tmp/typeb.l6hours-t.png',
            '/var/tmp/typeb.l6hours-t.spark.png',
            '/var/tmp/typeb.l6hours-t.xport.json',
            '/var/tmp/typeb.l24hours.meta.json',
            '/var/tmp/typeb.l24hours.png',
            '/var/tmp/typeb.l24hours.spark.png',
            '/var/tmp/typeb.l24hours.xport.json',
            '/var/tmp/typeb.l24hours-t.meta.json',
            '/var/tmp/typeb.l24hours-t.png',
            '/var/tmp/typeb.l24hours-t.spark.png',
            '/var/tmp/typeb.l24hours-t.xport.json',
            '/var/tmp/typeb.l72hours.meta.json',
            '/var/tmp/typeb.l72hours.png',
            '/var/tmp/typeb.l72hours.spark.png',
            '/var/tmp/typeb.l72hours.xport.json',
            '/var/tmp/typeb.l72hours-t.meta.json',
            '/var/tmp/typeb.l72hours-t.png',
            '/var/tmp/typeb.l72hours-t.spark.png',
            '/var/tmp/typeb.l72hours-t.xport.json',
            '/var/tmp/typeb.lweek.meta.json',
            '/var/tmp/typeb.lweek.png',
            '/var/tmp/typeb.lweek.spark.png',
            '/var/tmp/typeb.lweek.xport.json',
            '/var/tmp/typeb.lweek-t.meta.json',
            '/var/tmp/typeb.lweek-t.png',
            '/var/tmp/typeb.lweek-t.spark.png',
            '/var/tmp/typeb.lweek-t.xport.json',
            '/var/tmp/typeb.l2weeks.meta.json',
            '/var/tmp/typeb.l2weeks.png',
            '/var/tmp/typeb.l2weeks.spark.png',
            '/var/tmp/typeb.l2weeks.xport.json',
            '/var/tmp/typeb.l2weeks-t.meta.json',
            '/var/tmp/typeb.l2weeks-t.png',
            '/var/tmp/typeb.l2weeks-t.spark.png',
            '/var/tmp/typeb.l2weeks-t.xport.json',
            '/var/tmp/typeb.l4weeks.meta.json',
            '/var/tmp/typeb.l4weeks.png',
            '/var/tmp/typeb.l4weeks.spark.png',
            '/var/tmp/typeb.l4weeks.xport.json',
            '/var/tmp/typeb.l4weeks-t.meta.json',
            '/var/tmp/typeb.l4weeks-t.png',
            '/var/tmp/typeb.l4weeks-t.spark.png',
            '/var/tmp/typeb.l4weeks-t.xport.json',
            '/var/tmp/typeb.l3months.meta.json',
            '/var/tmp/typeb.l3months.png',
            '/var/tmp/typeb.l3months.spark.png',
            '/var/tmp/typeb.l3months.xport.json',
            '/var/tmp/typeb.l3months-t.meta.json',
            '/var/tmp/typeb.l3months-t.png',
            '/var/tmp/typeb.l3months-t.spark.png',
            '/var/tmp/typeb.l3months-t.xport.json',
            '/var/tmp/typeb.l6months.meta.json',
            '/var/tmp/typeb.l6months.png',
            '/var/tmp/typeb.l6months.spark.png',
            '/var/tmp/typeb.l6months.xport.json',
            '/var/tmp/typeb.l6months-t.meta.json',
            '/var/tmp/typeb.l6months-t.png',
            '/var/tmp/typeb.l6months-t.spark.png',
            '/var/tmp/typeb.l6months-t.xport.json',
            '/var/tmp/typeb.lyear.meta.json',
            '/var/tmp/typeb.lyear.png',
            '/var/tmp/typeb.lyear.spark.png',
            '/var/tmp/typeb.lyear.xport.json',
            '/var/tmp/typeb.lyear-t.meta.json',
            '/var/tmp/typeb.lyear-t.png',
            '/var/tmp/typeb.lyear-t.spark.png',
            '/var/tmp/typeb.lyear-t.xport.json',
            '/var/tmp/typeb.l2years.meta.json',
            '/var/tmp/typeb.l2years.png',
            '/var/tmp/typeb.l2years.spark.png',
            '/var/tmp/typeb.l2years.xport.json',
            '/var/tmp/typeb.l2years-t.meta.json',
            '/var/tmp/typeb.l2years-t.png',
            '/var/tmp/typeb.l2years-t.spark.png',
            '/var/tmp/typeb.l2years-t.xport.json'
        ])


if __name__ == "__main__":
    unittest.main()

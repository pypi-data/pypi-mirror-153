#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
Unit test module for testing the :py:mod:`mentat.reports.utils` module.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import unittest
from unittest.mock import Mock
import datetime
import pprint

#
# Custom libraries
#
from pynspect.gparser import PynspectFilterParser
from pynspect.jpath import jpath_values

import mentat.const
import mentat.services.sqlstorage
import mentat.services.eventstorage
import mentat.idea.internal
import mentat.reports.utils
from mentat.datatype.sqldb import GroupModel, FilterModel, NetworkModel, \
    SettingsReportingModel

#-------------------------------------------------------------------------------
# NOTE: Sorry for the long lines in this file. They are deliberate, because the
# assertion permutations are (IMHO) more readable this way.
#-------------------------------------------------------------------------------

REPORTS_DIR = '/var/tmp'

class TestMentatReportsUtils(unittest.TestCase):
    """
    Unit test class for testing the :py:mod:`mentat.reports.utils` module.
    """

    #
    # Turn on more verbose output, which includes print-out of constructed
    # objects. This will really clutter your console, usable only for test
    # debugging.
    #
    verbose = True

    ideas_raw = [
        {
            'Format': 'IDEA0',
            'ID': 'msg01',
            'DetectTime': '2018-01-01T12:00:00Z',
            'Category': ['Fraud.Phishing'],
            'Description': 'Synthetic example 01',
            'Source': [
                {
                    'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25', '10.0.0.1'],
                    'IP6': ['2001:db8::ff00:42:0/112']
                }
            ],
            'Target': [
                {
                    'IP4': ['10.2.2.0/24'],
                    'IP6': ['2001:ffff::ff00:42:0/112']
                }
            ],
            'Node': [
                {
                    'Name': 'org.example.kippo_honey',
                    'SW': ['Kippo']
                }
            ],
            '_Mentat' : {
                'ResolvedAbuses' : [
                    'abuse@cesnet.cz'
                ],
                'EventClass' : 'class01',
                'EventSeverity': 'low'
            }
        },
        {
            'Format': 'IDEA0',
            'ID': 'msg02',
            'DetectTime': '2018-01-01T13:00:00Z',
            'Category': ['Recon.Scanning'],
            'Description': 'Synthetic example 02',
            'Source': [
                {
                    'IP4': ['192.168.1.2-192.168.1.5', '192.169.0.0/25', '10.0.0.1'],
                    'IP6': ['2002:db8::ff00:42:0/112']
                }
            ],
            'Target': [
                {
                    'IP4': ['11.2.2.0/24'],
                    'IP6': ['2004:ffff::ff00:42:0/112']
                }
            ],
            'Node': [
                {
                    'Name': 'org.example.dionaea',
                    'SW': ['Dionaea']
                }
            ],
            '_Mentat' : {
                'ResolvedAbuses' : [
                    'abuse@cesnet.cz'
                ],
                'EventClass' : 'class02',
                'EventSeverity': 'low'
            }
        }
    ]

    ideas_obj = list(map(mentat.idea.internal.Idea, ideas_raw))

    def setUp(self):
        """
        Perform test case setup.
        """
        self.sqlstorage = mentat.services.sqlstorage.StorageService(
            url  = 'postgresql://mentat:mentat@localhost/mentat_utest',
            echo = False
        )
        self.sqlstorage.database_drop()
        self.sqlstorage.database_create()

        self.eventstorage = mentat.services.eventstorage.EventStorageService(
            dbname   = 'mentat_utest',
            user     = 'mentat',
            password = 'mentat',
            host     = 'localhost',
            port     = 5432
        )
        self.eventstorage.database_drop()
        self.eventstorage.database_create()
        for event in self.ideas_obj:
            event['_Mentat']['StorageTime'] = datetime.datetime.utcnow()
            self.eventstorage.insert_event(event)

        group = GroupModel(name = 'abuse@cesnet.cz',  source = 'manual', description = 'CESNET, z.s.p.o.')

        FilterModel(group = group, name = 'FLT1', type = 'basic', filter = 'Node.Name == "org.example.kippo_honey"', description = 'DESC1', enabled = True)
        FilterModel(group = group, name = 'FLT2', type = 'basic', filter = 'Category == "Recon.Scanning"', description = 'DESC2', enabled = True)

        NetworkModel(group = group, netname = 'UNET1', source = 'manual', network = '10.0.0.0/8')

        SettingsReportingModel(group = group)

        self.sqlstorage.session.add(group)
        self.sqlstorage.session.commit()

        self.stcache = mentat.reports.utils.StorageThresholdingCache(
            Mock(),
            self.eventstorage
        )
        self.ntcache = mentat.reports.utils.NoThresholdingCache()

    def tearDown(self):
        self.sqlstorage.session.close()
        self.sqlstorage.database_drop()
        self.eventstorage.database_drop()

    def test_01_generate_cache_keys(self):
        """
        Test :py:func:`mentat.reports.utils.ThresholdingCache._generate_cache_keys` function.
        """
        self.maxDiff = None

        for ip in (jpath_values(self.ideas_raw[0], "Source.IP4") + jpath_values(self.ideas_raw[0], "Source.IP6")):
            key = self.stcache._generate_cache_key(self.ideas_raw[0], ip)
            self.assertEqual(self.stcache.get_source_from_cache_key(key), ip)
        self.assertEqual(
            self.stcache._generate_cache_key({  # pylint: disable=locally-disabled,protected-access
                'Category': ['Test', 'Value'],
                'Source': [{'IP4': ['195.113.144.194']}]
            }, '195.113.144.194'),
            'Test/Value+++195.113.144.194'
        )

    def test_02_no_thr_cache(self):
        """
        Test :py:func:`mentat.reports.utils.NoThresholdingCache` class.
        """
        self.maxDiff = None

        ttltime = datetime.datetime.utcnow()
        relapsetime = ttltime - datetime.timedelta(seconds = 600)
        thresholdtime = relapsetime - datetime.timedelta(seconds = 600)

        self.assertFalse(
            self.ntcache.event_is_thresholded(self.ideas_obj[0], '192.168.1.1', ttltime)
        )
        self.ntcache.set_threshold(self.ideas_obj[0], '192.168.1.1', thresholdtime, relapsetime, ttltime)
        self.assertFalse(
            self.ntcache.event_is_thresholded(self.ideas_obj[0], '192.168.1.1', ttltime)
        )
        self.ntcache.threshold_event(self.ideas_obj[0], '192.168.1.1', 'Test', 'low', datetime.datetime.utcnow())
        self.assertFalse(
            self.ntcache.event_is_thresholded(self.ideas_obj[0], '192.168.1.1', ttltime)
        )

    def test_03_storage_thr_cache(self):
        """
        Test :py:func:`mentat.reports.utils.StorageThresholdingCache` class.
        """
        self.maxDiff = None

        ttltime = datetime.datetime.utcnow()
        reltime = ttltime - datetime.timedelta(seconds = 300)
        thrtime = reltime - datetime.timedelta(seconds = 300)

        self.assertFalse(
            self.stcache.event_is_thresholded(self.ideas_obj[0], '192.168.0.2-192.168.0.5', ttltime)
        )
        self.stcache.set_threshold(self.ideas_obj[0], '192.168.0.2-192.168.0.5', thrtime, reltime, ttltime)
        self.assertTrue(
            self.stcache.event_is_thresholded(self.ideas_obj[0], '192.168.0.2-192.168.0.5', ttltime - datetime.timedelta(seconds = 50))
        )
        self.assertFalse(
            self.stcache.event_is_thresholded(self.ideas_obj[0], '192.168.0.0/25', ttltime - datetime.timedelta(seconds = 50))
        )
        self.stcache.set_threshold(self.ideas_obj[0], '192.168.0.0/25', thrtime, reltime, ttltime)
        self.assertTrue(
            self.stcache.event_is_thresholded(self.ideas_obj[0], '192.168.0.0/25', ttltime - datetime.timedelta(seconds = 50))
        )

        self.stcache.threshold_event(self.ideas_obj[0], '192.168.0.2-192.168.0.5', 'test@domain.org', 'low', ttltime - datetime.timedelta(seconds = 50))
        self.stcache.threshold_event(self.ideas_obj[0], '192.168.0.0/25', 'test@domain.org', 'low', ttltime - datetime.timedelta(seconds = 50))
        relapses = self.stcache.relapses('test@domain.org', 'low', ttltime + datetime.timedelta(seconds = 50))
        self.assertEqual(len(relapses), 1)
        self.assertEqual(relapses[0][0], 'msg01')
        self.assertEqual(len(relapses[0][2]), 2)

        self.assertEqual(self.stcache.eventservice.thresholds_count(), 2)
        self.assertEqual(self.stcache.eventservice.thresholded_events_count(), 2)

        self.assertEqual(
            self.stcache.cleanup(ttltime + datetime.timedelta(seconds = 50)),
            {'thresholds': 2, 'events': 2}
        )

    def test_04_reporting_settings(self):
        """
        Test :py:class:`mentat.reports.utils.ReportingSettings` class.
        """
        self.maxDiff = None

        abuse_group = self.sqlstorage.session.query(GroupModel).filter(GroupModel.name == 'abuse@cesnet.cz').one()
        self.sqlstorage.session.commit()

        reporting_settings = mentat.reports.utils.ReportingSettings(
            abuse_group
        )
        self.assertEqual(reporting_settings.group_name, 'abuse@cesnet.cz')
        self.assertEqual(str(reporting_settings.filters), "[<Filter(name='FLT1')>, <Filter(name='FLT2')>]")
        self.assertEqual(str(reporting_settings.networks), "[<Network(netname='UNET1',network='10.0.0.0/8')>]")
        self.assertEqual(reporting_settings.mode, 'summary')
        self.assertEqual(reporting_settings.emails, (['abuse@cesnet.cz'], [], [], []))
        self.assertEqual(reporting_settings.redirect, False)
        self.assertEqual(reporting_settings.template, 'default')
        self.assertEqual(reporting_settings.locale, 'en')
        self.assertEqual(reporting_settings.timezone, 'UTC')
        self.assertEqual(reporting_settings.timing, 'default')
        self.assertEqual(reporting_settings.timing_cfg, {
            'critical': {
                'per': datetime.timedelta(0, 600),
                'rel': datetime.timedelta(0),
                'thr': datetime.timedelta(0, 7200)
            },
            'high': {
                'per': datetime.timedelta(0, 600),
                'rel': datetime.timedelta(0, 43200),
                'thr': datetime.timedelta(1)
            },
            'low': {
                'per': datetime.timedelta(1),
                'rel': datetime.timedelta(2),
                'thr': datetime.timedelta(6)
            },
            'medium': {
                'per': datetime.timedelta(0, 7200),
                'rel': datetime.timedelta(2),
                'thr': datetime.timedelta(6)
            }
        })
        pprint.pprint(reporting_settings)

        reporting_settings = mentat.reports.utils.ReportingSettings(
            abuse_group,
            force_mode          = 'both',
            force_template      = 'another',
            force_locale        = 'cs',
            force_timezone      = 'America/Los_Angeles'
        )
        self.assertEqual(reporting_settings.mode, 'both')
        self.assertEqual(reporting_settings.template, 'another')
        self.assertEqual(reporting_settings.locale, 'cs')
        self.assertEqual(reporting_settings.timezone, 'America/Los_Angeles')
        pprint.pprint(reporting_settings)

        filter_parser   = PynspectFilterParser()
        filter_compiler = mentat.idea.internal.IDEAFilterCompiler()
        filter_parser.build()

        filter_list = reporting_settings.setup_filters(filter_parser, filter_compiler)
        self.assertEqual(str(filter_list), "[(<Filter(name='FLT1')>, COMPBINOP(VARIABLE('Node.Name') OP_EQ CONSTANT('org.example.kippo_honey'))), (<Filter(name='FLT2')>, COMPBINOP(VARIABLE('Category') OP_EQ CONSTANT('Recon.Scanning')))]")

        network_list = reporting_settings.setup_networks()
        self.assertEqual(list(map(lambda x: str(x['nrobj']), network_list)), ['10.0.0.0/8'])


#-------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

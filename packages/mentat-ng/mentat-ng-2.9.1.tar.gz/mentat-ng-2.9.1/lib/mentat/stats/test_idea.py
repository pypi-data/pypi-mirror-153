#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


import unittest
from pprint import pprint

import datetime

import mentat.stats.idea
import mentat.datatype.sqldb


class TestMentatStatsIdea(unittest.TestCase):

    #
    # Turn on more verbose output, which includes print-out of constructed
    # objects. This will really clutter your console, usable only for test
    # debugging.
    #
    verbose = False

    ideas_raw = [
        {
            "Format": "IDEA0",
            "ID": "msg01",
            "CreateTime": "2012-11-03T10:00:02Z",
            "DetectTime": "2012-11-03T10:00:07Z",
            "Category": ["Fraud.Phishing"],
            "Source": [
                {
                    "Type": ["Phishing"],
                    "IP4": ["192.168.0.2-192.168.0.5", "192.168.0.0/25"],
                    "IP6": ["2001:db8::ff00:42:0/112"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.kippo",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["Kippo"]
                }
            ],
            "_Mentat" : {
                "ResolvedAbuses" : [
                    "abuse@cesnet.cz"
                ]
            }
        },
        {
            "Format": "IDEA0",
            "ID": "msg02",
            "CreateTime": "2012-11-03T11:00:02Z",
            "DetectTime": "2012-11-03T11:00:07Z",
            "Category": ["Fraud.Phishing"],
            "Source": [
                {
                    "Type": ["Phishing"],
                    "IP4": ["192.168.0.2-192.168.0.5", "192.168.0.0/25"],
                    "IP6": ["2001:db8::ff00:42:0/112"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.kippo",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["Kippo"]
                }
            ],
            "_Mentat" : {
                "ResolvedAbuses" : [
                    "abuse@cesnet.cz"
                ]
            }
        },
        {
            "Format": "IDEA0",
            "ID": "msg03",
            "CreateTime": "2012-11-03T12:00:02Z",
            "DetectTime": "2012-11-03T12:00:07Z",
            "Category": ["Fraud.Phishing"],
            "Source": [
                {
                    "Type": ["Phishing"],
                    "IP4": ["192.168.0.2-192.168.0.5", "192.168.0.0/25"],
                    "IP6": ["2001:db8::ff00:42:0/112"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.dionaea",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["Kippo"]
                }
            ],
            "_Mentat" : {
                "ResolvedAbuses" : [
                    "abuse@cesnet.cz"
                ]
            }
        },
        {
            "Format": "IDEA0",
            "ID": "msg04",
            "CreateTime": "2012-11-03T15:00:02Z",
            "DetectTime": "2012-11-03T15:00:07Z",
            "Category": ["Spam"],
            "Source": [
                {
                    "Type": ["Spam"],
                    "IP4": ["192.168.0.100", "192.168.0.105"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.dionaea",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["Dionaea"]
                }
            ]
        },
        {
            "Format": "IDEA0",
            "ID": "msg05",
            "CreateTime": "2012-11-03T18:00:02Z",
            "DetectTime": "2012-11-03T18:00:07Z",
            "Category": ["Exploit"],
            "Source": [
                {
                    "Type": ["Exploit"],
                    "IP4": ["192.168.0.109", "192.168.0.200"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.labrea",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["LaBrea"]
                }
            ],
            "_Mentat" : {
                "ResolvedAbuses" : [
                    "abuse@cesnet.cz"
                ]
            }
        }
        ,
        {
            "Format": "IDEA0",
            "ID": "msg06",
            "CreateTime": "2012-11-03T18:00:02Z",
            "DetectTime": "2012-11-03T18:00:07Z",
            "Category": ["Exploit"],
            "Source": [
                {
                    "Type": ["Exploit"],
                    "IP4": ["192.172.0.109", "192.172.0.200"]
                }
            ],
            "Node": [
                {
                    "Name": "org.example.labrea",
                    "Tags": ["Protocol", "Honeypot"],
                    "SW": ["LaBrea"]
                },
                {
                    "SW" : [
                        "Beekeeper"
                    ],
                    "Name" : "cz.cesnet.holly"
                }
            ]
        }
    ]

    def test_01_counter_inc(self):
        """
        Test counter incrementation utility.
        """
        self.maxDiff = None

        test = {}

        self.assertEqual(mentat.stats.idea._counter_inc(test, 'x', 'a'),    {'x': {'a': 1}})  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(mentat.stats.idea._counter_inc(test, 'x', 'a'),    {'x': {'a': 2}})  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(mentat.stats.idea._counter_inc(test, 'x', 'a'),    {'x': {'a': 3}})  # pylint: disable=locally-disabled,protected-access
        self.assertEqual(mentat.stats.idea._counter_inc(test, 'x', 'a', 5), {'x': {'a': 8}})  # pylint: disable=locally-disabled,protected-access

    def test_02_make_toplist(self):
        """
        Test toplist creation utility.
        """
        self.maxDiff = None

        test1 = {
            'detectors': {
                'org.example.holly': 1,
                'org.example.rimmer': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.dionaea': 5,
                'org.example.kippo': 3,
                'org.example.labrea': 2
            }
        }

        self.assertEqual(mentat.stats.idea._make_toplist(test1, 'detectors', 5), {  # pylint: disable=locally-disabled,protected-access
            'detectors': {
                'org.example.holly': 1,
                'org.example.rimmer': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.dionaea': 5,
                'org.example.kippo': 3,
                'org.example.labrea': 2
            }
        })

        test2 = {
            'detectors': {
                '__REST__': 50,
                'org.example.rimmer': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.dionaea': 5,
                'org.example.kippo': 3,
                'org.example.labrea': 2
            }
        }

        self.assertEqual(mentat.stats.idea._make_toplist(test2, 'detectors', 5, True), {  # pylint: disable=locally-disabled,protected-access
            'detectors': {
                '__REST__': 55,
                'org.example.dionaea': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.rimmer': 5
            }
        })

        test3 = {
            'detectors': {
                '__REST__': 50,
                'org.example.rimmer': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
            }
        }

        self.assertEqual(mentat.stats.idea._make_toplist(test3, 'detectors', 5), {  # pylint: disable=locally-disabled,protected-access
            'detectors': {
                '__REST__': 50,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.rimmer': 5
            }
        })

        test4 = {
            'ip4s': {
                'org.example.holly': 1,
                'org.example.rimmer': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.dionaea': 5,
                'org.example.kippo': 3,
                'org.example.labrea': 2
            }
        }

        self.assertEqual(mentat.stats.idea._make_toplist(test4, 'ip4s', 5), {  # pylint: disable=locally-disabled,protected-access
            'ip4s': {
                '__REST__': 6,
                'org.example.dionaea': 5,
                'org.example.kryten': 10,
                'org.example.queeg': 20,
                'org.example.rimmer': 5
            }
        })

    def test_03_timeline_boundaries(self):
        """
        Test timeline boundary calculations.
        """
        self.maxDiff = None

        self.assertEqual(
            mentat.stats.idea._calculate_timeline_boundaries(  # pylint: disable=locally-disabled,protected-access
                datetime.datetime(2018, 1, 1, 1, 11, 1),
                datetime.datetime(2018, 1, 1, 1, 31, 31)
            ),
            (
                datetime.datetime(2018, 1, 1, 1, 10, 0),
                datetime.datetime(2018, 1, 1, 1, 35, 0),
                datetime.timedelta(seconds=300)
            )
        )
        self.assertEqual(
            mentat.stats.idea._calculate_timeline_boundaries(  # pylint: disable=locally-disabled,protected-access
                datetime.datetime(2018, 1, 1, 1, 1, 1),
                datetime.datetime(2018, 1, 1, 1, 59, 31)
            ),
            (
                datetime.datetime(2018, 1, 1, 1, 0, 0),
                datetime.datetime(2018, 1, 1, 2, 0, 0),
                datetime.timedelta(seconds=300)
            )
        )
        self.assertEqual(
            mentat.stats.idea._calculate_timeline_boundaries(  # pylint: disable=locally-disabled,protected-access
                datetime.datetime(2018, 1, 1, 1, 11, 1),
                datetime.datetime(2018, 1, 1, 23, 59, 31)
            ),
            (
                datetime.datetime(2018, 1, 1, 1, 0, 0),
                datetime.datetime(2018, 1, 2, 0, 0, 0),
                datetime.timedelta(seconds=3600)
            )
        )
        self.assertEqual(
            mentat.stats.idea._calculate_timeline_boundaries(  # pylint: disable=locally-disabled,protected-access
                datetime.datetime(2018, 1, 1, 1, 11, 1),
                datetime.datetime(2018, 1, 11, 23, 59, 31)
            ),
            (
                datetime.datetime(2018, 1, 1, 0, 0, 0),
                datetime.datetime(2018, 1, 12, 0, 0, 0),
                datetime.timedelta(seconds=86400)
            )
        )

    def test_04_timeline_steps(self):
        """
        Test timeline step calculations.
        """
        self.maxDiff = None

        self.assertEqual(
            mentat.stats.idea._calculate_timeline_steps(  # pylint: disable=locally-disabled,protected-access
                datetime.datetime(2018, 1, 1, 1, 11, 1),
                datetime.datetime(2018, 1, 11, 23, 59, 31),
                100
            ),
            (
                datetime.timedelta(seconds=10800),
                88
            )
        )

    def test_05_calc_timeline_cfg(self):
        """
        Test timeline config calculations.
        """

    def test_06_evaluate_events(self):
        """
        Perform the message evaluation tests.
        """
        self.maxDiff = None

        self.assertEqual(mentat.stats.idea.evaluate_events(self.ideas_raw), {
            'abuses': {'__unknown__': 2, 'abuse@cesnet.cz': 4},
            'analyzers': {'Beekeeper': 1, 'Dionaea': 1, 'Kippo': 3, 'LaBrea': 1},
            'asns': {'__unknown__': 6},
            'categories': {'Exploit': 2, 'Fraud.Phishing': 3, 'Spam': 1},
            'category_sets': {'Exploit': 2, 'Fraud.Phishing': 3, 'Spam': 1},
            'classes': {'__unknown__': 6},
            'cnt_alerts': 6,
            'cnt_events': 6,
            'cnt_recurring': 0,
            'cnt_unique': 6,
            'countries': {'__unknown__': 6},
            'detectors': {
                'cz.cesnet.holly': 1,
                'org.example.dionaea': 2,
                'org.example.kippo': 2,
                'org.example.labrea': 1
            },
            'detectorsws': {
                'cz.cesnet.holly/Beekeeper': 1,
                'org.example.dionaea/Dionaea': 1,
                'org.example.dionaea/Kippo': 1,
                'org.example.kippo/Kippo': 2,
                'org.example.labrea/LaBrea': 1
            },
            'ips': {
                '192.168.0.0/25': 3,
                '192.168.0.100': 1,
                '192.168.0.105': 1,
                '192.168.0.109': 1,
                '192.168.0.2-192.168.0.5': 3,
                '192.168.0.200': 1,
                '192.172.0.109': 1,
                '192.172.0.200': 1,
                '2001:db8::ff00:42:0/112': 3
            },
            'list_ids': ['msg01', 'msg02', 'msg03', 'msg04', 'msg05', 'msg06'],
            'severities': {'__unknown__': 6}
        })

    def test_07_truncate_stats(self):
        """
        Perform the basic operativity tests.
        """
        self.maxDiff = None

        self.assertEqual(
            mentat.stats.idea.truncate_stats(mentat.stats.idea.evaluate_events(self.ideas_raw), 3, True),
            {
                'abuses': {'__unknown__': 2, 'abuse@cesnet.cz': 4},
                'analyzers': {'Beekeeper': 1, 'Kippo': 3, '__REST__': 2},
                'asns': {'__unknown__': 6},
                'categories': {'Exploit': 2, 'Fraud.Phishing': 3, '__REST__': 1},
                'category_sets': {'Exploit': 2, 'Fraud.Phishing': 3, '__REST__': 1},
                'classes': {'__unknown__': 6},
                'cnt_alerts': 6,
                'cnt_events': 6,
                'cnt_recurring': 0,
                'cnt_unique': 6,
                'countries': {'__unknown__': 6},
                'detectors': {'__REST__': 2, 'org.example.dionaea': 2, 'org.example.kippo': 2},
                'detectorsws': {'__REST__': 3,
                                'cz.cesnet.holly/Beekeeper': 1,
                                'org.example.kippo/Kippo': 2},
                'ips': {'192.168.0.0/25': 3, '192.168.0.2-192.168.0.5': 3, '__REST__': 9},
                'severities': {'__unknown__': 6}
            }
        )

        self.assertEqual(
            mentat.stats.idea.truncate_stats(mentat.stats.idea.evaluate_events(self.ideas_raw), 2),
            {
                'abuses': {'__unknown__': 2, 'abuse@cesnet.cz': 4},
                'analyzers': {'Beekeeper': 1, 'Dionaea': 1, 'Kippo': 3, 'LaBrea': 1},
                'asns': {'__unknown__': 6},
                'categories': {'Exploit': 2, 'Fraud.Phishing': 3, 'Spam': 1},
                'category_sets': {'Exploit': 2, 'Fraud.Phishing': 3, 'Spam': 1},
                'classes': {'__unknown__': 6},
                'cnt_alerts': 6,
                'cnt_events': 6,
                'cnt_recurring': 0,
                'cnt_unique': 6,
                'countries': {'__unknown__': 6},
                'detectors': {'cz.cesnet.holly': 1,
                              'org.example.dionaea': 2,
                              'org.example.kippo': 2,
                              'org.example.labrea': 1},
                'detectorsws': {'cz.cesnet.holly/Beekeeper': 1,
                                'org.example.dionaea/Dionaea': 1,
                                'org.example.dionaea/Kippo': 1,
                                'org.example.kippo/Kippo': 2,
                                'org.example.labrea/LaBrea': 1},
                'ips': {'192.168.0.0/25': 3, '__REST__': 12},
                'severities': {'__unknown__': 6}
            }
        )

    def test_08_group_events(self):
        """
        Perform the basic operativity tests.
        """
        self.maxDiff = None

        self.assertEqual(
            mentat.stats.idea.group_events(self.ideas_raw),
            {
                'stats_external': [
                    {
                        'Category': ['Spam'],
                        'CreateTime': '2012-11-03T15:00:02Z',
                        'DetectTime': '2012-11-03T15:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg04',
                        'Node': [{'Name': 'org.example.dionaea',
                                  'SW': ['Dionaea'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.100', '192.168.0.105'],
                                    'Type': ['Spam']}]
                    },
                    {
                        'Category': ['Exploit'],
                        'CreateTime': '2012-11-03T18:00:02Z',
                        'DetectTime': '2012-11-03T18:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg06',
                        'Node': [{'Name': 'org.example.labrea',
                                  'SW': ['LaBrea'],
                                  'Tags': ['Protocol', 'Honeypot']},
                                 {'Name': 'cz.cesnet.holly', 'SW': ['Beekeeper']}],
                        'Source': [{'IP4': ['192.172.0.109', '192.172.0.200'],
                                    'Type': ['Exploit']}]
                    }
                ],
                'stats_internal': [
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T10:00:02Z',
                        'DetectTime': '2012-11-03T10:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg01',
                        'Node': [{'Name': 'org.example.kippo',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T11:00:02Z',
                        'DetectTime': '2012-11-03T11:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg02',
                        'Node': [{'Name': 'org.example.kippo',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T12:00:02Z',
                        'DetectTime': '2012-11-03T12:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg03',
                        'Node': [{'Name': 'org.example.dionaea',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Exploit'],
                        'CreateTime': '2012-11-03T18:00:02Z',
                        'DetectTime': '2012-11-03T18:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg05',
                        'Node': [{'Name': 'org.example.labrea',
                                  'SW': ['LaBrea'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.109', '192.168.0.200'],
                                    'Type': ['Exploit']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    }
                ],
                'stats_overall': [
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T10:00:02Z',
                        'DetectTime': '2012-11-03T10:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg01',
                        'Node': [{'Name': 'org.example.kippo',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T11:00:02Z',
                        'DetectTime': '2012-11-03T11:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg02',
                        'Node': [{'Name': 'org.example.kippo',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Fraud.Phishing'],
                        'CreateTime': '2012-11-03T12:00:02Z',
                        'DetectTime': '2012-11-03T12:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg03',
                        'Node': [{'Name': 'org.example.dionaea',
                                  'SW': ['Kippo'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25'],
                                    'IP6': ['2001:db8::ff00:42:0/112'],
                                    'Type': ['Phishing']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Spam'],
                        'CreateTime': '2012-11-03T15:00:02Z',
                        'DetectTime': '2012-11-03T15:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg04',
                        'Node': [{'Name': 'org.example.dionaea',
                                  'SW': ['Dionaea'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.100', '192.168.0.105'],
                                    'Type': ['Spam']}]
                    },
                    {
                        'Category': ['Exploit'],
                        'CreateTime': '2012-11-03T18:00:02Z',
                        'DetectTime': '2012-11-03T18:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg05',
                        'Node': [{'Name': 'org.example.labrea',
                                  'SW': ['LaBrea'],
                                  'Tags': ['Protocol', 'Honeypot']}],
                        'Source': [{'IP4': ['192.168.0.109', '192.168.0.200'],
                                    'Type': ['Exploit']}],
                        '_Mentat': {'ResolvedAbuses': ['abuse@cesnet.cz']}
                    },
                    {
                        'Category': ['Exploit'],
                        'CreateTime': '2012-11-03T18:00:02Z',
                        'DetectTime': '2012-11-03T18:00:07Z',
                        'Format': 'IDEA0',
                        'ID': 'msg06',
                        'Node': [{'Name': 'org.example.labrea',
                                  'SW': ['LaBrea'],
                                  'Tags': ['Protocol', 'Honeypot']},
                                 {'Name': 'cz.cesnet.holly', 'SW': ['Beekeeper']}],
                        'Source': [{'IP4': ['192.172.0.109', '192.172.0.200'],
                                    'Type': ['Exploit']}]
                    }
                ]
            }
        )

    def test_09_evaluate_event_groups(self):
        """
        Perform the basic operativity tests.
        """
        result = mentat.stats.idea.evaluate_event_groups(self.ideas_raw)
        if self.verbose:
            print('*** result = mentat.stats.idea.evaluate_event_groups(self.ideas_raw) ***')
            pprint(result)
        self.assertTrue(result)

        result = mentat.stats.idea.truncate_evaluations(result, 3)
        if self.verbose:
            print('*** result = mentat.stats.idea.truncate_evaluations(result, 3) ***')
            pprint(result)
        self.assertTrue(result)

    def test_10_merge_stats(self):
        """
        Perform the statistics aggregation tests.
        """
        self.maxDiff = None

        sts1 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        sts2 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        sts3 = mentat.stats.idea.evaluate_events(self.ideas_raw)

        result = mentat.stats.idea._merge_stats(sts1)  # pylint: disable=locally-disabled,protected-access
        result = mentat.stats.idea._merge_stats(sts2, result)  # pylint: disable=locally-disabled,protected-access
        result = mentat.stats.idea._merge_stats(sts3, result)  # pylint: disable=locally-disabled,protected-access

        self.assertEqual(
            result,
            {
                'abuses': {'__unknown__': 6, 'abuse@cesnet.cz': 12},
                'analyzers': {'Beekeeper': 3, 'Dionaea': 3, 'Kippo': 9, 'LaBrea': 3},
                'asns': {'__unknown__': 18},
                'categories': {'Exploit': 6, 'Fraud.Phishing': 9, 'Spam': 3},
                'category_sets': {'Exploit': 6, 'Fraud.Phishing': 9, 'Spam': 3},
                'classes': {'__unknown__': 18},
                'cnt_alerts': 18,
                'cnt_events': 18,
                'countries': {'__unknown__': 18},
                'detectors': {'cz.cesnet.holly': 3,
                              'org.example.dionaea': 6,
                              'org.example.kippo': 6,
                              'org.example.labrea': 3},
                'detectorsws': {'cz.cesnet.holly/Beekeeper': 3,
                                'org.example.dionaea/Dionaea': 3,
                                'org.example.dionaea/Kippo': 3,
                                'org.example.kippo/Kippo': 6,
                                'org.example.labrea/LaBrea': 3},
                'ips': {'192.168.0.0/25': 9,
                        '192.168.0.100': 3,
                        '192.168.0.105': 3,
                        '192.168.0.109': 3,
                        '192.168.0.2-192.168.0.5': 9,
                        '192.168.0.200': 3,
                        '192.172.0.109': 3,
                        '192.172.0.200': 3,
                        '2001:db8::ff00:42:0/112': 9},
                'severities': {'__unknown__': 18}
            }
        )

    def test_11_aggregate_stat_groups(self):
        """
        Perform the statistic group aggregation tests.
        """
        self.maxDiff = None

        timestamp = 1485993600

        stse1 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stse2 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stse3 = mentat.stats.idea.evaluate_events(self.ideas_raw)

        stso1 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stso2 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stso3 = mentat.stats.idea.evaluate_events(self.ideas_raw)

        stsi1 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stsi2 = mentat.stats.idea.evaluate_events(self.ideas_raw)
        stsi3 = mentat.stats.idea.evaluate_events(self.ideas_raw)

        sts1 = mentat.datatype.sqldb.EventStatisticsModel(
            interval       = 'interval1',
            dt_from        = datetime.datetime.fromtimestamp(timestamp),
            dt_to          = datetime.datetime.fromtimestamp(timestamp+300),
            count          = stso1[mentat.stats.idea.ST_SKEY_CNT_ALERTS],
            stats_overall  = stso1,
            stats_internal = stsi1,
            stats_external = stse1
        )
        sts2 = mentat.datatype.sqldb.EventStatisticsModel(
            interval       = 'interval2',
            dt_from        = datetime.datetime.fromtimestamp(timestamp+300),
            dt_to          = datetime.datetime.fromtimestamp(timestamp+600),
            count          = stso2[mentat.stats.idea.ST_SKEY_CNT_ALERTS],
            stats_overall  = stso2,
            stats_internal = stsi2,
            stats_external = stse2
        )
        sts3 = mentat.datatype.sqldb.EventStatisticsModel(
            interval       = 'interval3',
            dt_from        = datetime.datetime.fromtimestamp(timestamp+600),
            dt_to          = datetime.datetime.fromtimestamp(timestamp+900),
            count          = stso3[mentat.stats.idea.ST_SKEY_CNT_ALERTS],
            stats_overall  = stso3,
            stats_internal = stsi3,
            stats_external = stse3
        )

        result = mentat.stats.idea.aggregate_stat_groups([sts1, sts2, sts3])

        self.assertTrue(result)
        self.assertEqual(result['dt_from'], datetime.datetime.fromtimestamp(timestamp))
        self.assertEqual(result['dt_to'], datetime.datetime.fromtimestamp(timestamp+900))


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

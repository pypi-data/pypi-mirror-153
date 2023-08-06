#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
Unit test module for testing the :py:mod:`mentat.idea.internal` module.
"""

import json
import unittest
import difflib

import ipranges
import idea.lite
import pynspect.gparser
import mentat.idea.internal

#-------------------------------------------------------------------------------
# NOTE: Sorry for the long lines in this file. They are deliberate, because the
# assertion permutations are (IMHO) more readable this way.
#-------------------------------------------------------------------------------

class TestMentatIdeaInternal(unittest.TestCase):
    """
    Unit test class for testing the :py:mod:`mentat.idea.internal` module.
    """

    #
    # Turn on more verbose output, which includes print-out of constructed
    # objects. This will really clutter your console, usable only for test
    # debugging.
    #
    verbose = False

    idea_raw_1 = {
        'Format': 'IDEA0',
        'ID': '4390fc3f-c753-4a3e-bc83-1b44f24baf75',
        'CreateTime': '2012-11-03T10:00:02Z',
        'DetectTime': '2012-11-03T10:00:07Z',
        'WinStartTime': '2012-11-03T05:00:00Z',
        'WinEndTime': '2012-11-03T10:00:00Z',
        'EventTime': '2012-11-03T07:36:00Z',
        'CeaseTime': '2012-11-03T09:55:22Z',
        'Category': ['Fraud.Phishing', 'Test'],
        'Ref': ['cve:CVE-1234-5678'],
        'Confidence': 1.0,
        'Description': 'Synthetic example',
        'ConnCount': 20,
        'Source': [
            {
                'Type': ['Phishing'],
                'IP4': ['192.168.0.2-192.168.0.5', '192.168.0.0/25', '192.168.1.1', '192.168.1.2', '192.168.1.4'],
                'IP6': ['2001:db8::ff00:42:0/112','2001:db8::ff00:42:50'],
                'Hostname': ['example.com'],
                'URL': ['http://example.com/cgi-bin/killemall'],
                'Proto': ['tcp', 'http'],
                'AttachHand': ['att1'],
                'Netname': ['ripe:IANA-CBLK-RESERVED1']
            }
        ],
        'Target': [
            {
                'Type': ['Backscatter', 'OriginSpam'],
                'Email': ['innocent@example.com'],
                'IP6': ['2001:ffff::ff00:42:0/112'],
                'Port': [22, 25, 443],
                'Proto': ['tcp', 'http'],
                'Spoofed': True
            },
            {
                'Type': ['CasualIP'],
                'IP4': ['10.2.2.0/24'],
                'Port': [22, 25, 443],
                'Proto': ['tcp', 'http'],
                'Anonymised': True
            }
        ],
        'Attach': [
            {
                'Handle': 'att1',
                'FileName': ['killemall'],
                'Type': ['Malware'],
                'ContentType': 'application/octet-stream',
                'Hash': ['sha1:0c4a38c3569f0cc632e74f4c'],
                'Size': 46,
                'Ref': ['Trojan-Spy:W32/FinSpy.A'],
                'ContentEncoding': 'base64',
                'Content': 'TVpqdXN0a2lkZGluZwo='
            }
        ],
        'Node': [
            {
                'Name': 'org.example.kippo_honey',
                'Realm': 'cesnet.cz',
                'Type': ['Protocol', 'Honeypot'],
                'SW': ['Kippo'],
                'AggrWin': '00:05:00'
            }
        ],
        '_Mentat' : {
            'StorageTime': '2017-04-05T10:21:39Z',
            'EventTemplate': 'sserv-012',
            'ResolvedAbuses': ['abuse@cesnet.cz'],
            'Impact': 'System provides SDDP service and can be misused for massive DDoS attack',
            'EventClass': 'vulnerable-config-ssdp'
        }
    }

    idea_raw_2 = {
        'ID': '4dd7cf5e-4a95-49f6-8f04-947de998012c',
        'Format': 'IDEA0',
        'DetectTime': '2016-06-21T13:08:27Z',
        'WinStartTime': '2016-06-21T11:55:02Z',
        'WinEndTime': '2016-06-21T12:00:02Z',
        'ConnCount': 2,
        'Category': ['Attempt.Login'],
        'Description': 'SSH login attempt',
        'Source': [
            {
                'IP4': ['188.14.166.39']
            }
        ],
        'Target': [
            {
                'Proto': ['tcp', 'ssh'],
                'IP4': ['195.113.165.128/25'],
                'Port': [22],
                'Anonymised': True
            }
        ],
        'Node': [
            {
                'Type': ['Relay'],
                'Name': 'cz.cesnet.mentat.warden_filer'
            },
            {
                'SW': ['Kippo'],
                'AggrWin': '00:05:00',
                'Name': 'cz.uhk.apate.cowrie',
                'Type': ['Connection','Honeypot','Recon']
            }
        ],
        '_Mentat': {
            'StorageTime': '2016-06-21T14:00:07Z'
        }
    }

    def test_01_idea_raw(self):
        """
        Perform basic parsing and conversion tests from raw JSON.
        """
        self.maxDiff = None

        idea_internal_1 = mentat.idea.internal.Idea(self.idea_raw_1)
        if self.verbose:
            print("IDEA raw 1 as 'mentat.idea.internal.Idea' object:")
            print(json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default))
        self.assertEqual(json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default), idea_internal_1.to_json(indent=4))
        orig = json.dumps(self.idea_raw_1, indent=4, sort_keys=True)
        new  = json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default)
        self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))

        idea_internal_2 = mentat.idea.internal.Idea(self.idea_raw_2)
        if self.verbose:
            print("IDEA raw 2 as 'mentat.idea.internal.Idea' object:")
            print(json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default))
        self.assertEqual(json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default), idea_internal_2.to_json(indent=4))
        orig = json.dumps(self.idea_raw_2, indent=4, sort_keys=True)
        new  = json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default)
        self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))


    def test_02_idea_lite(self):
        """
        Perform basic parsing and conversion tests from ``idea.lite.Idea``. For
        the purposes of comparison, the ``idea.lite.Idea`` class is also tested here.
        """
        self.maxDiff = None

        idea_lite_1 = idea.lite.Idea(self.idea_raw_1)
        if self.verbose:
            print("IDEA raw 1 as 'idea.lite.Idea' object:")
            print(json.dumps(idea_lite_1, indent=4, sort_keys=True, default=idea_lite_1.json_default))
        orig = json.dumps(self.idea_raw_1, indent=4, sort_keys=True)
        new  = json.dumps(idea_lite_1, indent=4, sort_keys=True, default=idea_lite_1.json_default)
        self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))

        # TODO: Following code ends with failure, fix it.
        #idea_internal_1 = mentat.idea.internal.Idea(idea_lite_1)
        #if self.verbose:
        #    print("IDEA object 'idea.lite.Idea' as 'mentat.idea.internal.Idea' object:")
        #    print(json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default))
        #orig = json.dumps(self.idea_raw_1, indent=4, sort_keys=True)
        #new  = json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default)
        #self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))


        idea_lite_2 = idea.lite.Idea(self.idea_raw_2)
        if self.verbose:
            print("IDEA raw 2 as 'idea.lite.Idea' object:")
            print(json.dumps(idea_lite_2, indent=4, sort_keys=True, default=idea_lite_2.json_default))
        orig = json.dumps(self.idea_raw_2, indent=4, sort_keys=True)
        new  = json.dumps(idea_lite_2, indent=4, sort_keys=True, default=idea_lite_2.json_default)
        self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))

        # TODO: Following code ends with failure, fix it.
        #idea_internal_2 = mentat.idea.internal.Idea(idea_lite_2)
        #if self.verbose:
        #    print("IDEA object 'idea.lite.Idea' as 'mentat.idea.internal.Idea' object:")
        #    print(json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default))
        #orig = json.dumps(self.idea_raw_2, indent=4, sort_keys=True)
        #new  = json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default)
        #self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))


    def test_03_accessors(self):
        """
        Perform tests of message convenience accessors.
        """
        self.maxDiff = None

        idea_internal_1 = mentat.idea.internal.Idea(self.idea_raw_1)
        if self.verbose:
            print("IDEA raw 1 as 'mentat.idea.internal.Idea' object:")
            print(json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default))

        self.assertEqual(idea_internal_1.get_id(), '4390fc3f-c753-4a3e-bc83-1b44f24baf75')
        self.assertEqual(idea_internal_1.get_detect_time().isoformat(), '2012-11-03T10:00:07')
        self.assertEqual(idea_internal_1.get_storage_time().isoformat(), '2017-04-05T10:21:39')
        self.assertEqual(idea_internal_1.get_abuses(), ['abuse@cesnet.cz'])
        self.assertEqual(idea_internal_1.get_categories(), ['Fraud.Phishing', 'Test'])
        self.assertEqual(idea_internal_1.get_description(), 'Synthetic example')
        self.assertEqual(idea_internal_1.get_detectors(), ['org.example.kippo_honey'])
        self.assertEqual(idea_internal_1.get_addresses('Source'), [
            ipranges.IP4('192.168.1.4'),
            ipranges.IP4Range('192.168.1.1-192.168.1.2'),
            ipranges.IP4Range('192.168.0.0-192.168.0.127'),
            ipranges.IP6Range('2001:db8::ff00:42:0-2001:db8::ff00:42:ffff')
        ])
        self.assertEqual(idea_internal_1.get_addresses('Target'), [
            ipranges.IP4Range('10.2.2.0-10.2.2.255'),
            ipranges.IP6Range('2001:ffff::ff00:42:0-2001:ffff::ff00:42:ffff')
        ])
        self.assertEqual(idea_internal_1.get_ports('Source'), [])
        self.assertEqual(idea_internal_1.get_ports('Target'), [22, 25, 443])
        self.assertEqual(idea_internal_1.get_protocols('Source'), ['http', 'tcp'])
        self.assertEqual(idea_internal_1.get_protocols('Target'), ['http', 'tcp'])
        self.assertEqual(idea_internal_1.get_types('Source'), ['Phishing'])
        self.assertEqual(idea_internal_1.get_types('Target'), ['Backscatter', 'CasualIP', 'OriginSpam'])
        self.assertEqual(idea_internal_1.get_types('Node'), ['Honeypot', 'Protocol'])

    def test_04_to_and_from_string(self):
        """
        Perform tests of message conversions to and from JSON string representation.
        """
        self.maxDiff = None

        idea_internal_1 = mentat.idea.internal.Idea(self.idea_raw_1)
        if self.verbose:
            print("IDEA raw 1 as 'mentat.idea.internal.Idea' object:")
            print(json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default))
        idea_internal_2 = mentat.idea.internal.Idea.from_json(
            idea_internal_1.to_json()
        )
        orig = json.dumps(idea_internal_1, indent=4, sort_keys=True, default=idea_internal_1.json_default)
        new  = json.dumps(idea_internal_2, indent=4, sort_keys=True, default=idea_internal_2.json_default)
        self.assertEqual(orig, new, "\n".join([l for l in difflib.context_diff(orig.split("\n"), new.split("\n"))]))

    def test_05_get_ranges(self):
        """
        Perform tests of get_ranges function.
        """
        self.maxDiff = None

        self.assertEqual(mentat.idea.internal.Idea.get_ranges([], ipranges.IP4Range, ipranges.IP4), [])
        self.assertEqual(mentat.idea.internal.Idea.get_ranges([], ipranges.IP6Range, ipranges.IP4), [])
        self.assertEqual(mentat.idea.internal.Idea.get_ranges([
            ipranges.IP4('192.168.0.2'),
            ipranges.IP4('192.168.0.3'),
            ipranges.IP4('192.168.0.4'),
            ipranges.IP4('192.168.0.5')],
            ipranges.IP4Range, ipranges.IP4),
            [ipranges.IP4Range((ipranges.IP4('192.168.0.2'), ipranges.IP4('192.168.0.5')))])
        self.assertEqual(mentat.idea.internal.Idea.get_ranges([
            ipranges.IP4('192.168.0.3'),
            ipranges.IP4('192.168.0.5'),
            ipranges.IP4('192.168.1.19'),
            ipranges.IP4('192.168.1.20')],
            ipranges.IP4Range, ipranges.IP4),[
            ipranges.IP4Range((ipranges.IP4('192.168.1.19'), ipranges.IP4('192.168.1.20'))),
            ipranges.IP4('192.168.0.5'),
            ipranges.IP4('192.168.0.3')])
        self.assertEqual(mentat.idea.internal.Idea.get_ranges([
            ipranges.IP4('192.168.0.2'),
            ipranges.IP4('192.168.0.5'),
            ipranges.IP4('192.168.0.7')],
            ipranges.IP4Range, ipranges.IP4), [
            ipranges.IP4('192.168.0.7'),
            ipranges.IP4('192.168.0.5'),
            ipranges.IP4('192.168.0.2')])

        self.assertEqual(mentat.idea.internal.Idea.get_ranges([
            ipranges.IP6('2001:db8::ff00:42:50'),
            ipranges.IP6('2001:0db8::ff00:42:51'),
            ipranges.IP6('2001:db8::ff00:42:0052'),
            ipranges.IP6('2001:0db8::ff00:0042:0053')],
            ipranges.IP6Range, ipranges.IP6),
            [ipranges.IP6Range((ipranges.IP6('2001:db8::ff00:42:50'), ipranges.IP6('2001:db8::ff00:42:53')))])

class TestIDEAFilterCompiler(unittest.TestCase):
    """
    Unit test class for testing the :py:class:`mentat.idea.internal.IDEAFilterCompiler` class.
    """

    def setUp(self):
        self.cpl = mentat.idea.internal.IDEAFilterCompiler()
        self.psr = pynspect.gparser.PynspectFilterParser()
        self.psr.build()

    def test_01_basic_compilations(self):
        """
        Perform basic compilation tests.
        """
        self.maxDiff = None

        rule = self.psr.parse('(DetectTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('DetectTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('DetectTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(DetectTime == 2016-06-21T13:08:27Z)')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('DetectTime') OP_EQ DATETIME('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('DetectTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(Source.IP4 == "188.14.166.39")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ CONSTANT('188.14.166.39'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ IPV4(IP4('188.14.166.39')))")

        rule = self.psr.parse('(Source.IP4 == 188.14.166.39)')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ IPV4('188.14.166.39'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ IPV4(IP4('188.14.166.39')))")

        rule = self.psr.parse('5 + 6 - 9')
        self.assertEqual(repr(rule), "MATHBINOP(INTEGER(5) OP_PLUS MATHBINOP(INTEGER(6) OP_MINUS INTEGER(9)))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "INTEGER(2)")

        rule = self.psr.parse('Test + 10 - 9')
        self.assertEqual(repr(rule), "MATHBINOP(VARIABLE('Test') OP_PLUS MATHBINOP(INTEGER(10) OP_MINUS INTEGER(9)))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(1))")

        rule = self.psr.parse('Test + (10 - 9)')
        self.assertEqual(repr(rule), "MATHBINOP(VARIABLE('Test') OP_PLUS MATHBINOP(INTEGER(10) OP_MINUS INTEGER(9)))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(1))")

        rule = self.psr.parse('(Test + 10) - 9')
        self.assertEqual(repr(rule), "MATHBINOP(MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(10)) OP_MINUS INTEGER(9))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(10)) OP_MINUS INTEGER(9))")

        rule = self.psr.parse('9 - 6 + Test')
        self.assertEqual(repr(rule), "MATHBINOP(INTEGER(9) OP_MINUS MATHBINOP(INTEGER(6) OP_PLUS VARIABLE('Test')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(INTEGER(9) OP_MINUS MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(6)))")

        rule = self.psr.parse('9 - (6 + Test)')
        self.assertEqual(repr(rule), "MATHBINOP(INTEGER(9) OP_MINUS MATHBINOP(INTEGER(6) OP_PLUS VARIABLE('Test')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(INTEGER(9) OP_MINUS MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(6)))")

        rule = self.psr.parse('(9 - 6) + Test')
        self.assertEqual(repr(rule), "MATHBINOP(MATHBINOP(INTEGER(9) OP_MINUS INTEGER(6)) OP_PLUS VARIABLE('Test'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "MATHBINOP(VARIABLE('Test') OP_PLUS INTEGER(3))")

    def test_02_idea_time_compilations(self):
        """
        Perform datetime compilation tests for :py:class:`mentat.idea.internal.Idea`.
        """
        self.maxDiff = None

        rule = self.psr.parse('(DetectTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('DetectTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('DetectTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(CreateTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('CreateTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('CreateTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(EventTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('EventTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('EventTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(CeaseTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('CeaseTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('CeaseTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(WinStartTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('WinStartTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('WinStartTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(WinEndTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('WinEndTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('WinEndTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

        rule = self.psr.parse('(_Mentat.StorageTime == "2016-06-21T13:08:27Z")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('_Mentat.StorageTime') OP_EQ CONSTANT('2016-06-21T13:08:27Z'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('_Mentat.StorageTime') OP_EQ DATETIME(datetime.datetime(2016, 6, 21, 13, 8, 27)))")

    def test_03_idea_ip_compilations(self):
        """
        Perform IP address compilation tests for :py:class:`mentat.idea.internal.Idea`.
        """
        self.maxDiff = None

        rule = self.psr.parse('(Source.IP4 == "192.168.1.1")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ CONSTANT('192.168.1.1'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP4') OP_EQ IPV4(IP4('192.168.1.1')))")

        rule = self.psr.parse('(Target.IP4 == "192.168.1.1")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Target.IP4') OP_EQ CONSTANT('192.168.1.1'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Target.IP4') OP_EQ IPV4(IP4('192.168.1.1')))")

        rule = self.psr.parse('(Source.IP6 == "::1")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP6') OP_EQ CONSTANT('::1'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP6') OP_EQ IPV6(IP6('::1')))")

        rule = self.psr.parse('(Target.IP6 == "::1")')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Target.IP6') OP_EQ CONSTANT('::1'))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Target.IP6') OP_EQ IPV6(IP6('::1')))")

        rule = self.psr.parse('(Source.IP4 IN ["192.168.1.1","192.168.1.2"])')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP4') OP_IN LIST(CONSTANT('192.168.1.1'), CONSTANT('192.168.1.2')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP4') OP_IN IPLIST(IPV4(IP4('192.168.1.1')), IPV4(IP4('192.168.1.2'))))")

        rule = self.psr.parse('(Target.IP4 IN ["192.168.1.1","192.168.1.2"])')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Target.IP4') OP_IN LIST(CONSTANT('192.168.1.1'), CONSTANT('192.168.1.2')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Target.IP4') OP_IN IPLIST(IPV4(IP4('192.168.1.1')), IPV4(IP4('192.168.1.2'))))")

        rule = self.psr.parse('(Source.IP6 IN ["::1","::2"])')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Source.IP6') OP_IN LIST(CONSTANT('::1'), CONSTANT('::2')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Source.IP6') OP_IN IPLIST(IPV6(IP6('::1')), IPV6(IP6('::2'))))")

        rule = self.psr.parse('(Target.IP6 IN ["::1","::2"])')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('Target.IP6') OP_IN LIST(CONSTANT('::1'), CONSTANT('::2')))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('Target.IP6') OP_IN IPLIST(IPV6(IP6('::1')), IPV6(IP6('::2'))))")

    def test_04_idea_func_compilations(self):
        """
        Perform function compilation tests for :py:class:`mentat.idea.internal.Idea`.
        """
        self.maxDiff = None

        rule = self.psr.parse('(DetectTime < utcnow())')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('DetectTime') OP_LT FUNCTION(utcnow()))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('DetectTime') OP_LT FUNCTION(utcnow()))")

        rule = self.psr.parse('(DetectTime < (utcnow() - 3600))')
        self.assertEqual(repr(rule), "COMPBINOP(VARIABLE('DetectTime') OP_LT MATHBINOP(FUNCTION(utcnow()) OP_MINUS INTEGER(3600)))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(VARIABLE('DetectTime') OP_LT MATHBINOP(FUNCTION(utcnow()) OP_MINUS TIMEDELTA(datetime.timedelta(seconds=3600))))")

        rule = self.psr.parse('(DetectTime + 3600) > utcnow()')
        self.assertEqual(repr(rule), "COMPBINOP(MATHBINOP(VARIABLE('DetectTime') OP_PLUS INTEGER(3600)) OP_GT FUNCTION(utcnow()))")
        res = self.cpl.compile(rule)
        self.assertEqual(repr(res), "COMPBINOP(MATHBINOP(VARIABLE('DetectTime') OP_PLUS TIMEDELTA(datetime.timedelta(seconds=3600))) OP_GT FUNCTION(utcnow()))")


#-------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
Unit test module for testing the :py:mod:`mentat.reports.event` module.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import unittest
from unittest.mock import MagicMock, Mock, call
import datetime

#
# Custom libraries
#
import mentat.const
import mentat.services.sqlstorage
import mentat.services.eventstorage
import mentat.idea.internal
import mentat.reports.utils
import mentat.reports.event
from mentat.datatype.sqldb import GroupModel, FilterModel, NetworkModel, \
    SettingsReportingModel, EventReportModel
from pynspect.jpath import jpath_values

#-------------------------------------------------------------------------------
# NOTE: Sorry for the long lines in this file. They are deliberate, because the
# assertion permutations are (IMHO) more readable this way.
#-------------------------------------------------------------------------------

REPORTS_DIR = '/var/tmp'

class TestMentatReportsEvent(unittest.TestCase):
    """
    Unit test class for testing the :py:mod:`mentat.reports.event` module.
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
                    'IP6': ['2001:db8::ff00:42:0/112'],
                    'Proto': ['ssh']
                }
            ],
            'Target': [
                {
                    'IP4': ['10.2.2.0/24'],
                    'IP6': ['2001:ffff::ff00:42:0/112'],
                    'Proto': ['https']
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
                    'IP4': ['10.0.1.2-10.0.1.5', '10.0.0.0/25', '10.0.0.0/22', '10.0.2.1'],
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
            'Note': 'Test note containing ; CSV delimiter.',
            '_Mentat' : {
                'ResolvedAbuses' : [
                    'abuse@cesnet.cz'
                ],
                'EventClass' : 'anomaly-traffic',
                'EventSeverity': 'low'
            }
        }
    ]

    ideas_obj = list(map(mentat.idea.internal.Idea, ideas_raw))

    template_vars = {
        "report_access_url": "https://URL/view=",
        "contact_email": "EMAIL1", 
        "admin_email": "EMAIL2",
        "default_event_class": "default"
    }

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
        groups_dict = {'abuse@cesnet.cz': group}

        FilterModel(group = group, name = 'FLT1', type = 'basic', filter = 'Node.Name == "org.example.kippo_honey"', description = 'DESC1', enabled = True)
        FilterModel(group = group, name = 'FLT2', type = 'basic', filter = 'Source.IP4 IN [10.0.0.0/24]', description = 'DESC2', enabled = True)
        FilterModel(group = group, name = 'FLT3', type = 'basic', filter = 'Source.IP4 IN [10.0.1.0/28]', description = 'DESC3', enabled = True)
        NetworkModel(group = group, netname = 'UNET1', source = 'manual', network = '10.0.0.0/8')
        SettingsReportingModel(group = group)

        self.sqlstorage.session.add(group)
        self.sqlstorage.session.commit()

        self.reporting_settings = mentat.reports.utils.ReportingSettings(group)
        settings_dict = {'abuse@cesnet.cz': self.reporting_settings}

        def lookup_mock(src, getall = False):
            if str(src).startswith('10.'):
                return [{'abuse_group': 'abuse@cesnet.cz', 'is_base': False}]
            else:
                return []

        whoismodule_mock = mentat.services.whois.WhoisModule()
        whoismodule_mock.lookup = MagicMock(side_effect = lookup_mock)

        self.reporter = mentat.reports.event.EventReporter(
            Mock(),
            REPORTS_DIR,
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../conf/templates/reporter')),
            [],
            'en',
            'UTC',
            self.eventstorage,
            self.sqlstorage,
            mailer = None,
            event_classes_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../conf/event_classes')),
            groups_dict = groups_dict,
            settings_dict = settings_dict,
            whoismodule = whoismodule_mock
        )

    def tearDown(self):
        self.sqlstorage.session.close()
        self.sqlstorage.database_drop()
        self.eventstorage.database_drop()

    def test_01_save_to_json_files(self):
        """
        Test :py:func:`mentat.reports.event.EventReporter._save_to_json_files` function.
        """
        self.maxDiff = None

        # Test saving file without timestamp information.
        report_file = 'utest-security-report.json'
        report_path = os.path.join(REPORTS_DIR, report_file)

        self.assertEqual(
            self.reporter._save_to_json_files( # pylint: disable=locally-disabled,protected-access
                self.ideas_obj,
                report_file
            ),
            (report_path, "{}.zip".format(report_path))
        )
        self.assertTrue(
            os.path.isfile(report_path)
        )
        self.assertTrue(
            os.path.isfile("{}.zip".format(report_path))
        )
        os.unlink(report_path)
        os.unlink("{}.zip".format(report_path))

        # Test saving file with timestamp information.
        report_file = 'utest-security-report-M20180726SL-HT9TC.json'
        report_path = os.path.join(REPORTS_DIR, '20180726', report_file)

        self.assertEqual(
            self.reporter._save_to_json_files( # pylint: disable=locally-disabled,protected-access
                self.ideas_obj,
                report_file
            ),
            (report_path, "{}.zip".format(report_path))
        )
        self.assertTrue(
            os.path.isfile(report_path)
        )
        self.assertTrue(
            os.path.isfile("{}.zip".format(report_path))
        )
        os.unlink(report_path)
        os.unlink("{}.zip".format(report_path))

    def test_02_save_to_files(self):
        """
        Test :py:func:`mentat.reports.event.EventReporter._save_to_files` function.
        """
        self.maxDiff = None

        # Test saving file without timestamp information.
        report_file = 'utest-security-report.txt'
        report_path = os.path.join(REPORTS_DIR, report_file)

        self.assertEqual(
            self.reporter._save_to_files( # pylint: disable=locally-disabled,protected-access
                "TEST CONTENT",
                report_file
            ),
            (report_path, "{}.zip".format(report_path))
        )
        self.assertTrue(
            os.path.isfile(report_path)
        )
        self.assertTrue(
            os.path.isfile("{}.zip".format(report_path))
        )
        os.unlink(report_path)
        os.unlink("{}.zip".format(report_path))

        # Test saving file with timestamp information.
        report_file = 'utest-security-report-M20180726SL-HT9TC.txt'
        report_path = os.path.join(REPORTS_DIR, '20180726', report_file)

        self.assertEqual(
            self.reporter._save_to_files( # pylint: disable=locally-disabled,protected-access
                "TEST CONTENT",
                report_file
            ),
            (report_path, "{}.zip".format(report_path))
        )
        self.assertTrue(
            os.path.isfile(report_path)
        )
        self.assertTrue(
            os.path.isfile("{}.zip".format(report_path))
        )
        os.unlink(report_path)
        os.unlink("{}.zip".format(report_path))

    def test_03_filter_events(self):
        """
        Test :py:class:`mentat.reports.event.EventReporter.filter_events` function.
        """
        self.maxDiff = None

        abuse_group = self.sqlstorage.session.query(GroupModel).filter(GroupModel.name == 'abuse@cesnet.cz').one()
        self.sqlstorage.session.commit()

        events, aggr, fltlog, flt_cnt = self.reporter.filter_events(abuse_group.name, self.ideas_obj)
        self.assertEqual(fltlog, {'FLT1': 1, 'FLT2': 1, 'FLT3': 1})
        self.assertEqual(flt_cnt, 1)
        for events in aggr.values():
            self.assertEqual(len(events), 2)
        self.reporter.logger.assert_has_calls([
            call.debug("Event matched filtering rule '%s' of group %s.", 'FLT1', 'abuse@cesnet.cz'),
            call.debug("Discarding event with ID '%s' from reports.", 'msg01'),
            call.debug('Event matched filtering rules, all sources filtered'),
            call.debug("Event matched filtering rule '%s' of group %s.", 'FLT3', 'abuse@cesnet.cz'),
            call.debug("Discarding event with ID '%s' from reports.", 'msg02'),
            call.debug("Event matched filtering rule '%s' of group %s.", 'FLT2', 'abuse@cesnet.cz'),
            call.debug("Discarding event with ID '%s' from reports.", 'msg02')
        ])
        self.sqlstorage.session.commit()

        events, aggr, fltlog, flt_cnt = self.reporter.filter_events(abuse_group.name, self.ideas_obj)
        self.sqlstorage.session.commit()
        flt1 = self.sqlstorage.session.query(FilterModel).filter(FilterModel.name == 'FLT1').one()
        self.assertEqual(flt1.hits, 2)

        events, aggr, fltlog, flt_cnt = self.reporter.filter_events(abuse_group.name, self.ideas_obj)
        events, aggr, fltlog, flt_cnt = self.reporter.filter_events(abuse_group.name, self.ideas_obj)
        self.sqlstorage.session.commit()
        flt1 = self.sqlstorage.session.query(FilterModel).filter(FilterModel.name == 'FLT1').one()
        self.assertEqual(flt1.hits, 4)

        for aggr in aggr.values():
            aggr = self.reporter.aggregate_events(aggr)
        self.assertEqual(list(sorted(aggr.keys())), ['anomaly-traffic'])
        self.assertEqual(list(aggr['anomaly-traffic'].keys()), ['10.0.2.1', '10.0.0.0/22'])

    def test_04_fetch_severity_events(self):
        """
        Test :py:class:`mentat.reports.event.EventReporter.fetch_severity_events` function.
        """
        self.maxDiff = None

        abuse_group = self.sqlstorage.session.query(GroupModel).filter(GroupModel.name == 'abuse@cesnet.cz').one()
        self.sqlstorage.session.commit()

        events = self.reporter.fetch_severity_events(
            abuse_group,
            'low',
            datetime.datetime.utcnow() - datetime.timedelta(seconds = 7200),
            datetime.datetime.utcnow() + datetime.timedelta(seconds = 7200)
        )
        self.assertEqual(list(map(lambda x: x['ID'], events)), ['msg01', 'msg02'])

        events = self.reporter.fetch_severity_events(
            abuse_group,
            'medium',
            datetime.datetime.utcnow() - datetime.timedelta(seconds = 7200),
            datetime.datetime.utcnow() + datetime.timedelta(seconds = 7200)
        )
        self.assertEqual(list(map(lambda x: x['ID'], events)), [])

        events = self.reporter.fetch_severity_events(
            abuse_group,
            'low',
            datetime.datetime.utcnow() - datetime.timedelta(seconds = 7200),
            datetime.datetime.utcnow() - datetime.timedelta(seconds = 3600)
        )
        self.assertEqual(list(map(lambda x: x['ID'], events)), [])

    def test_05_j2t_idea_path_valueset(self):
        """
        Test :py:class:`mentat.reports.event.EventReporter.j2t_idea_path_valueset` function.
        """
        self.maxDiff = None

        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj[0], 'Source.Proto'),
            ['ssh']
        )
        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj[0], ['Source.Proto', 'Target.Proto']),
            ['https', 'ssh']
        )

        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj[1], 'Source.Proto'),
            []
        )
        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj[1], ['Source.Proto', 'Target.Proto']),
            []
        )

        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj, 'Source.Proto'),
            ['ssh']
        )
        self.assertEqual(
            self.reporter.j2t_idea_path_valueset(self.ideas_obj, ['Source.Proto', 'Target.Proto']),
            ['https', 'ssh']
        )

    def test_06_render_report_summary(self):
        """
        Test :py:class:`mentat.reports.event.EventReporter.render_report_summary` function.
        """
        self.maxDiff = None

        abuse_group = self.sqlstorage.session.query(GroupModel).filter(GroupModel.name == 'abuse@cesnet.cz').one()

        report_txt = self.reporter.render_report(
            self._generate_mock_report(
                abuse_group,
                'low',
                mentat.const.REPORTING_MODE_SUMMARY
            ),
            self.reporting_settings,
            self.template_vars,
            ["file1.json"]
        )
        print("\n---\nSUMMARY REPORT IN EN:\n---\n")
        print(report_txt)
        self.assertTrue(report_txt)
        self.assertEqual(report_txt.split('\n')[0], 'Dear colleagues.')

        self.reporting_settings.locale = 'cs'
        self.reporting_settings.timezone = 'Europe/Prague'

        report_txt = self.reporter.render_report(
            self._generate_mock_report(
                abuse_group,
                'low',
                mentat.const.REPORTING_MODE_SUMMARY
            ),
            self.reporting_settings,
            self.template_vars,
            ["file1.json"]
        )
        print("\n---\nSUMMARY REPORT IN CS:\n---\n")
        print(report_txt)
        self.assertTrue(report_txt)
        self.assertEqual(report_txt.split('\n')[0], 'Vážení kolegové.')

    def test_07_render_report_extra(self):
        """
        Test :py:class:`mentat.reports.event.EventReporter.render_report_extra` function.
        """
        self.maxDiff = None

        abuse_group = self.sqlstorage.session.query(GroupModel).filter(GroupModel.name == 'abuse@cesnet.cz').one()
        self.sqlstorage.session.commit()

        report_txt = self.reporter.render_report(
            self._generate_mock_report(
                abuse_group,
                'low',
                mentat.const.REPORTING_MODE_EXTRA
            ),
            self.reporting_settings,
            self.template_vars,
            '192.168.1.1'
        )
        print("\n---\nEXTRA REPORT IN EN:\n---\n")
        print(report_txt)
        self.assertTrue(report_txt)
        self.assertEqual(report_txt.split('\n')[0], 'Dear colleagues.')

        self.reporting_settings.locale = 'cs'
        self.reporting_settings.timezone = 'Europe/Prague'

        report_txt = self.reporter.render_report(
            self._generate_mock_report(
                abuse_group,
                'low',
                mentat.const.REPORTING_MODE_EXTRA
            ),
            self.reporting_settings,
            self.template_vars,
            '192.168.1.1'
        )
        print("\n---\nEXTRA REPORT IN CS:\n---\n")
        print(report_txt)
        self.assertTrue(report_txt)
        self.assertEqual(report_txt.split('\n')[0], 'Vážení kolegové.')


    #---------------------------------------------------------------------------

    def _generate_mock_report(self, abuse_group, severity, rtype):
        report = EventReportModel(
            groups   = [abuse_group],
            severity = severity,
            type     = rtype,
            dt_from  = datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
            dt_to    = datetime.datetime.utcnow(),

            evcount_rep     = len(self.ideas_obj),
            evcount_all     = len(self.ideas_obj),
            evcount_flt     = len(self.ideas_obj),
            evcount_flt_blk = 1,
            evcount_thr     = len(self.ideas_obj),
            evcount_thr_blk = 0,
            evcount_rlp     = 0,

            filtering = {'FLT01':1}
        )
        report.generate_label()
        report.calculate_delta()

        if rtype == mentat.const.REPORTING_MODE_EXTRA:
            report.parent = EventReportModel(
                groups   = [abuse_group],
                severity = severity,
                type     = mentat.const.REPORTING_MODE_SUMMARY,
                dt_from  = datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
                dt_to    = datetime.datetime.utcnow(),

                evcount_rep     = len(self.ideas_obj),
                evcount_all     = len(self.ideas_obj),
                evcount_flt     = len(self.ideas_obj),
                evcount_flt_blk = 1,
                evcount_thr     = len(self.ideas_obj),
                evcount_thr_blk = 0,
                evcount_rlp     = 0,

                filtering = {'FLT01':1}
            )
            report.parent.generate_label()
            report.parent.calculate_delta()

        report.statistics = mentat.stats.idea.truncate_evaluations(
            mentat.stats.idea.evaluate_events(self.ideas_obj)
        )

        events_aggr = {}
        for obj in self.ideas_obj:
            for src in (jpath_values(obj, 'Source.IP4') + jpath_values(obj, 'Source.IP6')):
                events_aggr[src] = [obj]
        report.structured_data = self.reporter.prepare_structured_data(events_aggr, events_aggr, self.reporting_settings)
        return report


#-------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

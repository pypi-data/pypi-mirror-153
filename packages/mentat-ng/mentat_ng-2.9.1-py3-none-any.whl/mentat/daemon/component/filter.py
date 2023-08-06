#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Daemon component capable of filtering incoming messages with complex filtering
rules.

It is dependent on services of following modules:

* :py:mod:`pynspect.filters`

  Filtering rule library.

* :py:mod:`pynspect.compilers`

  Filtering rule compilation library.

The implementation is based on :py:class:`pyzenkit.zendaemon.ZenDaemonComponent`.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sys
import pprint

#
# Custom libraries.
#
import pyzenkit.zendaemon
from pynspect.gparser import PynspectFilterParser
from pynspect.filters import DataObjectFilter

from mentat.idea.internal import IDEAFilterCompiler


class FilterDaemonComponent(pyzenkit.zendaemon.ZenDaemonComponent):
    """
    Implementation of ZenDaemonComponent encapsulating pynspect library.
    """
    EVENT_MSG_PROCESS = 'message_process'

    def __init__(self, **kwargs):
        """
        Perform component initializations.
        """
        super().__init__(**kwargs)

        # Unique component identifier
        self.cid = kwargs.get('cid', 'filer')

        self.filter_rules_key = kwargs.get('filter_rules_key', 'filter_rules')

        self.filter_parser   = PynspectFilterParser()
        self.filter_compiler = IDEAFilterCompiler()
        self.filter          = DataObjectFilter()

        self.filter_parser.build()

        # Permit changing of default event mapping
        self.event_map = kwargs.get('event_map', {
            self.EVENT_MSG_PROCESS:  self.EVENT_MSG_PROCESS
        })

    def get_events(self):
        """
        Get the list of event names and their appropriate callback handlers.
        """
        return [
            { 'event': self.event_map[self.EVENT_MSG_PROCESS], 'callback': self.cbk_event_message_process, 'prepend': False }
        ]

    def setup(self, daemon):
        """
        Perform component setup.
        """
        self.filter_rules_cfg = daemon.c(self.filter_rules_key)
        daemon.dbgout("[STATUS] Component '{}': Loading filter rules {}".format(self.cid, pprint.pformat(self.filter_rules_cfg)))

        self.filter_rules = []
        for rule in self.filter_rules_cfg:
            try:
                flt = self.filter_parser.parse(rule['rule'])
                flt = self.filter_compiler.compile(flt)
                nme = rule.get('name', rule['rule'])
                self.filter_rules.append({
                    "rule": nme,
                    "filter": flt
                })
                daemon.logger.debug("[STATUS] Component '{}': Loaded filter rule '{}'".format(self.cid, nme))
            except:
                daemon.logger.debug("[STATUS] Component '{}': Unable to load filter rule '{}'".format(self.cid, rule))


    #---------------------------------------------------------------------------


    def cbk_event_message_process(self, daemon, args):
        """
        Print the message contents into the log.
        """
        daemon.logger.debug("Filtering message: '{}'".format(args['id']))
        try:
            for rule in self.filter_rules:
                if self.filter.filter(rule["filter"], args['idea']):
                    daemon.logger.debug("Message '{}' filtered out by filter '{}'".format(args['id'], rule["rule"]))
                    daemon.queue.schedule('message_cancel', args)
                    return (daemon.FLAG_STOP, args)
                else:
                    daemon.logger.debug("Message '{}' passed by filter '{}'".format(args['id'], rule["rule"]))
            return (daemon.FLAG_CONTINUE, args)
        except:
            daemon.logger.debug("Message '{}' caused some trouble during processing: '{}'".format(args['id'], sys.exc_info()[1]))
            daemon.queue.schedule('message_banish', args)
            return (daemon.FLAG_STOP, args)

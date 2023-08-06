#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
`IDEA <https://idea.cesnet.cz/en/index>`__ message enrichment plugin for the
:ref:`section-bin-mentat-enricher` daemon module performing lookup of all
``Source/IPx`` addresses within configured **whois** service.

.. todo::

    Documentation is still work in progress, please refer to the source code for
    details.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import collections
import pprint


#
# Custom libraries
#
import pynspect.jpath
import mentat.const
import mentat.services.whois


class WhoisEnricherPlugin:
    """
    Enricher plugin performing lookup of all Source/IPx addresses within configured
    whois service.
    """

    def __init__(self):
        self.whois_service = None

    def setup(self, daemon, config_updates = None):
        """
        Setup plugin.
        """
        whois_manager = mentat.services.whois.WhoisServiceManager(
            daemon.config,
            config_updates
        )
        self.whois_service = whois_manager.service()
        daemon.logger.info(
            "Initialized '%s' enricher plugin: %s",
            self.__class__.__name__,
            pprint.pformat(self.whois_service.status())
        )

    def process(self, daemon, message_id, message):
        """
        Process and enrich given message.
        """
        daemon.logger.debug(
            "WHOIS - processing message '%s'",
            message_id
        )

        sources = []
        sources += pynspect.jpath.jpath_values(message, 'Source.IP4')
        sources += pynspect.jpath.jpath_values(message, 'Source.IP6')

        resolved_abuses = collections.defaultdict(int)
        for src in sources:
            result = self.whois_service.lookup_abuse(src)
            if result is None:
                continue

            for res in result:
                resolved_abuses[res] += 1

        changed = False
        resolved_abuses = sorted(resolved_abuses.keys())
        if resolved_abuses:
            pynspect.jpath.jpath_set(message, '_Mentat.ResolvedAbuses', resolved_abuses)
            daemon.logger.debug(
                "WHOIS - Enriched message '%s' with attribute '_Mentat.ResolvedAbuses' and values %s",
                message_id,
                pprint.pformat(resolved_abuses)
            )
            changed = True

        return (daemon.FLAG_CONTINUE, changed)

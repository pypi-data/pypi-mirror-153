#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
Daemon component capable of storing IDEA messages into persistent storage.
Currently only `PostgreSQL <https://www.postgresql.org/>`__ database is supported.

It is dependent on services of following modules:

* :py:mod:`mentat.services.eventstorage`

  Interface for working with persistent storage.

The implementation is based on :py:class:`pyzenkit.zendaemon.ZenDaemonComponent`.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import time
import datetime
import traceback


#
# Custom libraries
#
import pyzenkit.zendaemon
import pynspect.jpath
import mentat.services.eventstorage


CONFIG_COMMIT_BULK     = 'commit_bulk'
CONFIG_COMMIT_BULKINTV = 'commit_bulk_interval'
CONFIG_COMMIT_BULKTHR  = 'commit_bulk_threshold'


class StorageDaemonComponent(pyzenkit.zendaemon.ZenDaemonComponent):
    """
    Daemon component capable of storing IDEA messages into database.
    """
    EVENT_START          = 'start'
    EVENT_STOP           = 'stop'

    EVENT_MSG_PROCESS    = 'message_process'
    EVENT_DBH_COMMIT     = 'dbh_commit'
    EVENT_LOG_STATISTICS = 'log_statistics'

    STATS_CNT_STORED = 'cnt_stored'
    STATS_CNT_ERRORS = 'cnt_errors'
    STATS_CNT_COMMIT_THRESHOLD  = 'cnt_eci_threshold'
    STATS_CNT_COMMIT_TIMEOUT    = 'cnt_eci_timeout'
    STATS_CNT_COMMITS_THRESHOLD = 'cnt_cis_threshold'
    STATS_CNT_COMMITS_TIMEOUT   = 'cnt_cis_timeout'

    def __init__(self, **kwargs):
        """
        Perform component initializations.
        """
        super().__init__(**kwargs)

        # Unique component identifier
        self.cid = kwargs.get('cid', 'storage')

        self.event_service      = None
        self.event_gateway      = None
        self.commit_bulk        = None
        self.commit_bulkintv    = None
        self.commit_bulkthr     = None
        self.events_uncommitted = None
        self.last_commit        = None

        # Permit changing of default event mapping
        self.event_map = kwargs.get('event_map', {
            self.EVENT_START:          self.EVENT_START,
            self.EVENT_STOP:           self.EVENT_STOP,
            self.EVENT_MSG_PROCESS:    self.EVENT_MSG_PROCESS,
            self.EVENT_DBH_COMMIT:     self.EVENT_DBH_COMMIT,
            self.EVENT_LOG_STATISTICS: self.EVENT_LOG_STATISTICS
        })

    def _event_insert_now(self, daemon, args):
        # Attempt to store IDEA message into database with immediate commit.
        self.event_service.insert_event(args['idea'])
        daemon.logger.info(
            "Component '{}': Stored message '{}':'{}' into database.".format(
                self.cid,
                args['id'],
                args['idea_id']
            )
        )

    def _event_insert_bulk(self, daemon, args):
        # Attempt to store IDEA message into database with delayed commit.
        self.event_service.insert_event_bulkci(args['idea'])
        daemon.logger.info(
            "Component '{}': Stored message '{}':'{}' into database (bulk mode).".format(
                self.cid,
                args['id'],
                args['idea_id']
            )
        )

        self.events_uncommitted += 1
        if not self.events_uncommitted % self.commit_bulkthr:
            daemon.logger.info(
                "Component '{}': Bulk commit threshold '{}' hit, performing commit.".format(
                    self.cid,
                    self.commit_bulkthr
                )
            )
            self.event_service.commit_bulk()
            self.inc_statistic(self.STATS_CNT_COMMIT_THRESHOLD, self.events_uncommitted)
            self.inc_statistic(self.STATS_CNT_COMMITS_THRESHOLD)
            self.events_uncommitted = 0
            self.last_commit = time.time()

    def _setup_insert_now(self, daemon):
        self.commit_bulk = False
        self.event_gateway = self._event_insert_now

    def _setup_insert_bulk(self, daemon):
        self.commit_bulk = True
        self.event_gateway = self._event_insert_bulk
        self.commit_bulkintv = daemon.c(CONFIG_COMMIT_BULKINTV)
        self.commit_bulkthr = daemon.c(CONFIG_COMMIT_BULKTHR)
        self.events_uncommitted = 0
        self.last_commit = time.time()

    def setup(self, daemon):
        """
        Perform component setup.
        """
        esm = mentat.services.eventstorage.EventStorageServiceManager(daemon.config)
        self.event_service = esm.service()
        self.commit_bulk = daemon.c(CONFIG_COMMIT_BULK)
        daemon.logger.debug(
            "[STATUS] Component '{}': Set up event storage service.".format(
                self.cid
            )
        )
        if self.commit_bulk:
            self._setup_insert_bulk(daemon)
            daemon.logger.info(
                "[STATUS] Component '{}': Using bulk commits with '{}' as enforced commit interval".format(
                    self.cid,
                    self.commit_bulkintv
                )
            )
            daemon.logger.info(
                "[STATUS] Component '{}': Using bulk commits with '{}' as bulk commit threshold".format(
                    self.cid,
                    self.commit_bulkthr
                )
            )
        else:
            self._setup_insert_now(daemon)

    def get_events(self):
        """
        Get the list of event names and their appropriate callback handlers.
        """
        return [
            {
                'event': self.event_map[self.EVENT_START],
                'callback': self.cbk_event_start,
                'prepend': False
            },
            {
                'event': self.event_map[self.EVENT_STOP],
                'callback': self.cbk_event_stop,
                'prepend': False
            },
            {
                'event': self.event_map[self.EVENT_MSG_PROCESS],
                'callback': self.cbk_event_message_process,
                'prepend': False
            },
            {
                'event': self.event_map[self.EVENT_DBH_COMMIT],
                'callback': self.cbk_event_database_commit,
                'prepend': False
            },
            {
                'event': self.event_map[self.EVENT_LOG_STATISTICS],
                'callback': self.cbk_event_log_statistics,
                'prepend': False
            }
        ]

    #---------------------------------------------------------------------------

    def cbk_event_start(self, daemon, args):
        """
        Start the component.
        """
        daemon.logger.debug(
            "Component '{}': Starting the component".format(
                self.cid
            )
        )
        if self.commit_bulk:
            daemon.logger.info(
                "Component '{}': Running in bulk commit mode.".format(
                    self.cid
                )
            )
            daemon.queue.schedule(self.EVENT_DBH_COMMIT)

        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_stop(self, daemon, args):
        """
        Stop the component.
        """
        daemon.logger.debug(
            "Component '{}': Stopping the component".format(
                self.cid
            )
        )
        # In case we are running in bulk commit mode.
        if self.commit_bulk:
            daemon.logger.info(
                "Component '{}': Committing all pending messages and switching to immediate commit mode.".format(
                    self.cid
                )
            )
            # Commit all currently pending IDEA messages.
            self._commit_pending()
            # Switch to immediate commit mode for the rest of the messages in the queue.
            self._setup_insert_now(daemon)

        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_message_process(self, daemon, args):
        """
        Store the message into the persistent storage.
        """
        daemon.logger.debug(
            "Component '{}': Storing message '{}':'{}'.".format(
                self.cid,
                args['id'],
                args['idea_id']
            )
        )
        try:
            # Set current time as _Mentat.StorageTime.
            pynspect.jpath.jpath_set(args['idea'], '_Mentat.StorageTime', datetime.datetime.utcnow())

            # Attempt to store IDEA message into database.
            self.event_gateway(daemon, args)

            self.inc_statistic(self.STATS_CNT_STORED)
            return (daemon.FLAG_CONTINUE, args)

        except:  # pylint: disable=locally-disabled,bare-except
            daemon.logger.error(
                "Component '{}': Unable to store IDEA message '{}' into database: '{}'".format(
                    self.cid,
                    args['id'],
                    traceback.format_exc()
                )
            )
            daemon.queue.schedule('message_banish', args)

            self.inc_statistic(self.STATS_CNT_ERRORS)
            return (daemon.FLAG_STOP, args)

    def cbk_event_database_commit(self, daemon, args):
        """
        Check, whether there are any messages waiting to be committed for greater than
        configured time period. Commit them if necessary to avoid loss of data.
        """
        daemon.logger.debug(
            "Component '{}': Checking whether commit needs to be enforced".format(
                self.cid
            )
        )

        if self.events_uncommitted and ((time.time() - self.last_commit) > self.commit_bulkintv):
            daemon.logger.info(
                "Component '{}': Commit timeout '{}' elapsed, performing commit.".format(
                    self.cid,
                    self.commit_bulkintv
                )
            )
            self._commit_pending()

        daemon.queue.schedule_after(self.commit_bulkintv, self.EVENT_DBH_COMMIT)
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_log_statistics(self, daemon, args):
        """
        Periodical processing statistics logging.
        """
        stats = self.get_statistics()
        stats_str = ''

        for k in [self.STATS_CNT_STORED, self.STATS_CNT_ERRORS, self.STATS_CNT_COMMIT_TIMEOUT, self.STATS_CNT_COMMIT_THRESHOLD, self.STATS_CNT_COMMITS_TIMEOUT, self.STATS_CNT_COMMITS_THRESHOLD]:
            if k in stats:
                stats_str = self.pattern_stats.format(stats_str, k, stats[k]['cnt'], stats[k]['inc'], stats[k]['spd'])
            else:
                stats_str = self.pattern_stats.format(stats_str, k, 0, 0, 0)

        daemon.logger.info(
            "Component '{}': *** Processing statistics ***{}".format(
                self.cid,
                stats_str
            )
        )
        return (daemon.FLAG_CONTINUE, args)

    def _commit_pending(self):
        self.event_service.commit_bulk()
        self.inc_statistic(self.STATS_CNT_COMMIT_TIMEOUT, self.events_uncommitted)
        self.inc_statistic(self.STATS_CNT_COMMITS_TIMEOUT)
        self.events_uncommitted = 0
        self.last_commit = time.time()

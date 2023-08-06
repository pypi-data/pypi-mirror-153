#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This Mentat module is a script providing database management functions and features.

This script is implemented using the :py:mod:`pyzenkit.zenscript` framework and
so it provides all of its core features. See the documentation for more in-depth
details.

It is further based on :py:mod:`mentat.script.fetcher` module, which provides
database fetching and message post-processing capabilities.


Usage examples
--------------

.. code-block:: shell

    # Display help message and exit.
    mentat-dbmngr.py --help

    # Run in debug mode (enable output of debugging information to terminal).
    mentat-dbmngr.py --debug

    # Run with increased logging level.
    mentat-dbmngr.py --log-level debug

    # Perform initial database schema creation (both IDEA event and metadata dbs).
    mentat-dbmngr.py --command init

    # Reinitialize metadata database (drop and create, data destructive!).
    mentat-dbmngr.py --command reinit-main

    # Rebuild all IDEA event database indices.
    mentat-dbmngr.py --command reindex-event

    # Insert/remove demonstration data (accounts, groups, filters and networks).
    mentat-dbmngr.py --command fixtures-add
    mentat-dbmngr.py --command fixtures-remove

    # Check IDEA event database for recently stored objects, send email warning
    # in case no new objects were stored in configured time interval.
    mentat-dbmngr.py --command watchdog-events
    mentat-dbmngr.py --command watchdog-events --watchdog-delta 3600

    # Same as above, only execute and produce output in Nagios plugin compatible
    # mode.
    mentat-dbmngr.py --command watchdog-events --nagios-plugin --log-level warning

    # Add new user account to the database. Usefull for creating initial account
    # after fresh installation. Note the use of double quotes to pass values
    # containing spaces (name, organization) and the use of commas to pass multiple
    # roles:
    mentat-dbmngr.py --command user-add login=admin "fullname=Clark Kent" email=kent@dailyplanet.com "organization=Daily Planet, inc." roles=user,admin


Available script commands
-------------------------

``init`` (*default*)
    Perform necessary database initializations including creating all required
    indices.

``fixtures-add``
    Populate database with demonstration objects - fixtures (user accounts and groups).

``fixtures-remove``
    Remove demonstration objects from database - fixtures (user accounts and groups).

``reinit-main``
    Reinitialize main database (drop whole database and recreate).

``reindex-event``
    Rebuild event database indices (drop all indices and recreate).

``user-add``
    Add new user account into the database.

``watchdog-events``
    Check IDEA event database table for last message storage time and send out
    warning email in a case the last message stored is way too old. This simple
    watchdog should be able to detect issues in message processing chain. Optionally
    when used with ``--nagios-plugin`` option the direct warning mailing  feature
    is suppressed and output and return code is in compliance with Nagios plugin
    development guidelines.


Custom configuration
--------------------

Custom command line options
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``--watchdog-delta value``
    Time interval delta in hours for watchdog checks.

    *Type:* ``integer``, *default:* ``2``

``--mail-subject value``
    Subject for the database watchdog emails.

    *Type:* ``string``, *default:* ``Mentat database watchdog alert``

``--mail-from value``
    Source email address for the database watchdog emails.

    *Type:* ``string``, *default:* ``root``

``--mail-to value``
    Target email address for the database watchdog emails.

    *Type:* ``string``, *default:* ``root``

``--nagios-plugin``
    Execute as Nagios plugin (flag).

    *Type:* ``bool``, *default:* ``False``

"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import smtplib
import datetime
from email.mime.text import MIMEText

#
# Custom libraries
#
import pyzenkit.zenscript
import mentat.script.fetcher
import mentat.const

from mentat.datatype.sqldb import UserModel
from mentat.fixtures import MentatFixtures


class MentatDbmngrScript(mentat.script.fetcher.FetcherScript):
    """
    Implementation of Mentat module (script) providing database management functions
    and features.
    """

    #
    # Class constants.
    #

    # List of configuration keys.
    CONFIG_WATCHDOG_DELTA  = 'watchdog_delta'
    CONFIG_MAIL_SUBJECT    = 'mail_subject'
    CONFIG_MAIL_FROM       = 'mail_from'
    CONFIG_MAIL_TO         = 'mail_to'
    CONFIG_NAGIOS_PLUGIN   = 'nagios_plugin'
    CONFIG_ADDITIONAL_ARGS = 'additional_args'

    def __init__(self):
        """
        Initialize dbmngr script object. This method overrides the base
        implementation in :py:func:`pyzenkit.zenscript.ZenScript.__init__` and
        it aims to even more simplify the script object creation by providing
        configuration values for parent contructor.
        """
        self.eventservice = None
        self.sqlservice   = None

        super().__init__(
            description = 'mentat-dbmngr.py - Mentat database management script'
        )

    def _init_argparser(self, **kwargs):
        """
        Initialize script command line argument parser. This method overrides the
        base implementation in :py:func:`pyzenkit.zenscript.ZenScript._init_argparser`
        and it must return valid :py:class:`argparse.ArgumentParser` object. It
        appends additional command line options custom for this script object.

        This method is called from the main constructor in :py:func:`pyzenkit.baseapp.BaseApp.__init__`
        as a part of the **__init__** stage of application`s life cycle.

        :param kwargs: Various additional parameters passed down from object constructor.
        :return: Valid argument parser object.
        :rtype: argparse.ArgumentParser
        """
        argparser = super()._init_argparser(**kwargs)

        #
        # Create and populate options group for custom script arguments.
        #
        arggroup_script = argparser.add_argument_group('custom script arguments')

        arggroup_script.add_argument(
            '--watchdog-delta',
            type = int,
            default = None,
            help = 'time interval delta in seconds for watchdog checks'
        )
        arggroup_script.add_argument(
            '--mail-subject',
            type = str,
            default = None,
            help = 'subject for the database watchdog emails'
        )
        arggroup_script.add_argument(
            '--mail-from',
            type = str,
            default = None,
            help = 'source email address for the database watchdog emails'
        )
        arggroup_script.add_argument(
            '--mail-to',
            type = str,
            default = None,
            help = 'target email address for the database watchdog emails'
        )
        arggroup_script.add_argument(
            '--nagios-plugin',
            action='store_true',
            default = None,
            help = 'execute as Nagios plugin (flag)'
        )
        arggroup_script.add_argument(
            'additional_args',
            nargs='*',
            help = 'optional additional arguments'
        )

        return argparser

    def _init_config(self, cfgs, **kwargs):
        """
        Initialize default script configurations. This method overrides the base
        implementation in :py:func:`pyzenkit.zenscript.ZenScript._init_config`
        and it appends additional configurations via ``cfgs`` parameter.

        This method is called from the main constructor in :py:func:`pyzenkit.baseapp.BaseApp.__init__`
        as a part of the **__init__** stage of application`s life cycle.

        :param list cfgs: Additional set of configurations.
        :param kwargs: Various additional parameters passed down from constructor.
        :return: Default configuration structure.
        :rtype: dict
        """
        cfgs = (
            (self.CONFIG_WATCHDOG_DELTA,  900),
            (self.CONFIG_MAIL_SUBJECT,    'Mentat database watchdog alert'),
            (self.CONFIG_MAIL_FROM,       'root'),
            (self.CONFIG_MAIL_TO,         'root'),
            (self.CONFIG_NAGIOS_PLUGIN,   False),
            (self.CONFIG_ADDITIONAL_ARGS, [])
        ) + cfgs
        return super()._init_config(cfgs, **kwargs)


    #---------------------------------------------------------------------------


    def get_default_command(self):
        """
        Return the name of the default script command. This command will be executed
        in case it is not explicitly selected either by command line option, or
        by configuration file directive.

        :return: Name of the default command.
        :rtype: str
        """
        return 'init'

    def cbk_command_init(self):
        """
        Implementation of the **init** command.

        Perform necessary database initializations including creating all
        required indices.
        """
        self.logger.info("Initializing main database.")
        self.sqlservice.database_create()
        self.logger.info("Initializing event database.")
        self.eventservice.database_create()
        self.logger.info("Initializing event database indices.")
        self.eventservice.index_create()

        return self.RESULT_SUCCESS

    def cbk_command_fixtures_add(self):
        """
        Implementation of the **fixtures-add** command.

        Populate database with demonstration objects - fixtures (user accounts
        and groups).
        """
        self.logger.info("Populating main database with demonstration objects.")

        MentatFixtures(self.eventservice, self.sqlservice, self.logger).import_to_db()

        return self.RESULT_SUCCESS

    def cbk_command_fixtures_remove(self):
        """
        Implementation of the **fixtures-remove** command.

        Remove demonstration objects from database - fixtures (user accounts
        and groups).
        """
        self.logger.info("Removing demonstration objects from main database.")

        MentatFixtures(self.eventservice, self.sqlservice, self.logger).remove_from_db()

        return self.RESULT_SUCCESS

    def cbk_command_reinit_main(self):
        """
        Implementation of the **reinit-main** command.

        Reinitialize main database (drop and create).
        """
        self.logger.info("Dropping main database.")
        self.sqlservice.database_drop()
        self.logger.info("Initializing main database.")
        self.sqlservice.database_create()

        return self.RESULT_SUCCESS

    def cbk_command_reindex_event(self):
        """
        Implementation of the **reindex-event** command.

        Drop existing indices in **event** database and recreate them according
        to current configuration.
        """
        self.logger.info("Dropping current indices in event database.")
        self.eventservice.index_drop()
        self.logger.info("Initializing event database indices.")
        self.eventservice.index_create()

        return self.RESULT_SUCCESS

    def cbk_command_user_add(self):
        """
        Implementation of the **user-add** command.

        Add new user account into the database.
        """
        self.logger.info("Creating new user account.")

        account_user = UserModel(
            enabled = True
        )

        for attr in self.c(self.CONFIG_ADDITIONAL_ARGS):
            key, value = attr.split('=', 2)
            if not key or not value:
                raise pyzenkit.zenscript.ZenScriptException(
                    "Invalid user account attribute: {}".format(str(attr))
                )

            if key == 'login':
                account_user.login = value
            elif key == 'fullname':
                account_user.fullname = value
            elif key == 'email':
                account_user.email = value
            elif key == 'organization':
                account_user.organization = value
            elif key == 'roles':
                account_user.roles = value.split(',')

        for attrname in ('login', 'fullname', 'email', 'organization', 'roles'):
            if not getattr(account_user, attrname, None):
                raise pyzenkit.zenscript.ZenScriptException(
                    "Please provide user`s {} as \"{}=value\" command line argument".format(
                        attrname,
                        attrname
                    )
                )

        try:
            self.sqlservice.session.add(account_user)
            self.sqlservice.session.commit()
            self.logger.info("Added user account to database: '%s'", str(account_user))
            return self.RESULT_SUCCESS

        except Exception as exc:
            self.sqlservice.session.rollback()
            self.logger.info("Unable to add user account to database: '%s' (%s)", str(account_user), str(exc))
            return self.RESULT_FAILURE

    def cbk_command_watchdog_events(self):
        """
        Implementation of the **watchdog-events** command.

        Check appropriate database collections for last updates and send warning
        email in case the last message stored is way too old. This simple watchdog
        should be able to detect issues in message processing chain.
        """
        result = {}

        wdelta = datetime.timedelta(seconds = self.c(self.CONFIG_WATCHDOG_DELTA))
        st_from = datetime.datetime.utcnow() - wdelta
        self.logger.info("Looking for messages stored after '%sZ' (in last %s)", st_from.isoformat(), str(wdelta))

        watchdog_result = self.eventservice.watchdog_events(self.c(self.CONFIG_WATCHDOG_DELTA))
        self.logger.debug("Watchdog query: %s", self.eventservice.cursor.lastquery)
        if watchdog_result:
            self.logger.info("Successfully found some messages stored after '%sZ' (in last %s)", st_from.isoformat(), str(wdelta))
        else:
            self.logger.info("Found no messages stored after '%sZ' (in last %s)", st_from.isoformat(), str(wdelta))

        if not self.c(self.CONFIG_NAGIOS_PLUGIN):
            if watchdog_result:
                result['alert_sent'] = False
            else:
                result['alert_sent'] = True
                self._email_watchdog_events(st_from, wdelta)
        else:
            if watchdog_result:
                print("MENTATDB OK - new events stored after {:s}Z;|{:s}Z;".format(
                    st_from.isoformat(),
                    st_from.isoformat()
                ))
                self.retc = mentat.const.NAGIOS_PLUGIN_RC_OK
            else:
                print("MENTATDB CRITICAL - No new events stored after {:s}Z;|{:s}Z;0".format(
                    st_from.isoformat(),
                    st_from.isoformat()
                ))
                self.retc = mentat.const.NAGIOS_PLUGIN_RC_CRITICAL

        return result


    #---------------------------------------------------------------------------


    def _email_watchdog_events(self, st_from, wdelta):
        """
        Helper method for sending watchdog alerts.
        """
        msg = MIMEText("""ATTENTION: No new IDEA events were stored into database after {stfrom} !!!

This alert means there were no new messages stored into IDEA event
database table at least in last {delta}.

This may or may not be a problem, but you might consider checking
that all Mentat real-time message processing modules are configured
and working correctly.

Regards

mentat-watchdog.py
""".format(stfrom = st_from.isoformat(), delta = str(wdelta)))

        msg['Subject'] = self.c(self.CONFIG_MAIL_SUBJECT)
        msg['From']    = self.c(self.CONFIG_MAIL_FROM)
        msg['To']      = self.c(self.CONFIG_MAIL_TO)

        self.logger.info("Sending watchdog alert to '%s' as '%s'", msg['To'], msg['From'])
        smtp = smtplib.SMTP('localhost')
        smtp.send_message(msg)
        smtp.quit()

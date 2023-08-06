#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Mentat system management and inspection library.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


from mentat.datatype.sqldb import UserModel, GroupModel, NetworkModel,\
    FilterModel, SettingsReportingModel


class MentatFixtures():
    """
    Class representing Mentat real-time module configuration for control utility.
    """
    def __init__(self, eventservice, sqlservice, logservice):
        self.eventservice = eventservice
        self.sqlservice   = sqlservice
        self.logservice   = logservice

    def import_to_db(self):
        """
        Import data fixtures into database.
        """
        account_user = UserModel(
            login = 'user',
            fullname = 'Demo User',
            email = 'user@bogus-domain.org',
            organization = 'BOGUS DOMAIN, a.l.e.',
            roles = ['user'],
            enabled = True
        )
        account_developer = UserModel(
            login = 'developer',
            fullname = 'Demo Developer',
            email = 'developer@bogus-domain.org',
            organization = 'BOGUS DOMAIN, a.l.e.',
            roles = ['user', 'developer'],
            enabled = True
        )
        account_maintainer = UserModel(
            login = 'maintainer',
            fullname = 'Demo Maintainer',
            email = 'maintainer@bogus-domain.org',
            organization = 'BOGUS DOMAIN, a.l.e.',
            roles = ['user', 'maintainer'],
            enabled = True
        )
        account_admin = UserModel(
            login = 'admin',
            fullname = 'Demo Admin',
            email = 'admin@bogus-domain.org',
            organization = 'BOGUS DOMAIN, a.l.e.',
            roles = ['user', 'admin'],
            enabled = True
        )
        group = GroupModel(
            name = 'DEMO_GROUP',
            source = 'manual',
            description = 'Demo Group',
            enabled = True
        )
        group.members.append(account_user)
        group.members.append(account_developer)
        group.members.append(account_maintainer)
        group.members.append(account_admin)

        group.managers.append(account_maintainer)
        group.managers.append(account_admin)

        SettingsReportingModel(
            group = group,
            emails_low = ['abuse@bogus-domain.org'],
            redirect = True
        )

        NetworkModel(
            group = group,
            netname = 'NETNAME1',
            source = 'manual',
            network = '192.168.0.0/24',
            description = 'First demonstration IPv4 network'
        )
        NetworkModel(
            group = group,
            netname = 'NETNAME2',
            source = 'manual',
            network = '195.113.144.0/24',
            description = 'Second demonstration IPv4 network'
        )
        NetworkModel(
            group = group,
            netname = 'NETNAME3',
            source = 'manual',
            network = '2001::/16',
            description = 'First demonstration IPv6 network'
        )

        FilterModel(
            group = group,
            name = 'Filter Queeg',
            type = 'advanced',
            filter = 'Node.Name == "cz.cesnet.queeg"',
            description = 'Filter out all messages originating from cz.cesnet.queeg detection node'
        )

        for dbobject in [account_user, account_developer, account_maintainer, account_admin, group]:
            try:
                self.sqlservice.session.add(dbobject)
                self.sqlservice.session.commit()
                self.logservice.info("Added demo object to database: '%s'", str(dbobject))
            except Exception as exc:
                self.sqlservice.session.rollback()
                self.logservice.info("Unable to add demo object to database: '%s' (%s)", str(dbobject), str(exc))

    def remove_from_db(self):
        """
        Remove data fixtures from database.
        """
        q_account_user = self.sqlservice.session.query(UserModel).filter(UserModel.login == 'user')
        q_account_developer = self.sqlservice.session.query(UserModel).filter(UserModel.login == 'developer')
        q_account_maintainer = self.sqlservice.session.query(UserModel).filter(UserModel.login == 'maintainer')
        q_account_admin = self.sqlservice.session.query(UserModel).filter(UserModel.login == 'admin')
        q_group = self.sqlservice.session.query(GroupModel).filter(GroupModel.name == 'DEMO_GROUP')
        self.sqlservice.session.commit()

        for q_dbobject in [q_account_user, q_account_developer, q_account_maintainer, q_account_admin, q_group]:
            try:
                dbobject = q_dbobject.first()
                if dbobject:
                    self.sqlservice.session.delete(dbobject)
                    self.sqlservice.session.commit()
                    self.logservice.info("Deleted demo object from database: '%s'", str(dbobject))
            except Exception as exc:
                self.sqlservice.session.rollback()
                self.logservice.info("Unable to remove demo object from database: '%s'", str(exc))


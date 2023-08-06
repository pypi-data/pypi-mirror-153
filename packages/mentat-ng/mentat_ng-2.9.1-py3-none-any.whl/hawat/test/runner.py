#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base library for Hawat unit tests.
"""

import vial.const
import vial.test.fixtures

from mentat.datatype.sqldb import UserModel, GroupModel, ItemChangeLogModel, SettingsReportingModel, FilterModel, NetworkModel
from mentat.const import CKEY_CORE_DATABASE, CKEY_CORE_DATABASE_EVENTSTORAGE

from hawat import create_app_full
from hawat.app import _config_app
from hawat.const import CFGKEY_MENTAT_CORE


def _config_testapp_hawat(app_config):
    """
    Configure and reconfigure application for testing before instantination.
    """
    _config_app(app_config)

    # Now customize configurations for testing purposes.
    app_config['TESTING'] = True
    app_config['WTF_CSRF_ENABLED'] = False
    app_config['DEBUG'] = False
    app_config['EXPLAIN_TEMPLATE_LOADING'] = False
    app_config['LOG_FILE'] = '/var/tmp/mentat-hawat-utest.log'
    app_config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mentat:mentat@localhost/mentat_utest'
    app_config['MAIL_SERVER'] = 'localhost'
    app_config['MAIL_PORT'] = 1025
    app_config['MAIL_DEFAULT_SENDER'] = 'root@unittest'
    app_config['EMAIL_ADMINS'] = ['admin@unittest']
    app_config['MODELS'] = {
        vial.const.MODEL_USER: UserModel,
        vial.const.MODEL_GROUP: GroupModel,
        vial.const.MODEL_ITEM_CHANGELOG: ItemChangeLogModel
    }
    app_config[CFGKEY_MENTAT_CORE][CKEY_CORE_DATABASE][CKEY_CORE_DATABASE_EVENTSTORAGE] = {
        'dbname': 'mentat_utest',
        'user': 'mentat',
        'password': 'mentat',
        'host': 'localhost',
        'port': 5432
    }


class TestRunnerMixin:
    """
    Class for testing :py:class:`hawat.base.HawatApp` application.
    """
    def setup_app(self):
        return create_app_full(
            config_object = 'hawat.config.TestingConfig',
            config_func = _config_testapp_hawat
        )

    def get_fixtures_db(self, app):
        fixture_list = vial.test.fixtures.get_fixtures_db(app)
        for fixture in fixture_list:
            if isinstance(fixture, app.get_model(vial.const.MODEL_USER)):
                fixture.organization = 'BOGUS DOMAIN, a.l.e.'
            elif isinstance(fixture, app.get_model(vial.const.MODEL_GROUP)):
                fixture.source = 'manual'
                SettingsReportingModel(group = fixture)
                FilterModel(
                    group = fixture,
                    name = 'FLT_{}'.format(fixture.name),
                    type = 'basic',
                    filter = 'Source.IP4 == 127.0.0.1',
                    enabled = True,
                    description = 'Filter for {}'.format(fixture.name)
                )
                NetworkModel(
                    group = fixture,
                    netname = 'NET_{}'.format(fixture.name),
                    source = 'manual',
                    network = '192.168.0.0/24',
                    description = 'Description for network NET_{}'.format(fixture.name)
                )
        return fixture_list

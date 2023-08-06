#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains default configurations for Hawat application. One of the
classes defined in this module may be passed as argument to :py:func:`hawat.app.create_app_full`
factory function to bootstrap Hawat default configurations. These values may be
then optionally overwritten by external configuration file and/or additional
configuration file defined indirrectly via environment variable. Please refer to
the documentation of :py:func:`hawat.app.create_app_full` factory function for more
details on this process.

There are following predefined configuration classess available:

:py:class:`hawat.config.ProductionConfig`
    Default configuration suite for production environments.

:py:class:`hawat.config.DevelopmentConfig`
    Default configuration suite for development environments.

:py:class:`hawat.config.TestingConfig`
    Default configuration suite for testing environments.

There is also following constant structure containing mapping of simple configuration
names to configuration classess:

:py:const:`CONFIG_MAP`

It is used from inside of :py:func:`hawat.app.create_app` factory method to pick
and apply correct configuration class to application. Please refer to the documentation
of :py:func:`hawat.app.create_app` factory function for more details on this process.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import socket

from flask_babel import lazy_gettext

import pyzenkit.jsonconf
import pyzenkit.utils

import vial.config

import mentat.const
from mentat.datatype.sqldb import UserModel, GroupModel, ItemChangeLogModel


class Config(vial.config.Config):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Base class for default configurations of Hawat application. You are free to
    extend and customize contents of this class to provide better default values
    for your particular environment.

    The configuration keys must be a valid Flask configuration and so they must
    be written in UPPERCASE to be correctly recognized.
    """

    APPLICATION_NAME = "Mentat"
    APPLICATION_ID   = "mentat"

    #
    # Flask-Mail configurations.
    #
    MAIL_DEFAULT_SENDER = '{}@{}'.format(APPLICATION_ID, socket.getfqdn())
    MAIL_SUBJECT_PREFIX = '[{}]'.format(APPLICATION_NAME)

    #
    # Flask-Migrate configurations.
    #
    MIGRATE_DIRECTORY = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        'migrations'
    )

    #---------------------------------------------------------------------------
    # Custom application configurations.
    #---------------------------------------------------------------------------

    ROLES = vial.const.ROLES
    """List of all valid user roles supported by the application."""

    MODELS = {
        vial.const.MODEL_USER: UserModel,
        vial.const.MODEL_GROUP: GroupModel,
        vial.const.MODEL_ITEM_CHANGELOG: ItemChangeLogModel
    }
    """Models to be used within the application."""

    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.design_bs3',
        'vial.blueprints.devtools',
        'vial.blueprints.changelogs',

        'hawat.blueprints.auth_env',
        'hawat.blueprints.auth_pwd',
        'hawat.blueprints.home',
        'hawat.blueprints.reports',
        'hawat.blueprints.events',
        'hawat.blueprints.hosts',
        'hawat.blueprints.timeline',
        'hawat.blueprints.dnsr',
        #'hawat.blueprints.pdnsr',
        'hawat.blueprints.geoip',
        #'hawat.blueprints.nerd',
        'hawat.blueprints.whois',
        'hawat.blueprints.performance',
        'hawat.blueprints.status',
        'hawat.blueprints.dbstatus',
        'hawat.blueprints.users',
        'hawat.blueprints.groups',
        'hawat.blueprints.settings_reporting',
        'hawat.blueprints.filters',
        'hawat.blueprints.networks',
    ]
    """List of requested application blueprints to be loaded during setup."""

    DISABLED_ENDPOINTS = []
    """List of endpoints disabled on application level."""

    MENU_MAIN_SKELETON = [
        {
            'entry_type': 'submenu',
            'ident': 'dashboards',
            'position': 100,
            'title': lazy_gettext('Dashboards'),
            'resptitle': True,
            'icon': 'section-dashboards'
        },
        {
            'entry_type': 'submenu',
            'ident': 'more',
            'position': 200,
            'title': lazy_gettext('More'),
            'resptitle': True,
            'icon': 'section-more',
        },
        {
            'entry_type': 'submenu',
            'ident': 'admin',
            'position': 300,
            'authentication': True,
            'authorization': ['power'],
            'title': lazy_gettext('Administration'),
            'resptitle': True,
            'icon': 'section-administration'
        },
        {
            'entry_type': 'submenu',
            'ident': 'developer',
            'position': 400,
            'authentication': True,
            'authorization': ['developer'],
            'title': lazy_gettext('Development'),
            'resptitle': True,
            'icon': 'section-development'
        }
    ]
    """Configuration of application menu skeleton."""

    HAWAT_REPORT_FEEDBACK_MAILS = ['root@{}'.format(socket.getfqdn())]
    """List of system administrator emails, that receive feedback messages for reports."""

    HAWAT_CHART_TIMELINE_MAXSTEPS = 200
    """Maximal number of steps (bars) displayed in timeline chart."""

    HAWAT_LIMIT_AODS = 20
    """Limit for number of objects for which to automatically fetch additional data services."""

    HAWAT_SEARCH_QUERY_QUOTA = 7
    """Event search query quota per each user."""

    SQLALCHEMY_SETUP_ARGS = {
        'metadata': mentat.datatype.sqldb.MODEL.metadata,
        'model_class': mentat.datatype.sqldb.MODEL,
        'query_class': mentat.services.sqlstorage.RetryingQuery
    }


class ProductionConfig(Config, vial.config.ProductionConfig):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing application configurations for *production* environment.
    """


class DevelopmentConfig(Config, vial.config.DevelopmentConfig):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing application configurations for *development* environment.
    """

    #EXPLAIN_TEMPLATE_LOADING = True

    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.design_bs3',
        'vial.blueprints.devtools',
        'vial.blueprints.changelogs',

        'hawat.blueprints.auth_env',
        'hawat.blueprints.auth_dev',
        'hawat.blueprints.auth_pwd',
        'hawat.blueprints.home',
        'hawat.blueprints.reports',
        'hawat.blueprints.events',
        'hawat.blueprints.hosts',
        'hawat.blueprints.timeline',
        'hawat.blueprints.dnsr',
        #'hawat.blueprints.pdnsr',
        'hawat.blueprints.geoip',
        #'hawat.blueprints.nerd',
        'hawat.blueprints.whois',
        'hawat.blueprints.performance',
        'hawat.blueprints.status',
        'hawat.blueprints.dbstatus',
        'hawat.blueprints.users',
        'hawat.blueprints.groups',
        'hawat.blueprints.settings_reporting',
        'hawat.blueprints.filters',
        'hawat.blueprints.networks',
    ]


class TestingConfig(Config, vial.config.TestingConfig):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing *testing* Hawat applications` configurations.
    """
    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.design_bs3',
        'vial.blueprints.devtools',
        'vial.blueprints.changelogs',

        'hawat.blueprints.auth_env',
        'hawat.blueprints.auth_dev',
        'hawat.blueprints.auth_pwd',
        'hawat.blueprints.home',
        'hawat.blueprints.reports',
        'hawat.blueprints.events',
        'hawat.blueprints.hosts',
        'hawat.blueprints.timeline',
        'hawat.blueprints.dnsr',
        #'hawat.blueprints.pdnsr',
        'hawat.blueprints.geoip',
        #'hawat.blueprints.nerd',
        'hawat.blueprints.whois',
        'hawat.blueprints.performance',
        'hawat.blueprints.status',
        'hawat.blueprints.dbstatus',
        'hawat.blueprints.users',
        'hawat.blueprints.groups',
        'hawat.blueprints.settings_reporting',
        'hawat.blueprints.filters',
        'hawat.blueprints.networks',
    ]


CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     ProductionConfig
}
"""Configuration map for easy mapping of configuration aliases to config objects."""


def get_app_root_relative_config():
    """
    These configurations are relative to APP_ROOT_PATH environment setting and
    must be handled separately.
    """
    return {
        'MENTAT_CORE': pyzenkit.jsonconf.config_load_dir(
            pyzenkit.utils.get_resource_path(mentat.const.PATH_CFG_CORE)
        ),
        'MENTAT_PATHS': {
            'path_crn': pyzenkit.utils.get_resource_path(mentat.const.PATH_CRN),
            'path_cfg': pyzenkit.utils.get_resource_path(mentat.const.PATH_CFG),
            'path_var': pyzenkit.utils.get_resource_path(mentat.const.PATH_VAR),
            'path_log': pyzenkit.utils.get_resource_path(mentat.const.PATH_LOG),
            'path_run': pyzenkit.utils.get_resource_path(mentat.const.PATH_RUN),
            'path_tmp': pyzenkit.utils.get_resource_path(mentat.const.PATH_TMP),
        },
        'MENTAT_CACHE_DIR': pyzenkit.utils.get_resource_path(
            os.path.join(mentat.const.PATH_VAR, 'cache')
        ),
        'MENTAT_CONTROLLER_CFG': pyzenkit.utils.get_resource_path(
            os.path.join(mentat.const.PATH_CFG, 'mentat-controller.py.conf')
        ),
        'LOG_FILE': pyzenkit.utils.get_resource_path(
            os.path.join(mentat.const.PATH_LOG, 'mentat-hawat.py.log')
        )
    }

def get_default_config_file():
    """
    Get path to default configuration file based on the environment.
    """
    return os.path.join(
        pyzenkit.utils.get_resource_path(mentat.const.PATH_CFG),
        'mentat-hawat.py.conf'
    )

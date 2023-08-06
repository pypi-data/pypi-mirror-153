#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains default *Vial* application configurations.
"""


import os
import socket
import collections
from flask_babel import lazy_gettext

import vial.const


class Config:  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Base class for default configurations of Vial application. You are free to
    extend and customize contents of this class to provide better default values
    for your particular environment.

    The configuration keys must be a valid Flask configuration and so they must
    be written in UPPERCASE to be correctly recognized.
    """

    APPLICATION_NAME = "Vial"
    APPLICATION_ID   = "vial"

    #---------------------------------------------------------------------------
    # Flask internal configurations. Please refer to Flask documentation for
    # more information about each configuration key.
    #---------------------------------------------------------------------------

    DEBUG      = False
    TESTING    = False
    SECRET_KEY = 'default-secret-key'

    #---------------------------------------------------------------------------
    # Flask extension configurations. Please refer to the documentation of that
    # particular Flask extension for more details.
    #---------------------------------------------------------------------------

    #
    # Flask-WTF configurations.
    #
    WTF_CSRF_ENABLED = True

    #
    # Flask-Mail configurations.
    #
    MAIL_SERVER         = 'localhost'
    MAIL_PORT           = 25
    MAIL_USERNAME       = None
    MAIL_PASSWORD       = None
    MAIL_DEFAULT_SENDER = '{}@{}'.format(APPLICATION_ID, socket.getfqdn())
    MAIL_SUBJECT_PREFIX = '[{}]'.format(APPLICATION_NAME)

    #
    # Flask-Babel configurations.
    #
    BABEL_DEFAULT_LOCALE   = vial.const.DEFAULT_LOCALE
    BABEL_DEFAULT_TIMEZONE = vial.const.DEFAULT_TIMEZONE
    BABEL_DETECT_LOCALE    = True
    """Custom configuration, make detection of best possible locale optional to enable forcing default."""

    #
    # Flask-SQLAlchemy configurations.
    #
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_SETUP_ARGS          = {}

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

    MODELS = {}
    """Models to be used within the application."""

    SUPPORTED_LOCALES = collections.OrderedDict([
        ('en', 'English'),
        ('cs', 'Česky')
    ])
    """List of all languages (locales) supported by the application."""

    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.auth_env',
        'vial.blueprints.auth_pwd',
        'vial.blueprints.devtools',
        'vial.blueprints.design_bs3',
        'vial.blueprints.home',
        'vial.blueprints.users',
        'vial.blueprints.groups',
        'vial.blueprints.changelogs'
    ]
    """List of requested application blueprints to be loaded during setup."""

    DISABLED_ENDPOINTS = []
    """List of endpoints disabled on application level."""

    ENDPOINT_LOGIN = 'auth.login'
    """
    Default login view. Users will be redirected to this view in case they are not
    authenticated, but the authentication is required for the requested endpoint.
    """

    LOGIN_MSGCAT = 'info'
    """Default message category for messages related to user authentication."""

    ENDPOINT_HOME = 'home.index'
    """Homepage endpoint."""

    ENDPOINT_LOGIN_REDIRECT = 'home.index'
    """Default redirection endpoint after login."""

    ENDPOINT_LOGOUT_REDIRECT = 'home.index'
    """Default redirection endpoint after logout."""

    MENU_MAIN_SKELETON = [
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

    EMAIL_ADMINS = ['root@{}'.format(socket.getfqdn())]
    """List of system administrator emails."""

    LOG_DEFAULT_LEVEL = 'info'
    """Default logging level, case insensitive. One of the values ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``."""

    LOG_FILE_LEVEL = 'info'
    """File logging level, case insensitive. One of the values ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``."""

    LOG_EMAIL_LEVEL = 'error'
    """File logging level, case insensitive. One of the values ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``."""

    ICONS = vial.const.ICONS


class ProductionConfig(Config):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing application configurations for *production* environment.
    """


class DevelopmentConfig(Config):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing application configurations for *development* environment.
    """

    #---------------------------------------------------------------------------
    # Flask internal configurations. Please refer to Flask documentation for
    # more information about each configuration key.
    #---------------------------------------------------------------------------


    DEBUG = True

    #EXPLAIN_TEMPLATE_LOADING = True

    #DEBUG_TB_PROFILER_ENABLED = True

    #---------------------------------------------------------------------------
    # Custom application configurations.
    #---------------------------------------------------------------------------

    ENDPOINT_LOGIN = 'auth_dev.login'

    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.auth_dev',
        'vial.blueprints.auth_env',
        'vial.blueprints.auth_pwd',
        'vial.blueprints.devtools',
        'vial.blueprints.design_bs3',
        'vial.blueprints.home',
        'vial.blueprints.users',
        'vial.blueprints.groups',
        'vial.blueprints.changelogs'
    ]

    LOG_DEFAULT_LEVEL = 'debug'

    LOG_FILE_LEVEL = 'debug'


class TestingConfig(Config):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class containing *testing* Vial applications` configurations.
    """

    #---------------------------------------------------------------------------
    # Flask internal configurations. Please refer to Flask documentation for
    # more information about each configuration key.
    #---------------------------------------------------------------------------

    TESTING = True

    EXPLAIN_TEMPLATE_LOADING = False

    #---------------------------------------------------------------------------
    # Custom application configurations.
    #---------------------------------------------------------------------------

    ENDPOINT_LOGIN = 'auth_dev.login'

    ENABLED_BLUEPRINTS = [
        'vial.blueprints.auth',
        'vial.blueprints.auth_api',
        'vial.blueprints.auth_dev',
        'vial.blueprints.auth_env',
        'vial.blueprints.auth_pwd',
        'vial.blueprints.devtools',
        'vial.blueprints.design_bs3',
        'vial.blueprints.home',
        'vial.blueprints.users',
        'vial.blueprints.groups',
        'vial.blueprints.changelogs'
    ]

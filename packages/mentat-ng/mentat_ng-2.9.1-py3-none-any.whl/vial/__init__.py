#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
*Vial* is a lightweight skeleton application with batteries included built on top
of excelent `Flask <http://flask.pocoo.org/>`__ microframework.
"""


__author__  = "Honza Mach <honza.mach.ml@gmail.com>"
__version__ = "1.0.0"


import os


def create_app_full(  # pylint: disable=locally-disabled,too-many-arguments
        app_class,
        app_name,
        config_dict   = None,
        config_object = 'vial.config.ProductionConfig',
        config_file   = None,
        config_env    = 'VIAL_CONFIG_FILE',
        config_func   = None):
    """
    Factory function for building Vial application. This function takes number of
    optional arguments, that can be used to create a very customized instance of
    Vial application. This can be very usefull when extending applications`
    capabilities or for purposes of testing. Each of these arguments has default
    value for the most common application setup, so for disabling it entirely it
    is necessary to provide ``None`` as a value.

    :param class app_class: Flask application class to instantinate.
    :param string app_name: Name of the application, identifier in lowercase.
    :param dict config_dict: Initial default configurations.
    :param str config_object: Name of a class or module containing configurations.
    :param str config_file: Name of a file containing configurations.
    :param str config_env: Name of an environment variable pointing to a file containing configurations.
    :param callable config_func: Callable that will receive app.config as parameter.
    :return: Vial application
    :rtype: vial.app.VialApp
    """

    app = app_class(app_name)

    if config_dict and isinstance(config_dict, dict):
        app.config.update(config_dict)
    if config_object:
        app.config.from_object(config_object)
    if config_file:
        app.config.from_pyfile(config_file)
    if config_env and os.getenv(config_env, None):
        app.config.from_envvar(config_env)
    if config_func and callable(config_func):
        config_func(app.config)

    app.setup_app()

    return app

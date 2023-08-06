#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains logging setup for *Vial* application.
"""


import logging
from logging.handlers import WatchedFileHandler, SMTPHandler


def setup_logging_default(app):
    """
    Setup default application logging features.
    """
    log_level_str = app.config['LOG_DEFAULT_LEVEL'].upper()
    log_level = getattr(
        logging,
        log_level_str,
        None
    )
    if not isinstance(log_level, int):
        raise ValueError(
            'Invalid default log level: %s' % log_level_str
        )

    app.logger.setLevel(log_level)
    app.logger.debug(
        '%s: Default logging services successfully started with level %s',
        app.config['APPLICATION_NAME'],
        log_level_str
    )

    return app


def setup_logging_file(app):
    """
    Setup application logging via watched file (rotated by external command).
    """
    log_level_str = app.config['LOG_FILE_LEVEL'].upper()
    log_level = getattr(
        logging,
        log_level_str,
        None
    )
    if not isinstance(log_level, int):
        raise ValueError(
            'Invalid log file level: %s' % log_level_str
        )

    file_handler = WatchedFileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )

    app.logger.addHandler(file_handler)
    app.logger.debug(
        '%s: File logging services successfully started to file %s with level %s',
        app.config['APPLICATION_NAME'],
        app.config['LOG_FILE'],
        log_level_str
    )

    return app

def setup_logging_email(app):
    """
    Setup application logging via email.
    """
    log_level_str = app.config['LOG_EMAIL_LEVEL'].upper()
    log_level = getattr(
        logging,
        log_level_str,
        None
    )
    if not isinstance(log_level, int):
        raise ValueError(
            'Invalid log email level: %s' % log_level_str
        )

    credentials = None
    secure = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        if app.config['MAIL_USE_TLS']:
            secure = ()

    mail_handler = SMTPHandler(
        mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr = app.config['MAIL_DEFAULT_SENDER'],
        toaddrs = app.config['EMAIL_ADMINS'],
        subject = app.config['MAIL_SUBJECT_PREFIX'] + ' Application Error',
        credentials = credentials,
        secure = secure
    )
    mail_handler.setLevel(log_level)
    mail_handler.setFormatter(
        logging.Formatter('''
Message type: %(levelname)s
Location:     %(pathname)s:%(lineno)d
Module:       %(module)s
Function:     %(funcName)s
Time:         %(asctime)s

Message:

%(message)s
'''))

    app.logger.addHandler(mail_handler)
    app.logger.debug(
        '%s: Email logging services successfully started with level %s',
        app.config['APPLICATION_NAME'],
        log_level_str
    )

    return app

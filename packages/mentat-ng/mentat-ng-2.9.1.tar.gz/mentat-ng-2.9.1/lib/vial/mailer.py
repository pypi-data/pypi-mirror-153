#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains mailer setup for *Vial* application.
"""


import flask_mail


MAILER = flask_mail.Mail()
"""Global application resource: :py:mod:`flask_mail` mailer."""

def on_email_sent(message, app):
    """
    Signal handler for handling :py:func:`flask_mail.email_dispatched` signal.
    Log subject and recipients of all email that have been sent.
    """
    app.logger.info(
        "Sent email '%s' to '%s'",
        message.subject,
        ', '.join(message.recipients)
    )
flask_mail.email_dispatched.connect(on_email_sent)

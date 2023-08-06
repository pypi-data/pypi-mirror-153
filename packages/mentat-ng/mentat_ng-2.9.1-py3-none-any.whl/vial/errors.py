#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains error handling code for *Vial* application.
"""


from werkzeug.http import HTTP_STATUS_CODES
from flask import request, make_response, render_template, jsonify
from flask_babel import gettext
from flask_login import current_user

import vial.const


def wants_json_response():
    """Helper method for detecting prefered response in JSON format."""
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

def error_handler_switch(status_code, exc):
    """Return correct error response (HTML or JSON) based on client preferences."""
    if wants_json_response():
        return api_error_response(status_code, exception = exc)
    return error_response(status_code, exception = exc)

def _make_payload(status_code, message = None, exception = None):
    """Prepare the error response payload regardless of the response type."""
    payload = {
        'status': status_code,
        'error': HTTP_STATUS_CODES.get(status_code, gettext('Unknown error'))
    }
    if message:
        payload['message'] = message
    if exception:
        # Flask built-in exceptions classes come with default description strings.
        # Use these as default for empty message.
        if hasattr(exception.__class__, 'description'):
            payload['message'] = exception.__class__.description
        # Append the whole exception object for developers to make debugging easier.
        if current_user.is_authenticated and current_user.has_role(vial.const.ROLE_DEVELOPER):
            payload['exception'] = exception
    return payload

def error_response(status_code, message = None, exception = None):
    """Generate error response in HTML format."""
    status_code = int(status_code)
    payload = _make_payload(status_code, message, exception)
    return make_response(
        render_template(
            'http_error.html',
            **payload
        ),
        status_code
    )

def api_error_response(status_code, message = None, exception = None):
    """Generate error response in JSON format."""
    status_code = int(status_code)
    payload = _make_payload(status_code, message, exception)
    response = jsonify(payload)
    response.status_code = status_code
    return response

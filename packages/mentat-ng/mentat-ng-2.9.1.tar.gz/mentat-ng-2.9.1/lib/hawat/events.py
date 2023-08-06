#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains couple of simple helpers for working with IDEA messages.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os

#
# Flask related modules.
#
import flask

#
# Custom modules.
#
import pyzenkit.jsonconf
import hawat.const
import mentat.services.eventstorage


_DB = None


def _get_cached_values(cache_file):
    cache_dir = flask.current_app.config.get(
        hawat.const.CFGKEY_MENTAT_CACHE_DIR
    )
    return pyzenkit.jsonconf.json_load(
        os.path.join(
            cache_dir,
            cache_file
        )
    )

def _get_values(cache_file, column):
    try:
        return _get_cached_values(cache_file)
    except FileNotFoundError:
        return db_get().distinct_values(column)

def get_event_source_types():
    """
    Return list of all available event source types.
    """
    return _get_values('itemset-stat-sourcetypes.json', 'source_type')

def get_event_target_types():
    """
    Return list of all available event target types.
    """
    return _get_values('itemset-stat-targettypes.json', 'target_type')

def get_event_detector_types():
    """
    Return list of all available event detector types.
    """
    return _get_values('itemset-stat-detectortypes.json', 'node_type')

def get_event_detectors():
    """
    Return list of all available event detectors.
    """
    return _get_values('itemset-stat-detectors.json', 'node_name')

def get_event_categories():
    """
    Return list of all available event categories.
    """
    return _get_values('itemset-stat-categories.json', 'category')

def get_event_severities():
    """
    Return list of all available event severities.
    """
    return _get_values('itemset-stat-severities.json', 'eventseverity')

def get_event_classes():
    """
    Return list of all available event classes.
    """
    return _get_values('itemset-stat-classes.json', 'eventclass')

def get_event_protocols():
    """
    Return list of all available event protocols.
    """
    return _get_values('itemset-stat-protocols.json', 'protocol')

def get_event_inspection_errs():
    """
    Return list of all available event inspection errors.
    """
    return _get_values('itemset-stat-inspectionerrors.json', 'inspectionerrors')

def db_settings(app):
    """
    Return database settings from Mentat core configurations.

    :return: Database settings.
    :rtype: dict
    """
    return app.mconfig

def get_event_enums():
    # Get lists of available options for various event search form select fields.
    enums = {}
    enums.update(
        source_types    = get_event_source_types(),
        target_types    = get_event_target_types(),
        detectors       = get_event_detectors(),
        detector_types  = get_event_detector_types(),
        categories      = get_event_categories(),
        severities      = get_event_severities(),
        classes         = get_event_classes(),
        protocols       = get_event_protocols(),
        inspection_errs = get_event_inspection_errs()
    )
    enums.update(
        host_types = sorted(list(set(enums['source_types'] + enums['target_types']))),
    )
    return enums

def get_event_form_choices():
    enums = get_event_enums()
    choices = {}
    for key, vals in enums.items():
        choices[key] = list(zip(vals, vals))
    return choices

def db_init(app):
    """
    Initialize connection to event database.
    """
    mentat.services.eventstorage.init(db_settings(app))
    app.eventdb = mentat.services.eventstorage.service()


def db_get():
    """
    Opens a new database connection if there is none yet for the
    current application context.

    :return: Database storage handler.
    :rtype: flask_sqlalchemy.SQLAlchemy
    """
    return mentat.services.eventstorage.service()


def db_cursor():
    """
    Convenience method.
    """
    return db_get().session

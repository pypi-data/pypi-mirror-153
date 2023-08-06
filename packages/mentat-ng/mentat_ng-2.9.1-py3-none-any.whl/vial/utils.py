#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains various usefull utilities for *Vial* application.
"""


import os
import uuid
import copy
import datetime
import json
import yaml


class URLParamsBuilder:
    """
    Small utility class for building URL parameter dictionaries for various view
    endpoints.

    .. note::

        This class is still proof of concept and work in progress.
    """
    def __init__(self, skeleton = None):
        self.rules = []
        self.kwrules = {}
        self.skeleton = skeleton or {}

    @staticmethod
    def _add_scalar(dst, key, val):
        if val is not None:
            dst[key] = val

    @staticmethod
    def _add_vector(dst, key, val):
        if val is not None:
            dst.setdefault(key, []).append(val)

    def add_rule(self, key, as_list = False, optional = False):
        """
        Add new rule to URL parameter builder.

        :param str key: Name of the rule key.
        :param bool as_list: Indication that the rule parameter is a list of multiple values.
        :param bool optional: Indication that the rule parameter is optional.
        """
        if as_list:
            rule = [key, self._add_vector, True, optional]
            self.rules.append(rule)
        else:
            rule = [key, self._add_scalar, False, optional]
            self.rules.append(rule)
        return self

    def add_kwrule(self, key, as_list = False, optional = False):
        """
        Add new keyword rule to URL parameter builder.

        :param str key: Name of the rule key.
        :param bool as_list: Indication that the rule parameter is a list of multiple values.
        :param bool optional: Indication that the rule parameter is optional.
        """
        if as_list:
            rule = [key, self._add_vector, True, optional]
            self.kwrules[key] = rule
        else:
            rule = [key, self._add_scalar, False, optional]
            self.kwrules[key] = rule
        return self

    def get_params(self, *args, **kwargs):
        """
        Get URL parameters as dictionary with filled-in values.
        """
        tmp = copy.deepcopy(self.skeleton)
        for idx, rule in enumerate(self.rules):
            try:
                rule[1](tmp, rule[0], args[idx])
            except IndexError:
                if not rule[3]:
                    raise
        for key, rule in self.kwrules.items():
            if key in kwargs:
                rule[1](tmp, rule[0], kwargs[key])
        return tmp


class LimitCounter:
    """
    Simple configurable limit counter with support for multiple keys.
    """
    def __init__(self, limit):
        self.counters = {}
        self.limit    = limit

    def count_and_check(self, key, increment = 1):
        """
        Increment key counter and check against internal limit.
        """
        self.counters[key] = self.counters.get(key, 0) + increment
        return self.counters[key] <= self.limit


#------------------------------------------------------------------------------


def get_timedelta(tstamp):
    """
    Get timedelta from current UTC time and given datetime object.

    :param datetime.datetime: Datetime of the lower timedelta boundary.
    :return: Timedelta object.
    :rtype: datetime.timedelta
    """
    return datetime.datetime.utcnow() - tstamp

def get_datetime_utc(aware = False):
    """
    Get current UTC datetime.

    :return: Curent UTC datetime.
    :rtype: datetime.datetime
    """
    if aware:
        return datetime.datetime.now(datetime.timezone.utc)
    return datetime.datetime.utcnow()

def parse_datetime(dtstring):
    """
    Parse given datetime string.

    :param str dtstring: Datetime string in ISON format to parse.
    :return: Curent UTC datetime.
    :rtype: datetime.datetime
    """
    return datetime.datetime.fromisoformat(dtstring)

def get_datetime_local():
    """
    Get current local timestamp.

    :return: Curent local timestamp.
    :rtype: datetime.datetime
    """
    return datetime.datetime.now()

def check_file_exists(filename):
    """
    Check, that given file exists in the filesystem.

    :param str filename: Name of the file to check.
    :return: Existence flag as ``True`` or ``False``.
    :rtype: bool
    """
    return os.path.isfile(filename)

def in_query_params(haystack, needles, on_true = True, on_false = False, on_empty = False):
    """
    Utility method for checking that any needle from given list of needles is
    present in given haystack.
    """
    if not haystack:
        return on_empty
    for needle in needles:
        if needle in haystack:
            return on_true
    return on_false

def generate_query_params(baseparams, updates):
    """
    Generate query parameters for GET method form.

    :param dict baseparams: Original query parameters.
    :param dict updates: Updates for query parameters.
    :return: Deep copy of original parameters modified with given updates.
    :rtype: dict
    """
    result = copy.deepcopy(baseparams)
    result.update(updates)
    return result

def json_to_yaml(json_data):
    """
    Include given file in raw form directly into the generated content.
    This may be usefull for example for including JavaScript files
    directly into the HTML page.
    """
    return yaml.dump(
        yaml.safe_load(
            json_data
        ),
        default_flow_style=False
    )

def get_uuid4():
    """
    Generate random UUID identifier.
    """
    return uuid.uuid4()

def load_json_from_file(filename):
    """
    Load JSON from given file.
    """
    with open(filename) as fhnd:
        res = json.load(fhnd)
    return res

def make_copy_deep(data):
    """
    Make a deep copy of given data structure.
    """
    return copy.deepcopy(data)

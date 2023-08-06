#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module provides classess and tools for object representation of
`IDEA <https://idea.cesnet.cz/en/index>`__ messages in Mentat project.

This module is based on ``idea.lite`` module from `idea <https://homeproj.cesnet.cz/git/idea.git>`__
package. It is attempting to reuse already defined structures wherever
and whenever possible and only append few custom datatypes to existing
definition.

The most important part of this module, which is available to users, is
the :py:class:`mentat.idea.internal.Idea` class. Following code snippet
demonstates use case scenario:

.. code-block:: python

    >>> import mentat.idea.internal

    # IDEA messages ussually come from regular dicts or JSON
    >>> idea_raw = {...}

    # Just pass the dict as parameter to constructor
    >>> idea_msg = mentat.idea.internal.Idea(idea_raw)

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import json
import pprint

import typedcols
import idea.base
import idea.lite

import ipranges

import pynspect.jpath
import pynspect.rules
import pynspect.compilers


def mentat_dict_typedef(flavour, list_flavour, errors_list, abuses_list, addon=None):
    """
    Typedef generator helper for easy usage of custom definitions at
    multiple places.
    """
    mentat_def = {
        "InspectionErrors": {
            "description": "List of event pecularities found during inspection",
            "type": errors_list
        },
        "StorageTime": {
            "description": "Unix timestamp of the moment the message was stored into database",
            "type": flavour["Timestamp"]
        },
        "EventTemplate": {
            "description": "Template used to generate the event (deprecated)",
            "type": flavour["String"]
        },
        "EventClass": {
            "description": "Event class determined by inspection",
            "type": flavour["String"]
        },
        "EventSeverity": {
            "description": "Event severity determined by inspection",
            "type": flavour["String"]
        },
        "Impact": {
            "description": "More user friendly description of event impact, used for reporting (IDMEF legacy)",
            "type": flavour["String"]
        },
        "ResolvedAbuses": {
            "description": "Abuse contacts related to any alert source",
            "type": abuses_list
        },
        "SourceResolvedASN": {
            "description": "AS numbers related to any alert source",
            "type": list_flavour["Integer"]
        },
        "SourceResolvedCountry": {
            "description": "Coutry ISO codes related to any alert source",
            "type": list_flavour["String"]
        }
    }
    if addon is not None:
        mentat_def.update(addon)
    return mentat_def


class MentatDict(typedcols.TypedDict):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    This type definition represents a custom subdictionary under key
    *_Mentat*/*_CESNET* in message root dictionary.
    """
    allow_unknown = True
    typedef = mentat_dict_typedef(
        idea.lite.idea_types,
        idea.lite.idea_lists,
        typedcols.typed_list("InspectionErrorsList", str),
        typedcols.typed_list("ResolvedAbusesList", str)
    )


def internal_base_addon_typedef(flavour, list_flavour, mentat_dict, addon=None):  # pylint: disable=locally-disabled,unused-argument
    """
    Typedef generator helper for easy usage of custom definitions at
    multiple places.
    """
    addon_def = {
        "ts": {
            "description": "CESNET specific timestamp as NTP timestamp",
            "type": flavour["Timestamp"]
        },
        "ts_u": {
            "description": "CESNET specific timestamp as native Unix timestamp",
            "type": flavour["Integer"]
        },
        "_Mentat": {
            "description": "Custom CESNET/Mentat abominations to IDEA definition",
            "type": mentat_dict
        },
        "_CESNET": {
            "description": "Custom CESNET/Mentat abominations to IDEA definition",
            "type": mentat_dict
        }
    }
    if addon is not None:
        addon_def.update(addon)
    return addon_def


class Idea(idea.lite.Idea):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    This class attempts to make only very contained changes to original
    ``idea.lite.Idea`` class, so that there is no need to update this class
    in case underlying definition changes.

    To make these changes, the *addon* feature of ``typedcols`` library is
    used.
    """
    allow_unknown = True
    typedef = idea.base.idea_typedef(
        idea.lite.idea_types,
        idea.lite.idea_lists,
        idea.lite.idea_defaults,
        typedcols.typed_list("SourceList", idea.lite.SourceTargetDict),
        typedcols.typed_list("TargetList", idea.lite.SourceTargetDict),
        typedcols.typed_list("AttachList", idea.lite.AttachDict),
        typedcols.typed_list("NodeList", idea.lite.NodeDict),
        internal_base_addon_typedef(
            idea.lite.idea_types,
            idea.lite.idea_lists,
            MentatDict
        )
    )

    json_default = staticmethod(idea.lite.Idea.json_default)
    """
    Helper method for JSON serialization of :py:class:`mentat.idea.internal.Idea`
    messages.

    Example usage:

    .. code-block:: python

        >>>import json
        >>>idea_internal = ...
        >>>json.dumps(idea_internal, indent=4, sort_keys=True, default=idea_internal.json_default)
    """

    @staticmethod
    def from_json(json_string):
        """
        Instantinate message object directly from given JSON serialized string.
        """
        return Idea(json.loads(json_string))

    def get_id(self):
        """
        Convenience method for returning message identifier.

        :return: Value of message attribute ``idea['ID']``.
        :rtype: str
        """
        return self['ID']

    def get_detect_time(self):
        """
        Convenience method for returning message detection time.

        :return: Value of message attribute ``idea['DetectTime']``.
        :rtype: datetime.datetime
        """
        return self['DetectTime']

    def get_custom_key(self):
        """
        Convenience method for returning the correct custom key.

        :return: The value of _Mentat if present, otherwise the value of _CESNET if present.
        If neither of those keys exist then empty dictionary is returned.
        :rtype: mentat_dict
        """
        return self.get('_Mentat') if '_Mentat' in self else self.get('_CESNET', {})

    def get_storage_time(self):
        """
        Convenience method for returning message storage time.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['StorageTime']``.
        :rtype: datetime.datetime
        """
        return self.get_custom_key().get('StorageTime', None)

    def get_class(self):
        """
        Convenience method for returning message event class.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['EventClass']``.
        :rtype: str
        """
        return self.get_custom_key().get('EventClass', None)

    def get_severity(self):
        """
        Convenience method for returning message event severity.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['EventSeverity']``.
        :rtype: str
        """
        return self.get_custom_key().get('EventSeverity', None)

    def get_abuses(self):
        """
        Convenience method for returning list of all resolved abuses.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['ResolvedAbuses']``.
        :rtype: list of strings
        """
        return list(self.get_custom_key().get('ResolvedAbuses', list()))

    def get_categories(self):
        """
        Convenience method for returning list of all message categories.

        :return: Value of message attribute ``idea['Category']``.
        :rtype: list of strings
        """
        return list(self['Category'])

    def get_description(self):
        """
        Convenience method for returning message description.

        :return: Value of message attribute ``idea['description']``.
        :rtype: list of strings
        """
        return self.get('Description', None)

    def get_detectors(self):
        """
        Convenience method for returning list of all message detectors.

        :return: Value of message attribute ``idea['Node']['Name']``.
        :rtype: list of strings
        """
        return [name for name in (node.get('Name', None) for node in self.get('Node', [])) if name]

    @staticmethod
    def get_ranges(addresses, rngcls, ipcls):
        """
        Helper function for making ranges of IP addresses.

        :param list addrs: List of single addresses, nets or ranges of IP4 or IP6 addresses.
        :param class rngcls: The class of returned list (either IP4Range or IP6Range).
        :param class ipcls: The class of single IP address (either IP4 or IP6).
        :return: The list of ranges of IP addresses.
        :rtype: list of ``rngcls`` objects
        """
        addrs = sorted(addresses, reverse = True, key = lambda ip: ip.high())

        result = []
        prev = None
        ipmin = None
        ipmax = None

        for curr in addrs:
            if not prev:
                ipmin = curr.low()
                ipmax = curr.high()
            else:
                if curr.high() + 1 >= ipmin:
                    ipmin = min(curr.low(), ipmin)
                else:
                    result.append(rngcls((ipmin, ipmax)) if ipmin != ipmax else ipcls(ipmin))
                    ipmin = curr.low()
                    ipmax = curr.high()
            prev = curr

        if ipmin and ipmax:
            result.append(rngcls((ipmin, ipmax)) if ipmin != ipmax else ipcls(ipmin))

        return result

    def get_addresses(self, node, get_v4 = True, get_v6 = True):
        """
        Convenience method for returning list of all addresses (both v4 and v6)
        for given node (``Source`` and ``Target``).

        :param str node: Type of the node (``Source`` or ``Target``).
        :param bool get_v4: Fetch IPv4 addressess.
        :param bool get_v6: Fetch IPv6 addressess.
        :return: Value of message attributes ``idea[node]['IP4']`` and ``idea[node]['IP6']``.
        :rtype: list of ipranges
        """
        result = []
        ip4s = []
        ip6s = []

        if node in self:
            for src in self[node]:
                if get_v4 and 'IP4' in src:
                    ip4s.extend(list(src['IP4']))
                if get_v6 and 'IP6' in src:
                    ip6s.extend(list(src['IP6']))

            result.extend(self.get_ranges(ip4s, ipranges.IP4Range, ipranges.IP4))
            result.extend(self.get_ranges(ip6s, ipranges.IP6Range, ipranges.IP6))

        return result

    def get_ports(self, node):
        """
        Convenience method for returning list of all ports for given node
        (``Source`` and ``Target``).

        :param str node: Type of the node (``Source`` or ``Target``).
        :return: Value of message attributes ``idea[node]['Port']``.
        :rtype: list of int
        """
        result = set()
        if node in self:
            for src in self[node]:
                if 'Port' in src:
                    for item in list(src['Port']):
                        result.add(item)
        return sorted(list(result))

    def get_protocols(self, node):
        """
        Convenience method for returning list of all protocols for given node
        (``Source`` and ``Target``).

        :param str node: Type of the node (``Source`` or ``Target``).
        :return: Value of message attributes ``idea[node]['Port']``.
        :rtype: list of int
        """
        result = set()
        if node in self:
            for src in self[node]:
                if 'Proto' in src:
                    for item in list(src['Proto']):
                        result.add(str(item).lower())
        return sorted(list(result))

    def get_types(self, node):
        """
        Convenience method for returning list of all types for given node
        (``Source``, ``Target`` and ``Node``).

        :param str node: Type of the node (``Source``, ``Target`` or ``Node``).
        :return: Value of message attributes ``idea[node]['Port']``.
        :rtype: list of int
        """
        result = set()
        if node in self:
            for src in self[node]:
                if 'Type' in src:
                    for item in list(src['Type']):
                        result.add(item)
        return sorted(list(result))

    def get_countries_src(self):
        """
        Convenience method for returning list of all resolved source countries.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['SourceResolvedCountry']``.
        :rtype: list of strings
        """
        return list(
            self.get_custom_key().get('SourceResolvedCountry', [])
        )

    def get_asns_src(self):
        """
        Convenience method for returning list of all resolved source ASNs.

        :return: Value of message attribute ``idea['_Mentat'/'_CESNET']['SourceResolvedASN']``.
        :rtype: list of strings
        """
        return list(
            self.get_custom_key().get('SourceResolvedASN', [])
        )

    def get_inspection_errors(self):
        """
        Convenience method for returning a list of inspection errors.

        :return: List of values of ``idea['_Mentat']['InspectionErrors']``.
        :rtype: list
        """
        return self.get_jpath_values('_Mentat.InspectionErrors' if '_Mentat' in self else '_CESNET.InspectionErrors')

    def get_jpath_value(self, jpath):
        """
        Return single (first in case o a list) value on given JPath within the
        IDEA message.

        :param str jpath: JPath as defined in :py:mod:`pynspect.jpath` module.
        :return: Single (or first) value on given JPath.
        """
        return pynspect.jpath.jpath_value(self, jpath)

    def get_jpath_values(self, jpath):
        """
        Return all values on given JPath within the IDEA message.

        :param str jpath: JPath as defined in :py:mod:`pynspect.jpath` module.
        :return: List of all values on given JPath.
        :rtype: list
        """
        return pynspect.jpath.jpath_values(self, jpath)


class IdeaGhost(Idea):
    """
    This class represents simplified IDEA message objects as reconstructed from
    SQL records retrieved from database. These records are represented by the
    :py:class:`mentat.idea.sqldb.Idea` class, however the native database record
    object is used when the message is fetched from database.

    Objects of this class ARE NOT a perfect 1to1 match with original objects based
    on :py:class:`mentat.idea.internal.Idea`. During the conversion to database
    representation some of the information gets lost due to the design of the data
    model optimized for database search. However from the point of view of the
    searching these objects are same, because there is the same set of categories,
    source and target IPs and all other message attributes, so they can be used
    as representatives in use cases where the full message is not necessary. The
    big pro in using these ghost objects is that they are much cheaper to construct
    in comparison with the full IDEA message representation.
    """
    @classmethod
    def from_record(cls, record):
        """
        Construct the IDEA ghost object from the given SQL record.
        """
        idea_raw = {}
        idea_raw['ID'] = record.id
        idea_raw['DetectTime'] = record.detecttime
        idea_raw['Category'] = list(record.category)
        idea_raw['Description'] = record.description

        for whatfrom, whereto in (('source', 'Source'), ('target', 'Target')):
            datastore = {}
            ip_list = getattr(record, '{}_ip'.format(whatfrom), '').replace('{', '').replace('}', '')
            if ip_list:
                ip_list = ip_list.split(',')
            if ip_list:
                for ipaddr in ip_list:
                    if ipaddr.find(':') != -1:
                        datastore.setdefault('IP6',[]).append(ipaddr)
                    else:
                        datastore.setdefault('IP4',[]).append(ipaddr)
            if getattr(record, '{}_type'.format(whatfrom), []):
                datastore['Type'] = list(getattr(record, '{}_type'.format(whatfrom), []))
            if getattr(record, '{}_port'.format(whatfrom), []):
                datastore['Port'] = list(getattr(record, '{}_port'.format(whatfrom), []))
            if record.protocol:
                datastore['Proto'] = list(record.protocol)
            if datastore:
                idea_raw[whereto] = [datastore]

        if record.node_name:
            for node_name in record.node_name:
                node = {}
                node['Name'] = node_name
                if record.node_type:
                    node['Type'] = list(record.node_type)
                idea_raw.setdefault('Node', []).append(node)

        if record.resolvedabuses:
            idea_raw.setdefault('_Mentat', {})['ResolvedAbuses'] = list(record.resolvedabuses)
        if record.storagetime:
            idea_raw.setdefault('_Mentat', {})['StorageTime'] = record.storagetime
        if record.eventclass:
            idea_raw.setdefault('_Mentat', {})['EventClass'] = record.eventclass
        if record.eventseverity:
            idea_raw.setdefault('_Mentat', {})['EventSeverity'] = record.eventseverity
        if record.inspectionerrors:
            idea_raw.setdefault('_Mentat', {})['InspectionErrors'] = list(record.inspectionerrors)

        try:
            return cls(idea_raw)
        except Exception:
            print("Record:")
            pprint.pprint(record)
            print("IDEA raw:")
            pprint.pprint(idea_raw)
            raise


class IDEAFilterCompiler(pynspect.compilers.IDEAFilterCompiler):
    """
    Custom filter compiler tailored for extended schema of :py:class:`mentat.idea.internal.Idea`
    messages. The implementation is based on :py:class:`pynspect.compilers.IDEAFilterCompiler`
    and it simply adds additional compilation directives for the extended IDEA
    schema. When working with :py:class:`mentat.idea.internal.Idea` messages this
    compiler should be used for proper rule compilations.
    """
    def __init__(self):
        super(IDEAFilterCompiler, self).__init__()

        self.register_variable_compilation(
            '_Mentat.StorageTime',
            pynspect.compilers.compile_timeoper,
            pynspect.rules.ListRule
        )

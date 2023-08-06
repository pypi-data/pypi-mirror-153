#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Implementation of internal **PassiveDNS** service connector.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import copy
import requests

from mentat.const import CKEY_CORE_SERVICES, CKEY_CORE_SERVICES_PDNS


_MANAGER = None


class PDNSRConfigException(ValueError):
    pass

class PDNSRRuntimeException(RuntimeError):
    pass


class PDNSRService:
    """
    Implementation of internal **PassiveDNS** access service.
    """

    def __init__(self, base_url, base_api_url, api_key):
        """
        Initialize geolocation service with paths to desired database files.
        """
        self.base_url     = base_url
        self.base_api_url = base_api_url
        self.api_key      = api_key

        # Check presence and validity of config.
        if not self.base_url:
            raise PDNSRConfigException(
                "PassiveDNS service is used but base URL is not configured"
            )
        if not (self.base_url.startswith("https://") or self.base_url.startswith("http://")):
            raise PDNSRConfigException(
                "Invalid PassiveDNS service base URL"
            )
        if not self.base_api_url:
            raise PDNSRConfigException(
                "PassiveDNS service is used but base API URL is not configured"
            )
        if not (self.base_api_url.startswith("https://") or self.base_api_url.startswith("http://")):
            raise PDNSRConfigException(
                "Invalid PassiveDNS service base API URL"
            )
        if not self.api_key:
            raise PDNSRConfigException(
                "PassiveDNS service is used but api_key is not configured"
            )

        # Ensure both base_url and base_api_url end with slash.
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        if not self.base_api_url.endswith("/"):
            self.base_api_url += "/"

    def setup(self):
        """
        Additional internal setup currently not necessary.
        """
        pass

    def status(self):
        """
        Display status of the service.
        """
        return {
            'base_url': self.base_url,
            'base_api_url': self.base_api_url,
        }

    def get_url_lookup_ip(self, ipaddr):
        """
        Get URL for looking up given IP address in PassiveDNS service.
        """
        return "{}?query={}&type=ip&since=&until=".format(
            self.base_url,
            str(ipaddr)
        )

    def get_api_url_lookup_ip(self, ipaddr):
        """
        Get API URL for looking up given IP address in PassiveDNS service.
        """
        return "{}ip/{}?token={}".format(
            self.base_api_url,
            str(ipaddr),
            self.api_key
        )

    def lookup_ip(self, ipaddr, sortby = None, limit = None):
        """
        Lookup given IP address in PassiveDNS service.
        """
        # Prepare request to PassiveDNS API
        url = self.get_api_url_lookup_ip(ipaddr)

        # Send request
        try:
            resp = requests.get(url)
        except Exception:
            raise PDNSRRuntimeException(
                "Can't get data from PassiveDNS service: {}ip/{}".format(self.base_api_url, str(ipaddr))
            )

        if resp.status_code == requests.codes.not_found:
            return None
        resp.raise_for_status()

        # Parse response
        try:
            result = resp.json()
            if sortby:
                field, direction = sortby.split('.')
                reverse = True if direction == 'desc' else False
                result = sorted(result, key = lambda x: x.get(field, None), reverse = reverse)
            if limit and int(limit):
                result = result[:int(limit)]
            return result
        except Exception as exc:
            raise PDNSRRuntimeException(
                "Invalid data received from PassiveDNS service: {}".format(str(exc))
            )


class PDNSRServiceManager:
    """
    Class representing a custom PDNSRServiceManager capable of understanding and
    parsing Mentat system core configurations and enabling easy way of unified
    bootstrapping of :py:class:`mentat.services.nerd.PDNSRService` service.
    """

    def __init__(self, core_config, updates = None):
        """
        Initialize PDNSRServiceManager object with full core configuration tree structure.

        :param dict core_config: Mentat core configuration structure.
        :param dict updates: Optional configuration updates (same structure as ``core_config``).
        """
        self._pdnsrconfig = {}

        self._service = None

        self._configure_pdnsr(core_config, updates)

    def _configure_pdnsr(self, core_config, updates):
        """
        Internal sub-initialization helper: Configure database structure parameters
        and optionally merge them with additional updates.

        :param dict core_config: Mentat core configuration structure.
        :param dict updates: Optional configuration updates (same structure as ``core_config``).
        """
        self._nerdconfig = copy.deepcopy(
            core_config[CKEY_CORE_SERVICES][CKEY_CORE_SERVICES_PDNS]
        )

        if updates and CKEY_CORE_SERVICES in updates and CKEY_CORE_SERVICES_PDNS in updates[CKEY_CORE_SERVICES]:
            self._nerdconfig.update(
                updates[CKEY_CORE_SERVICES][CKEY_CORE_SERVICES_PDNS]
            )

    def service(self):
        """
        Return handle to PassiveDNS service according to internal configurations.

        :return: Reference to PassiveDNS service object.
        :rtype: mentat.services.passivednsr.PDNSRService
        """
        if not self._service:
            self._service = PDNSRService(**self._nerdconfig)
            self._service.setup()
        return self._service


#-------------------------------------------------------------------------------


def init(core_config, updates = None):
    """
    (Re-)Initialize :py:class:`PDNSRServiceManager` instance at module level and
    store the refence within module.
    """
    global _MANAGER  # pylint: disable=locally-disabled,global-statement
    _MANAGER = PDNSRServiceManager(core_config, updates)


def manager():
    """
    Obtain reference to :py:class:`NerdServiceManager` instance stored at module
    level.
    """
    global _MANAGER  # pylint: disable=locally-disabled,global-statement
    return _MANAGER


def service():
    """
    Obtain reference to :py:class:`NerdService` instance from module level manager.
    """
    return manager().service()

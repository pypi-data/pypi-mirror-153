#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2018 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#
#-------------------------------------------------------------------------------


"""
Enricher plugins performing DNS lookup of all Source/IPx addresses using
*CESNET* and *The Email Laundry (EML)* PassiveDNS service.

The implementation consists of PassiveDNS connectors and their Enricher plugins.
The connectors provide information about domains linked to a user defined IP address.
Each domain record provides at least information when the domain name in combination
with the IP address was seen for the first and the last time from the point of
a DNS sniffer.

.. note::

    To use the plugin based on The Email Laundry services you must have a private
    API key and specify it in the plugin configuration.

.. warning::

    Still a work in progress and alpha code.

"""

__author__ = "Lukáš Huták <lukas.hutak@cesnet.cz>"
__credits__ = "Václav Bartoš <bartos@cesnet.cz>, Pavel Kácha <pavel.kacha@cesnet.cz>, " \
              "Jan Mach <jan.mach@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from datetime import datetime, timedelta
import pprint
import time
import json
import math
import ipaddress
import requests

# Custom libraries
from pynspect.jpath import jpath_values, jpath_set
import mentat.plugin.enricher
import mentat.services.cache


class PassiveDNSConnectorError(RuntimeError):
    """
    Custom error of the PassiveDNSConnector
    """
    pass


class PassiveDNSConnectorBase:
    """
    The abstract base class for PassiveDNS connectors.

    The class provides common interface and basic record caching.
    """
    def __init__(self, cache=None, api_timeout=0.5, rec_validity=168):
        """
        Base connector initializer

        :param cache: Optional record cache (can be None)
        :param int api_timeout:  Query timeout (seconds)
        :param int rec_validity: Return only records X hours old
        """
        self._cache = cache
        self._cfg_api_timeout  = api_timeout
        self._cfg_rec_validity = rec_validity

    def _cache_find(self, ip_addr):
        """
        Find a record in the local cache.

        :param str ip_addr: IP address to find
        :return: If the record is present (True, list of domains) else (False, None).
          If the record is present but domains are unknown for PassiveDNS, the domains are None.
        :rtype: (bool, list of dict or None)
        """
        rec = self._cache.get(ip_addr) if self._cache is not None else None
        if not rec:
            return (False, None)

        return (True, rec['domains'])

    def _cache_add(self, ip_addr, domains):
        """
        Add/update a record in the local cache.

        :param str          ip_addr: IP address
        :param list of dict domains: Domains associated to the IP address (can be None)
        """
        if self._cache is None:
            return  # Cache is not available

        if not domains:
            # Replace empty list with None
            domains = None

        self._cache[ip_addr] = {"domains": domains}

    def _create_rec(self, name, time_first, time_last, **kwargs):
        """
        Create an internal record format

        :param str name:       Domain name
        :param int time_first: First seen timestamp (seconds since UNIX epoch)
        :param int time_last:  Last seen timestamp (seconds since UNIX epoch)
        :param kwargs:         Additional extra parameters
        :return: Internal record format
        :rtype: dict
        """
        time2str = lambda ts: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))
        ret = {
            "Name": name,
            "FirstSeenTime": time2str(time_first),
            "LastSeenTime": time2str(time_last),
        }

        if kwargs:
            ret.update(**kwargs)
        return ret

    def _query_fn(self, ip_addr, timeout):
        """
        PassiveDNS query function

        This function is intended to be implemented in subclasses. The function will
        send a request to a PassiveDNS API and return parsed records in the internal
        format or raise an exception.
        :param str ip_addr: IP address to query
        :param int timeout: Query timeout in seconds
        :return: Parsed domains as a list of internal records (can be empty)
        :rtype: list of dict
        """
        raise NotImplementedError("The function is not implemented in the subclass")

    def query(self, ip_addr, timeout=None):
        """
        Get domains of an IP address based on PassiveDNS

        First, the IP address is searched in the local cache. If the corresponding
        record is present and valid, the result is returned immediately without
        querying a PassiveDNS server. Otherwise, a new query is send to the remote server
        and results of successfully processed queries are stored into the local cache
        and returned.

        :param str ip_addr: IP address to query
        :param int timeout: Query timeout in seconds (if None, default timeout is used)
        :return: Parsed domains as a list of internal records (can be empty)
        :rtype:  list of dict
        """
        # First, check record cache
        found, domains = self._cache_find(ip_addr)
        if found:
            return [] if not domains else domains

        # Not found in the cache, create a new query and store the result
        if not timeout:
            timeout = self._cfg_api_timeout

        domains = self._query_fn(ip_addr, timeout)
        self._cache_add(ip_addr, domains)
        return domains

    def query_multi(self, ip_addrs, timeout=None):
        """
        Get domains of multiple IP addresses based on PassiveDNS

        Similar to the casual query, however, results of multiple IP addresses are returned
        as dictionary where keys are IP addresses and values are lists of parsed domains.
        IP addresses without known domain records are not present in the result.

        :param list of str ip_addrs: List of IP addresses to query
        :param int timeout:          Single query timeout in seconds (if None, default
          timeout is used)
        :return: IP addresses and their domains (can be empty)
        :rtype:  dict [str, list of dict]
        """
        domain_dict = {}
        for i in ip_addrs:
            domains = self.query(i, timeout)
            if not domains:
                continue
            domain_dict[str(i)] = domains
        return domain_dict

    def status(self):
        """
        Determine and return the status of internal cache table and configuration

        :return: Dictionary containing various subkeys
        :rtype:  dict
        """
        stats = {
            'api_timeout':  self._cfg_api_timeout,
            'rec_validity': self._cfg_rec_validity
        }

        if self._cache is not None:
            stats.update({"cached_records": len(self._cache)})
        return stats


class PassiveDNSConnectorEML(PassiveDNSConnectorBase):
    """
    PassiveDNS connector for 'The Email Laundry' PassiveDNS API

    This connector uses PassiveDNS API provided by The Email Laundry. To use this
    API you MUST define your private API Key.
    """

    # List of configuration parameters
    API_SERVER = "http://feedapi.theemaillaundry.net"
    API_URL = "/pdns/api/v0.1/ipv{ip_version}/{ip_address}?key={key}"

    def __init__(self, api_key, api_limit=100, cache_mgr=None, cache_exp=7200, **kwargs):
        """
        Connector initializer

        If a cache manager object :py:class:`mentat.services.cache.CacheServiceManager` is passed
        to the connector, the connector will cache results of queries for faster lookup of already
        queried IP addresses.

        :param str api_key:   EML API key
        :param int api_limit: Maximum number of domains per one IP address (max. 100)
        :param cache_mgr:     Cache manager (can be None)
        :param int cache_exp: Cache record timeout (seconds)
        :param kwargs: Additional parameters to override base connector parameters
            (see :class:`PassiveDNSConnectorBase`)
        """
        if not api_key:
            raise RuntimeError("EML API key is not defined!")
        cache = cache_mgr.cache("PassiveDNS_EML", cache_exp, True) if cache_mgr else None

        super().__init__(cache, **kwargs)
        self._session = requests.Session()
        self._cfg_api_key = api_key
        self._cfg_api_limit = api_limit

    def _query_url(self, ip_addr, limit=None, date=None):
        """
        Create a query URL for a new HTTP Get request

        :param str ip_addr: IP address
        :param int limit:   Limit number of records to receive
        :param str date:    Select only records that were active on a specific day (format "YYYYMMDD")
        :return: Formatted URL address
        :rtype: str
        """
        addr = ipaddress.ip_address(ip_addr)
        query_str = self.API_SERVER + self.API_URL.format(
            ip_version = addr.version,
            ip_address = str(addr),
            key        = self._cfg_api_key
        )

        if limit:
            query_str += "&limit=" + str(limit)
        if date:
            query_str += "&date=" + str(date)
        return query_str

    def _query_parse(self, json_txt):
        """
        Process a JSON response retrieved from the PassiveDNS API

        Check validity of received DNS records and extract only valid domain names.
        :param dict json_txt: Response from the PassiveDNS
        :return: Parsed information about associated domain names (can be empty)
        :rtype:  list of dict
        """
        domains = []
        time_min = int(time.time()) - (self._cfg_rec_validity * 3600)

        try:
            data = json.loads(json_txt)
            for rec in data["result"]:
                ts_last = int(rec["last_seen"])
                if ts_last < time_min:
                    # Skip old records
                    continue

                name     = str(rec["query"])
                ts_first = int(rec["first_seen"])
                ttl      = int(rec["ttl"])

                new_domain = self._create_rec(name, ts_first, ts_last, TTL=ttl)
                domains.append(new_domain)
        except json.decoder.JSONDecodeError as err:
            raise PassiveDNSConnectorError("Failed to parse JSON response: " + str(err))
        except (KeyError, TypeError, ValueError) as err:
            raise PassiveDNSConnectorError("Unexpected response structure: " + str(err))
        return domains

    def _query_fn(self, ip_addr, timeout):
        """
        PassiveDNS query function

        The function will send a request to a PassiveDNS API and return parsed
        records in the internal format or raise an exception.
        :param str ip_addr:      IP address to query
        :param int timeout: Query timeout in seconds
        :return: Parsed domains as a list of internal records (can be empty)
        :rtype: list of dict
        """
        # Prepare Request URL with parameters
        url = self._query_url(ip_addr, limit=self._cfg_api_limit)

        try:
            # Reuse the session to create a new request
            response = self._session.get(url, timeout=timeout)
            ret_code = response.status_code
        except requests.exceptions.RequestException as err:
            raise PassiveDNSConnectorError("API request failed: " + str(err))

        if ret_code == 200:    # Success
            domains = self._query_parse(response.text)
        elif ret_code == 404:  # IP address not found
            domains = []
        else:
            err_msg = "Unexpected return code '{}' from the PassiveDNS server (request '{}').".format(ret_code, url)
            raise PassiveDNSConnectorError(err_msg)

        return domains


class PassiveDNSConnectorCESNET(PassiveDNSConnectorBase):
    """
    PassiveDNS connector for 'CESNET' PassiveDNS API
    """
    # List of configuration parameters
    API_SERVER = "https://passivedns.cesnet.cz"
    API_URL = "/pdns/ip/{ip_address}?from={start}&to={end}"

    def __init__(self, api_limit=100, cache_mgr=None, cache_exp=7200, **kwargs):
        """
        Connector initializer

        If a cache manager object :py:class:`mentat.services.cache.CacheServiceManager` is passed
        to the connector, the connector will cache results of queries for faster lookup of already
        queried IP addresses.

        Due to remote API limitation the common parameter 'api_validity' (in hours) is
        rounded up to represent full days.

        :param int api_limit: Maximum number of domains per one IP address
          (if the value is None, no limit is applied)
        :param cache_mgr:     Cache manager (can be None)
        :param int cache_exp: Cache record timeout (seconds)
        :param kwargs: Additional parameters to override base connector parameters
            (see :py:class:`PassiveDNSConnectorBase`)
        """
        cache = cache_mgr.cache("PassiveDNS_CESNET", cache_exp, True) if cache_mgr else None

        super().__init__(cache, **kwargs)
        self._session = requests.Session()
        self._cfg_rec_validity = math.ceil(self._cfg_rec_validity / 24.0) * 24
        self._cfg_api_limit = api_limit

    def _query_url(self, ip_addr):
        """
        Create a query URL for a new HTTP Get request

        :param str ip_addr: IP address
        :return: Formatted URL address
        :rtype: str
        """
        addr = ipaddress.ip_address(ip_addr)

        # Determine time range
        date2str = lambda date: date.strftime("%Y-%m-%d")
        date_start = date2str(datetime.now() - timedelta(hours=self._cfg_rec_validity))
        date_end =   date2str(datetime.now() + timedelta(days=1))

        return self.API_SERVER + self.API_URL.format(
            ip_address = str(addr),
            start = date_start,
            end = date_end
        )

    def _query_parser(self, json_txt):
        """
        Process a JSON response retrieved from the PassiveDNS API

        Check validity of received DNS records and convert them into the internal format.
        :param str json_txt: Response from the PassiveDNS API
        :return: Parsed information about associated domain names (can be empty)
        :rtype:  list of dict
        """
        # Domain main sanitizer removes the last doc if present
        name_sanitizer = lambda name: name[:-1] if name[-1] == '.' else name
        # Timestamp parser converts date to number of seconds from Unix Epoch
        ts_parser = lambda ts: time.mktime(datetime.strptime(ts, "%Y-%m-%d").timetuple())

        domains = []
        try:
            data = json.loads(json_txt)
            for rec in data:
                name     = name_sanitizer(str(rec["domain"]))
                ts_first = int(ts_parser(str(rec["time_first"])))
                ts_last  = int(ts_parser(str(rec["time_last"])))
                rec_type = str(rec["type"]).upper()

                new_domain = self._create_rec(name, ts_first, ts_last, Type=rec_type)
                domains.append(new_domain)
        except json.decoder.JSONDecodeError as err:
            raise PassiveDNSConnectorError("Failed to parse JSON response: " + str(err))
        except (KeyError, TypeError, ValueError) as err:
            raise PassiveDNSConnectorError("Unexpected response structure: " + str(err))

        limit = self._cfg_api_limit
        if limit is not None and limit < len(domains):
            # Sort from the newest to the older and remove exceeding records
            cmp_fn = lambda rec: time.mktime(time.strptime(rec["LastSeenTime"], "%Y-%m-%dT%H:%M:%SZ"))
            domains.sort(key=cmp_fn)
            domains = domains[-self._cfg_api_limit:]

        return domains

    def _query_fn(self, ip_addr, timeout):
        """
        PassiveDNS query function

        The function will send a request to a PassiveDNS API and return parsed
        records in the internal format or raise an exception.
        :param str ip_addr:      IP address to query
        :param int timeout: Query timeout in seconds
        :return: Parsed domains as a list of internal records (can be empty)
        :rtype: list of dict
        """
        url = self._query_url(ip_addr)

        try:
            response = self._session.get(url, timeout=timeout)
            ret_code = response.status_code
        except requests.exceptions.RequestException as err:
            raise PassiveDNSConnectorError("API request failed: " + str(err))

        if ret_code == 200:    # Success
            domains = self._query_parser(response.text)
        elif ret_code == 404:  # IP address not found
            domains = []
        else:
            err_msg = "Unexpected return code '{}' from the PassiveDNS server (request '{}').".format(ret_code, url)
            raise PassiveDNSConnectorError(err_msg)
        return domains

# -------------------------------------------------------------------------------------

def _format_results(source_id, pairs):
    """
    Prepare a formatted result for an IDEA messsage.

    The function wraps each item in a new dictionary with identification of
    the type of IDEA enrichment block (key, type, reference, etc).
    :param str source_id: Identification string of the API provider
    :param dict [str, list of dict] pairs: IP address and their domains
    :return: Formatter result
    :rtype: list of dict
    """
    res = []
    for ip_addr, domains in pairs.items():
        res.append({
            "Key": str(ip_addr),
            "Type": ["PassiveDNS"],
            "Ref": str(source_id),
            "DNS": domains
        })
    return res

class PassiveDNSCESNETEnricherPlugin(mentat.plugin.enricher.EnricherPlugin):
    """
    Enricher plugin performing PassiveDNS lookup of all Source/IPx addresses using
    *CESNET* PassiveDNS service.
    """
    SOURCE_ID = "https://passivedns.cesnet.cz/"

    def __init__(self):
        """
        Initializer of the plugin
        """
        self.connector = None

    def setup(self, daemon, config_updates = None):
        """
        Process configuration parameters and prepare PassiveDNS connector
        """
        # Prepare a cache manager
        cache_mgr = mentat.services.cache.CacheServiceManager(
            daemon.config,
            config_updates
        )

        # Initialized connector
        self.connector = PassiveDNSConnectorCESNET(cache_mgr=cache_mgr, **config_updates)
        daemon.logger.info("Initialized '{}' enricher plugin: {}".format(
            self.__class__.__name__,
            pprint.pformat(self.connector.status())
        ))

    def process(self, daemon, message_id, message):
        """
        Process and enrich given message.
        """
        daemon.logger.debug("PassiveDNSCESNET - message '{}'".format(message_id))

        sources = []
        sources += jpath_values(message, 'Source.IP4')
        sources += jpath_values(message, 'Source.IP6')

        # Process only global IP addresses
        sources = [x for x in sources if ipaddress.ip_address(x).is_global]

        # Start PasssiveDNS lookup
        try:
            pairs = self.connector.query_multi(sources)
        except PassiveDNSConnectorError as err:
            daemon.logger.warn("PassiveDNSCESNET lookup failed: " + str(err))
            return (daemon.FLAG_CONTINUE, self.FLAG_UNCHANGED)

        # Store results
        changed = False
        enrichments = _format_results(self.SOURCE_ID, pairs)

        if enrichments:
            data = jpath_values(message, "Enrich")
            data.extend(enrichments)
            jpath_set(message, "Enrich", data)
            daemon.logger.debug("Enriched message '{}' with attribute 'Enriched'".format(message_id))
            changed = True

        return (daemon.FLAG_CONTINUE, changed)


class PassiveDNSEMLEnricherPlugin(mentat.plugin.enricher.EnricherPlugin):
    """
    Enricher plugin performing PassiveDNS lookup of all Source/IPx addresses using
    *The Email Laundry* (EML) service.
    """
    SOURCE_ID = "http://feedapi.theemaillaundry.net/"

    def __init__(self):
        """
        Initializer of the plugin
        """
        self.connector = None
        self.cache = None

    def setup(self, daemon, config_updates = None):
        """
        Process configuration parameters and prepare PassiveDNS connector
        """
        # Make sure that the API key is defined
        key = config_updates.get("api_key") if config_updates is not None else None
        if not key:
            raise RuntimeError("PassiveDNS API key is not defined!")

        # Prepare a cache manager
        cache_mgr = mentat.services.cache.CacheServiceManager(
            daemon.config,
            config_updates
        )

        # Initialized connector
        self.connector = PassiveDNSConnectorEML(cache_mgr=cache_mgr, **config_updates)
        daemon.logger.info("Initialized '{}' enricher plugin: {}".format(
            self.__class__.__name__,
            pprint.pformat(self.connector.status())
        ))

    def process(self, daemon, message_id, message):
        """
        Process and enrich given message.
        """
        daemon.logger.debug("PassiveDNSEML - message '{}'".format(message_id))

        sources = []
        sources += jpath_values(message, 'Source.IP4')
        # IPv6 addresses are not supported by API yet
        # sources += jpath_values(message, 'Source.IP6')

        # Process only global IP addresses
        sources = [x for x in sources if ipaddress.ip_address(x).is_global]

        # Start PasssiveDNS lookup
        try:
            pairs = self.connector.query_multi(sources)
        except PassiveDNSConnectorError as err:
            daemon.logger.warn("PassiveDNSEML lookup failed: " + str(err))
            return (daemon.FLAG_CONTINUE, self.FLAG_UNCHANGED)

        # Store results
        changed = False
        enrichments = _format_results(self.SOURCE_ID, pairs)

        if enrichments:
            data = jpath_values(message, "Enrich")
            data.extend(enrichments)
            jpath_set(message, "Enrich", data)
            daemon.logger.debug("Enriched message '{}' with attribute 'Enriched'".format(message_id))
            changed = True

        return (daemon.FLAG_CONTINUE, changed)

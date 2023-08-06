#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2018 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#
#-------------------------------------------------------------------------------

__author__ = "Lukáš Huták <lukas.hutak@cesnet.cz>"
__credits__ = "Václav Bartoš <bartos@cesnet.cz>, Pavel Kácha <pavel.kacha@cesnet.cz>, " \
              "Jan Mach <jan.mach@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

"""
Simple cache module based on BerkeleyDB

The module represents a dictionary with automatic record expiration. The cache can be
shared across multiple independent processes at time. Any object that can be serialized
using :py:mod:`pickle` can be used as a dictionary key or value.

Cache purge (i.e. removing expired record) is executed automatically in specified intervals
so users don't have to call purge operation manually. However, if the operation is required
at specific time the users still can call it directly.

Prerequisites
^^^^^^^^^^^^^

The module depends on libdb library (available through a system package manager)
and its python wrapper `bsddb3 <https://www.jcea.es/programacion/pybsddb.htm>`__
(available through the system package manager or `PyPI <https://pypi.org/project/bsddb3/>`__)

.. warning:

    The cache module is NOT thread-safe.

.. warning:

    Cache module can be used by multiple independent processes at time, therefore, in case of
    underlying database corruption a cache recovery function is NOT supported. Automatic
    re-initialization (i.e. cache destruction and initialization) is also NOT possible since
    any other processes can still using it. In such case, user interaction (i.e. stopping
    processes and removing cache files) is necessary!

"""

import pickle
import time
import os
import copy

from bsddb3 import db
from mentat.const import CKEY_CORE_SERVICES, CKEY_CORE_SERVICES_CACHE

class CacheServiceError(BaseException):
    """
    Custom cache exception
    """
    pass


class CacheService(object):
    """
    Imlementation of the cache dictionary
    """
    # Common class parameters
    GLOB_DB_NAME = "global.db"

    def __init__(self, path, name, timeout=None, to_force=False, bsize=2**24, purge_int=15):
        """
        Initialize a new cache or load an existing cache

        If a record timeout is not specified (i.e. None), the timeout is obtained from the cache
        configuration. However, if the cache hasn't been created before, the timeout is undefined!
        On the other hand, if the timeout is specified by a user but it doesn't match the cache
        configuration, an exception is raised too!

        Buffer size of the Berkeley database (originally called cache size) represent shared memory
        buffer pool. If it is set too small, your's application performance will suffer from too
        much disk I/O.

        :param str path:          Directory where the caches are stored
        :param str name:          Name of the cache to create/load
        :param int timeout:       Default record timeout (seconds) or None
        :param bool to_force:     Overwrite current timeout, if defined
        :param int or None bsize: Buffer size of Berkeley database (in bytes, must be in powers of
            two). If the value is None or the cache already exists, the parameter is ignored!
        :param int purge_int:     Number of seconds between automatic cache purge
        """
        if not isinstance(name, str) or not isinstance(path, str):
            raise TypeError("Directory and name of the cache must be string!")
        if ".." in name:
            raise ValueError("Name of the cache must not contain '..'!")
        if bsize is not None and not (bsize > 0 and ((bsize & (bsize - 1)) == 0)):
            raise ValueError("Buffer size must be in powers of two!")
        if purge_int <= 0:
            raise ValueError("Purge interval must be greater that zero!")

        # Create a database directory if not exists
        cache_path = path + "/" + name
        os.makedirs(cache_path, exist_ok=True)

        msg_recovery = "Cache DB '{0}' in '{1}' is corrupted. Destroy it manually or run recovery."
        msg_other = "Initialization of cache DB '{0}' failed: {1}"

        # Configure cache timeout (the same value shared across all instances)
        try:
            self._timeout = self._setup_timeout(path, name, timeout, to_force)
        except db.DBRunRecoveryError:
            raise CacheServiceError(msg_recovery.format(self.GLOB_DB_NAME, path))
        except db.DBError as err:
            raise CacheServiceError(msg_other.format(self.GLOB_DB_NAME, str(err)))

        # Create/connect to the DB
        try:
            self._setup_db(cache_path, bsize)
        except db.DBRunRecoveryError:
            raise CacheServiceError(msg_recovery.format(name, cache_path))
        except db.DBError as err:
            raise CacheServiceError(msg_other.format(name, str(err)))

        # Remove expired records, if exists
        self._purge_int = purge_int
        self._purge_time = None
        self.purge()

    def _setup_timeout(self, path, name, timeout, force=False):
        """
        Check if all caches with the same identifier use the same record timeout

        First, the function connects to a global database environment with databases shared across
        all caches. If the environment or the databases doesn't exist, new ones are created.
        Finally, try to compare a timeout of the current cache with the user defined value using one
        of the shared databases. If the user specified value is None, the function just adopts the
        timeout of the current cache.

        :raises CacheServiceError: If the current cache timeout is already defined but it doesn't
            match user specified value, which is not None.
        :raises CacheServiceError: If the current cache timeout is not specified and the user
            specifiedvalue is None. In other worlds, a cache maintainer haven't created the cache
            yet.

        :param str path:     Path to the directory with shared databases
        :param str name:     Cache identification
        :param int timeout:  Timeout in seconds or None, if unknown
        :param bool force:   Overwrite current timeout, if already defined
        :return: Cache record timeout
        :rtype: int
        """
        if timeout is not None and not isinstance(timeout, int):
            raise CacheServiceError("Timeout must be an integer or None!")
        if isinstance(timeout, int) and timeout <= 0:
            raise CacheServiceError("Timeout must be greater than zero!")

        # Connect to the internal database with timeouts
        env_flags = db.DB_CREATE | db.DB_INIT_MPOOL | db.DB_INIT_CDB
        env = db.DBEnv()
        env.open(path, env_flags)
        timeouts_db = db.DB(env)
        timeouts_db.open(
            self.GLOB_DB_NAME,
            dbname="timeouts",
            dbtype=db.DB_HASH,
            flags=db.DB_CREATE
        )

        # Get the current value
        key = pickle.dumps(name)
        value_now = timeouts_db.get(key, default=None)
        if value_now is not None:
            value_now = int(pickle.loads(value_now))

        if timeout is None:
            # User didn't define timeout -> just return the current value
            if value_now is None:
                raise CacheServiceError("Timeout configuration of the cache '{0}' is not "
                    "available!".format(name))
            return value_now

        if value_now is None or force:
            # Cache timeout is not specified or timeout overwrite is enabled
            timeouts_db.put(key, pickle.dumps(timeout))
            return timeout

        if value_now != timeout:
            # Timeout values mismatch
            raise CacheServiceError("Record timeout ({0} s) of the cache '{1}' doesn't match "
                "previously defined value ({2} s)!".format(timeout, name, value_now))

        return timeout

    def _setup_db(self, path, bsize=None):
        """
        Initialize a database environment and connect to a cache database

        If the database environment doesn't exists, a new one is created. The same applies to all
        cache databases. The environment consists of 2 databases, cache data itself and timestamps.
        The timestamp database, where keys are timestamps, represents a database index of the cache
        data database. Keep on mind that the timestamp database could contain duplicates of the
        same key!

        :param str path:          Path to the database environment
        :param int or None bsize: Buffer size of Berkeley DB (if None, do not modify)
        :return: None
        """
        # Initialize DB environment and main databases
        env_flags = db.DB_CREATE | db.DB_INIT_MPOOL | db.DB_INIT_CDB
        db_flags = db.DB_CREATE
        db_filename = self.__class__.__name__ + ".db"

        self._cache_env = db.DBEnv()
        if bsize is not None:
            self._cache_env.set_cachesize(0, bsize, 0)
        self._cache_env.open(path, env_flags)

        self._cache_data = db.DB(self._cache_env)
        self._cache_data.open(
            db_filename,
            dbname="data",
            dbtype=db.DB_HASH,
            flags=db_flags
        )

        # Create "secondary" DB with timestamps
        self._cache_ts = db.DB(self._cache_env)
        self._cache_ts.set_flags(db.DB_DUPSORT)  # Support sorted duplicates
        self._cache_ts.open(
            db_filename,
            dbname="timestamps",
            dbtype=db.DB_HASH,
            flags=db_flags
        )
        self._cache_data.associate(self._cache_ts, self._key_gen)

    def _key_gen(self, pri_key, pri_data):
        """
        Callback function for creating a secondary database key

        The function takes a key and value of the primary database and returns timestamp of
        the record.

        :param bytes pri_key:  Primary record key
        :param bytes pri_data: Primary record value
        :return: Pickled timestamp
        :rtype: bytes
        """
        ts = pickle.loads(pri_data)[0]
        return pickle.dumps(ts)

    def _auto_purge(self):
        """
        Automatically remove expired records

        The function runs cache purge if the time since last purge has exceeded a specified
        interval.
        :return: None
        """
        if self._purge_time + self._purge_int > time.time():
            return
        self.purge()

    def purge(self):
        """
        Remove expired records from the cache

        First, the function prepare a set of timestamps to remove and then it will remove them.
        This prevents the process to hold a write cursor for long time and block other processes
        during cache purge.
        :return: None
        """
        key2del = set()
        time_now = int(time.time())

        cursor = self._cache_ts.cursor()
        while cursor.next_nodup() is not None:
            k, _ = cursor.current()
            rec_time = pickle.loads(k)
            if int(rec_time) >= time_now:
                continue
            key2del.add(k)
        cursor.close()

        # Remove them
        for key in key2del:
            try:
                self._cache_ts.delete(key)
            except KeyError:  # Someone already managed to remove the key
                pass

        # Update the last purge time
        self._purge_time = time.time()

    def clear(self):
        """
        Empty a database

        :return: None
        """
        self._cache_data.truncate()

    def set(self, key, value, timeout=None):
        """
        Store a key/value pair to the cache

        If the key already exists in the cache, the previous value is replaced.
        The key and value must be pickable objects.

        :param key:   The key to be used
        :param value: The value to be stored
        :param int timeout: Override default timeout value (seconds)
        :return: None
        """
        # (Optional) cache purge
        self._auto_purge()

        # Define expiration timeout
        if timeout is None:
            timeout = self._timeout
        if int(timeout) <= 0:
            raise CacheServiceError("Record timeout is not valid!")
        time_exp = int(time.time() + timeout)

        # Store the record
        key_data = pickle.dumps(key)
        value_data = pickle.dumps((time_exp, value))
        self._cache_data.put(key_data, value_data)

    def get(self, key, default=None):
        """
        Get a value stored in the cache for a given key

        If the record has expired, the default value is returned.
        :param key: The key to be search in the cache
        :param default: Value to return if the record is not present.
        :return: The value or default
        """
        # (Optional) cache purge
        self._auto_purge()

        # Try to find the record
        key_data = pickle.dumps(key)
        value_data = self._cache_data.get(key_data, default=default)
        if value_data == default:
            return default

        # Check timeout
        value = pickle.loads(value_data)
        time_now = time.time()
        if value[0] < time_now:  # Record has expired
            return default

        return value[1]

    def _dump(self, index=False):
        """
        Dump content of the cache on standard output (for development purpose only)

        :param bool index: Also print the index DB with timestamps (i.e. secondary DB)
        :return: None
        """
        rec_cnt = 0
        print("Cache dump:")
        cursor = self._cache_data.cursor()
        while cursor.next() is not None:
            k, v = cursor.current()
            key = pickle.loads(k)
            ts, value = pickle.loads(v)
            print("- Key '{}', exp.ts: '{}', value: {}".format(key, ts, repr(value)))
            rec_cnt += 1
        cursor.close()
        print("  (total record count: {})".format(rec_cnt))

        if not index:
            return None

        rec_cnt = 0
        print("Secondary DB:")
        cursor = self._cache_ts.cursor()
        while cursor.next() is not None:
            k, v = cursor.current()
            key = pickle.loads(k)
            _, value = pickle.loads(v)
            print("- Key '{}', value: {}".format(key, repr(value)))
            rec_cnt += 1
        cursor.close()
        print("  (total record count: {})".format(rec_cnt))

    def __getitem__(self, item):
        """
        Get a value stored in the cache for a given key

        :raises KeyError: If the key doesn't exist or the record is not valid anymore.
        :param item: The key to be search in the cache
        :return: Value
        """
        data = self.get(item)
        if data is None:
            raise KeyError(item)
        return data

    def __setitem__(self, key, value):
        """
        Store a key/value pair to the cache

        If the key already exists in the cache, the previous value is replaced. The key and value
        must be pickable objects.

        :param key:   The key to be used
        :param value: The value to be stored
        :return: None
        """
        self.set(key, value)

    def __delitem__(self, key):
        """
        Delete a specific key from the cache

        :raises KeyError: If the key doesn't exist in the cache. Keep on mind that the cache could
            be simultaneously used by multiple processes.
        :param key: Key
        :return: None
        """
        key_data = pickle.dumps(key)
        self._cache_data.delete(key_data)

    def __len__(self):
        """
        Return number of records in the cache

        :return: Number of records
        :rtype: int
        """
        return len(self._cache_data)


class CacheServiceManager(object):
    """
    Class representing a custom CacheManager capable of understanding and parsing Mentat system
    core configuration and enabling easy bootstrapping
    of :py:class:`mentat.services.cache.CacheService`.
    """
    def __init__(self, core_config, updates=None):
        """
        Initialize CacheServiceManager object with full core configuration tree structure

        :param dict core_config: Mentat core configuration structure
        :param dict updates:     Optional configuration updates (same structure as ``core_config``)
        """
        self._cache_config = {}
        self._configure_cache(core_config, updates)

    def _configure_cache(self, core_config, updates):
        """
        Internal sub-initialization helper: Configure cache structure parameters and optionally
        merge them with additional updates.

        :param dict core_config: Mentat core configuration structure
        :param dict updates:     Optional configuration updates (same structure as ``core_config``)
        """
        self._cache_config = copy.deepcopy(core_config[CKEY_CORE_SERVICES][CKEY_CORE_SERVICES_CACHE])

        if updates and CKEY_CORE_SERVICES in updates and CKEY_CORE_SERVICES_CACHE in updates[CKEY_CORE_SERVICES]:
            self._cache_config.update(
                updates[CKEY_CORE_SERVICES][CKEY_CORE_SERVICES_CACHE]
            )

    def cache(self, name, timeout=None, to_force=False):
        """
        Return handle to a cache according to internal configuration and user defined parameters

        For a detailed description of parameters, see :py:class:`mentat.services.cache.CacheService`  .
        :param str name:      Name of the cache to create/load
        :param int timeout:   Default record timeout (seconds) or None
        :param bool to_force: Overwrite current timeout, if defined
        :return: Reference to the cache object
        :rtype: mentat.services.cache.CacheService
        """
        return CacheService(name=name, timeout=timeout, to_force=to_force, **self._cache_config)

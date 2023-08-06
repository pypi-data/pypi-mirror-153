#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Library for calculating various statistics from given list of IDEA messages.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import math
import datetime
import bisect

from pynspect.jpath import jpath_value, jpath_values
from mentat.reports.utils import SimpleMemoryThresholdingCache, SingleSourceThresholdingCache
from mentat.const import REPORT_TYPE_SUMMARY


KEY_UNKNOWN = '__unknown__'
KEY_NONE    = '__none__'

#
# Literal constants for keywords of statistical categories.
#
ST_INTERNAL = 'stats_internal'
ST_EXTERNAL = 'stats_external'
ST_OVERALL  = 'stats_overall'

#
# Literal constants for keywords of calculated statistics.
#
ST_SKEY_IPS         = 'ips'
ST_SKEY_IP4S        = 'ip4s'
ST_SKEY_IP6S        = 'ip6s'
ST_SKEY_ANALYZERS   = 'analyzers'
ST_SKEY_CATEGORIES  = 'categories'
ST_SKEY_CATEGSETS   = 'category_sets'
ST_SKEY_DETECTORS   = 'detectors'
ST_SKEY_DETECTORSWS = 'detectorsws'
ST_SKEY_DETECTORTPS = 'detector_types'
ST_SKEY_ABUSES      = 'abuses'
ST_SKEY_EMAILS      = 'emails'
ST_SKEY_ASNS        = 'asns'
ST_SKEY_COUNTRIES   = 'countries'
ST_SKEY_CLASSES     = 'classes'
ST_SKEY_SEVERITIES  = 'severities'
ST_SKEY_PORTS       = 'ports'
ST_SKEY_SRCPORTS    = 'source_ports'
ST_SKEY_TGTPORTS    = 'target_ports'
ST_SKEY_SRCTYPES    = 'source_types'
ST_SKEY_TGTTYPES    = 'target_types'
ST_SKEY_PROTOCOLS   = 'protocols'
ST_SKEY_LIST_IDS    = 'list_ids'
ST_SKEY_CNT_ALERTS  = 'cnt_alerts'
ST_SKEY_CNT_EVENTS  = 'cnt_events'
ST_SKEY_CNT_EVTS_A  = 'cnt_events_all'
ST_SKEY_CNT_EVTS_F  = 'cnt_events_filtered'
ST_SKEY_CNT_EVTS_T  = 'cnt_events_thresholded'
ST_SKEY_CNT_EVTS_N  = 'cnt_events_new'
ST_SKEY_CNT_EVTS_R  = 'cnt_events_relapsed'
ST_SKEY_CNT_RECURR  = 'cnt_recurring'
ST_SKEY_CNT_UNIQUE  = 'cnt_unique'
ST_SKEY_CNT_REPORTS = 'cnt_reports'
ST_SKEY_CNT_EMAILS  = 'cnt_emails'
ST_SKEY_CNT_REPS_S  = 'cnt_reports_summary'
ST_SKEY_CNT_REPS_E  = 'cnt_reports_extra'
ST_SKEY_COUNT       = 'count'
ST_SKEY_DT_FROM     = 'dt_from'
ST_SKEY_DT_TO       = 'dt_to'
ST_SKEY_TIMELINE    = 'timeline'
ST_SKEY_TLCFG       = 'timeline_cfg'
ST_SKEY_TIMESCATTER = 'timescatter'
ST_SKEY_REST        = '__REST__'

LIST_STAT_GROUPS = (
    ST_INTERNAL,
    ST_EXTERNAL,
    ST_OVERALL,
)
"""List of statistical groups. The statistics will be calculated separatelly for these."""

LIST_AGGREGATIONS = (
    [ST_SKEY_IPS,        ('Source.IP4', 'Source.IP6'),                                   KEY_UNKNOWN],
    #[ST_SKEY_IP4S,      ('Source.IP4',),                                                KEY_UNKNOWN],
    #[ST_SKEY_IP6S,      ('Source.IP6',),                                                KEY_UNKNOWN],
    [ST_SKEY_ANALYZERS,  ('Node[#].SW',),                                                KEY_UNKNOWN],
    [ST_SKEY_CATEGORIES, ('Category',),                                                  KEY_UNKNOWN],
    [ST_SKEY_DETECTORS,  ('Node[#].Name',),                                              KEY_UNKNOWN],
    [ST_SKEY_ABUSES,     ('_Mentat.ResolvedAbuses', '_CESNET.ResolvedAbuses'),           KEY_UNKNOWN],
    [ST_SKEY_ASNS,       ('_Mentat.SourceResolvedASN', '_CESNET.SourceResolvedASN'),     KEY_UNKNOWN],
    [ST_SKEY_COUNTRIES,  ('_Mentat.SourceResolvedCountry', '_CESNET.SourceResolvedASN'), KEY_UNKNOWN],
    [ST_SKEY_CLASSES,    ('_Mentat.EventClass', '_CESNET.SourceResolvedASN'),            KEY_UNKNOWN],
    [ST_SKEY_SEVERITIES, ('_Mentat.EventSeverity', '_CESNET.SourceResolvedASN'),         KEY_UNKNOWN]
)
"""List of statistical aggregations."""

LIST_SKIP_SINGLEHOST = (
    ST_SKEY_IPS,
    ST_SKEY_ABUSES,
    ST_SKEY_ASNS,
    ST_SKEY_COUNTRIES
)

TRUNCATION_WHITELIST = {
    ST_SKEY_ANALYZERS:   True,
    ST_SKEY_CATEGORIES:  True,
    ST_SKEY_CATEGSETS:   True,
    ST_SKEY_DETECTORS:   True,
    ST_SKEY_DETECTORSWS: True,
    ST_SKEY_DETECTORTPS: True,
    ST_SKEY_SRCTYPES:    True,
    ST_SKEY_TGTTYPES:    True,
    ST_SKEY_PROTOCOLS:   True,
    ST_SKEY_ABUSES:      True,
    ST_SKEY_COUNTRIES:   True,
    ST_SKEY_CLASSES:     True,
    ST_SKEY_SEVERITIES:  True,
}
"""Whitelist for truncating statistics."""

TRUNCATION_THRESHOLD = 100
"""Threshold for truncated statistics."""

TRUNCATION_WHITELIST_THRESHOLD = 1000
"""Threshold for whitelisted truncated statistics."""

LIST_CALCSTAT_KEYS = tuple(
    [x[0] for x in LIST_AGGREGATIONS] + [
        ST_SKEY_CATEGSETS,
        ST_SKEY_DETECTORSWS,
        ST_SKEY_DETECTORTPS,
        ST_SKEY_SRCTYPES,
        ST_SKEY_TGTTYPES,
        ST_SKEY_SRCPORTS,
        ST_SKEY_TGTPORTS,
        ST_SKEY_PROTOCOLS
    ]
)
"""List of subkey names of all calculated statistics."""


LIST_OPTIMAL_STEPS = (
    1,         2,         3,         4,         5,         6,         10,         12,         15,        20,    30,     # seconds
    1*60,      2*60,      3*60,      4*60,      5*60,      6*60,      10*60,      12*60,      15*60,     20*60, 30*60,  # minutes
    1*3600,    2*3600,    3*3600,    4*3600,    6*3600,    8*3600,    12*3600,                                          # hours
    1*24*3600, 2*24*3600, 3*24*3600, 4*24*3600, 5*24*3600, 6*24*3600,  7*24*3600, 10*24*3600, 14*24*3600                # days
)
"""List of optimal timeline steps. This list is populated with values, that round nicelly in time calculations."""


#-------------------------------------------------------------------------------


def truncate_stats(stats, top_threshold = TRUNCATION_THRESHOLD, force = False):
    """
    Make statistics more brief. For each of the statistical aggregation subkeys
    generate toplist containing given number of items at most.

    :param dict stats: Structure containing statistics.
    :param int top_threshold: Toplist threshold size.
    :param bool force: Force the toplist threshold even to whitelisted keys.
    :return: Updated structure containing statistics.
    :rtype: dict
    """
    # If present, remove the list of event identifiers. This list can possibly
    # contain thousands of items or even more.
    if ST_SKEY_LIST_IDS in stats:
        del stats[ST_SKEY_LIST_IDS]

    # Create toplists for all statistical aggregation subkeys.
    if stats.get(ST_SKEY_CNT_ALERTS, 0) > 0 or stats.get(ST_SKEY_CNT_EVENTS, 0) > 0:
        for key in LIST_CALCSTAT_KEYS:
            if key in stats:
                stats = _make_toplist(stats, key, top_threshold, force)

    return stats


def truncate_stats_with_mask(stats, mask, top_threshold = TRUNCATION_THRESHOLD, force = False):
    """
    Make statistics more brief. For each of the statistical aggregation subkeys
    generate toplist containing at most given number of items, but in this case
    use given precalculated mask to decide which items should be hidden. The use
    case for this method is during calculation of timeline statistics. In that
    case the global toplists must be given to mask out the items in every time
    interval, otherwise every time interval might have different item toplist and
    it would not be possible to draw such a chart.

    :param dict stats: Structure containing single statistic category.
    :param dict mask: Global truncated statistics to serve as a mask.
    :param int top_threshold: Toplist threshold size.
    :param bool force: Force the toplist threshold even to whitelisted keys.
    :return: Updated structure containing statistics.
    :rtype: dict
    """
    # If present, remove the list of event identifiers. This list can possibly
    # contain thousands of items or even more.
    if ST_SKEY_LIST_IDS in stats:
        del stats[ST_SKEY_LIST_IDS]

    # Create masked toplists for all statistical aggregation subkeys.
    if stats.get(ST_SKEY_CNT_ALERTS, 0) > 0 or stats.get(ST_SKEY_CNT_EVENTS, 0) > 0:
        for key in LIST_CALCSTAT_KEYS:
            if key in stats:
                stats = _mask_toplist(stats, mask, key, top_threshold, force)

    return stats


def truncate_evaluations(stats, top_threshold = TRUNCATION_THRESHOLD, force = False):
    """
    Make all statistical groups more brief with :py:func:`truncate_stats`.

    :param dict stats: Structure containing statistics for all groups.
    :param int top_threshold: Toplist threshold size.
    :param bool force: Force the toplist threshold even to whitelisted keys.
    :return: Updated structure containing statistics.
    :rtype: dict
    """
    for key in LIST_STAT_GROUPS:
        if key in stats:
            stats[key] = truncate_stats(stats[key], top_threshold, force)
    return stats


#-------------------------------------------------------------------------------


def evaluate_events(events, stats = None):
    """
    Evaluate statistics for given list of IDEA events.

    :param list events: List of IDEA events to be evaluated.
    :param dict stats: Optional data structure to which to append the calculated statistics.
    :return: Structure containing calculated event statistics.
    :rtype: dict
    """
    if stats is None:
        stats = dict()

    stats.setdefault(ST_SKEY_CNT_EVENTS, 0)
    stats.setdefault(ST_SKEY_CNT_RECURR, 0)
    stats[ST_SKEY_CNT_ALERTS] = len(events)

    # Do not calculate anything for empty event list.
    if not events:
        return stats

    # Prepare structure for storing IDEA event identifiers.
    if ST_SKEY_LIST_IDS not in stats:
        stats[ST_SKEY_LIST_IDS] = []

    for event in events:
        # Remember the event ID.
        stats[ST_SKEY_LIST_IDS].append(event['ID'])

        # Include event into global statistics.
        _include_event_to_stats(stats, event)

    # Calculate secondary statistics.
    stats = _calculate_secondary_stats(stats)

    return stats


def evaluate_timeline_events(events, dt_from, dt_to, max_count, stats = None):
    """
    Evaluate statistics for given list of IDEA events and produce statistical
    record for timeline visualisations.

    :param list events: List of IDEA events to be evaluated.
    :param datetime.datetime dt_from: Lower timeline boundary.
    :param datetime.datetime dt_to: Upper timeline boundary.
    :param int max_count: Maximal number of items for generating toplists.
    :param dict stats: Data structure to which to append calculated statistics.
    :return: Structure containing evaluated event timeline statistics.
    :rtype: dict
    """
    if stats is None:
        stats = dict()

    stats.setdefault(ST_SKEY_CNT_EVENTS, 0)
    stats.setdefault(ST_SKEY_CNT_RECURR, 0)
    stats[ST_SKEY_CNT_ALERTS] = len(events)

    # Do not calculate anything for empty event list.
    if not events:
        return stats

    # Prepare structure for storing IDEA event timeline statistics.
    if ST_SKEY_TIMELINE not in stats:
        stats[ST_SKEY_TIMELINE], stats[ST_SKEY_TLCFG] = _init_timeline(dt_from, dt_to, max_count)

    # Prepare event thresholding cache for detection of recurring events.
    tcache = SimpleMemoryThresholdingCache()

    # Precalculate list of timeline keys for further bisection search.
    tl_keys = [x[0] for x in stats[ST_SKEY_TIMELINE]]

    for event in events:
        # Detect recurring events.
        recurring = tcache.event_is_thresholded(event, None, None)
        tcache.set_threshold(event, None, None, None, None)

        # Include event into global statistics.
        _include_event_to_stats(stats, event, recurring)

        # Include event into appropriate timeline window.
        event_dt = jpath_value(event, 'DetectTime')
        tl_key_idx = bisect.bisect_left(tl_keys, event_dt) - 1
        if tl_key_idx < 0:
            raise ValueError('Event does not fit into timeline with detect time {}'.format(str(event_dt)))
        _include_event_to_stats(stats[ST_SKEY_TIMELINE][tl_key_idx][1], event, recurring)

    # Calculate secondary statistics and truncate result to toplist of given size.
    stats = _calculate_secondary_stats(stats)
    stats = truncate_stats(stats)

    # Calculate secondary statistics and mask the result to toplist of given size
    # for all timeline time windows.
    for tl_stat in stats[ST_SKEY_TIMELINE]:
        tl_stat[1] = truncate_stats_with_mask(tl_stat[1], stats)

    return stats


def evaluate_singlehost_events(host, events, dt_from, dt_to, max_count, stats = None):
    """
    Evaluate statistics for given list of IDEA events and produce statistical
    record for single host visualisations.

    :param str source: Event host.
    :param list events: List of IDEA events to be evaluated.
    :param datetime.datetime dt_from: Lower timeline boundary.
    :param datetime.datetime dt_to: Upper timeline boundary.
    :param int max_count: Maximal number of items for generating toplists.
    :param dict stats: Data structure to which to append calculated statistics.
    :return: Structure containing evaluated event timeline statistics.
    :rtype: dict
    """
    if stats is None:
        stats = dict()

    stats.setdefault(ST_SKEY_CNT_EVENTS, 0)
    stats.setdefault(ST_SKEY_CNT_RECURR, 0)
    stats[ST_SKEY_CNT_ALERTS] = len(events)

    # Do not calculate anything for empty event list.
    if not events:
        return stats

    # Prepare structure for storing IDEA event timeline statistics.
    if ST_SKEY_TIMELINE not in stats:
        stats[ST_SKEY_TIMELINE], stats[ST_SKEY_TLCFG] = _init_timeline(dt_from, dt_to, max_count)

    # Prepare event thresholding cache for detection of recurring events.
    tcache = SingleSourceThresholdingCache(host)

    # Precalculate list of timeline keys for further bisection search.
    tl_keys = [x[0] for x in stats[ST_SKEY_TIMELINE]]

    for event in events:
        # Detect recurring events.
        recurring = tcache.event_is_thresholded(event, None, None)
        tcache.set_threshold(event, None, None, None, None)

        # Include event into global statistics.
        _include_event_to_stats(stats, event, recurring, LIST_SKIP_SINGLEHOST)

        # Include event into appropriate timeline window.
        event_dt = jpath_value(event, 'DetectTime')
        tl_key_idx = bisect.bisect_left(tl_keys, event_dt) - 1
        if tl_key_idx < 0:
            raise ValueError('Event does not fit into timeline with detect time {}'.format(str(event_dt)))
        _include_event_to_stats(stats[ST_SKEY_TIMELINE][tl_key_idx][1], event, recurring, LIST_SKIP_SINGLEHOST)

    # Calculate secondary statistics and truncate result to toplist of given size.
    stats = _calculate_secondary_stats(stats)
    stats = truncate_stats(stats)

    # Calculate secondary statistics and mask the result to toplist of given size
    # for all timeline time windows.
    for tl_stat in stats[ST_SKEY_TIMELINE]:
        tl_stat[1] = truncate_stats_with_mask(tl_stat[1], stats)

    return stats


def aggregate_stats_reports(report_list, dt_from, dt_to, result = None):
    """
    Aggregate multiple reporting statistical records.

    :param list report_list: List of report objects as retrieved from database.
    :param datetime.datetime dt_from: Lower timeline boundary.
    :param datetime.datetime dt_to: Upper timeline boundary.
    :param dict result: Optional data structure for storing the result.
    :return: Single aggregated statistical record.
    :rtype: dict
    """
    if result is None:
        result = dict()

    if not report_list:
        return result

    # Prepare structure for storing report timeline statistics.
    if ST_SKEY_TIMELINE not in result:
        result[ST_SKEY_TIMELINE], result[ST_SKEY_TLCFG] = _init_daily_timeline(dt_from, dt_to)

    # Prepare structure for storing report time scatter statistics.
    if ST_SKEY_TIMESCATTER not in result:
        result[ST_SKEY_TIMESCATTER] = _init_time_scatter()

    # Precalculate list of timeline keys for further bisection search.
    tl_keys = [x[0] for x in result[ST_SKEY_TIMELINE]]

    for report in report_list:
        report_ct = report.createtime

        # Include report into global statistics.
        _include_report_to_stats(result, report)

        # Include report into appropriate timeline window.
        tl_key_idx = bisect.bisect_left(tl_keys, report_ct) - 1
        if tl_key_idx < 0:
            raise ValueError('Report does not fit into timeline with create time {}'.format(str(report_ct)))
        _include_report_to_stats(result[ST_SKEY_TIMELINE][tl_key_idx][1], report)

        # Include report into appropriate time scatter window.
        _include_report_to_stats(result[ST_SKEY_TIMESCATTER][report_ct.weekday()][report_ct.hour], report)

    # Calculate secondary statistics and truncate result to toplist of given size.
    result = _calculate_secondary_stats(result)
    result = truncate_stats(result)

    # Mask the result to toplist of given size for all timeline windows.
    for tl_stat in result[ST_SKEY_TIMELINE]:
        tl_stat[1] = truncate_stats_with_mask(tl_stat[1], result)

    # Mask the result to toplist of given size for all time scatter windows.
    for ts_stat in result[ST_SKEY_TIMESCATTER]:
        ts_stat[:] = [truncate_stats_with_mask(x, result) for x in ts_stat]

    return result


def aggregate_dbstats_events(aggr_type, aggr_name, aggr_data, default_val, timeline_cfg, result = None):
    """

    """
    if result is None:
        result = dict()

    if aggr_type == 'timeline':
        bucket_dict = { bucket: idx for idx, bucket in enumerate(timeline_cfg['buckets']) }
        result.setdefault(
            ST_SKEY_TIMELINE,
            [
                [x, {}] for x in timeline_cfg['buckets']
            ]
        )

    if aggr_data:
        if aggr_type == 'aggregate':
            for res in aggr_data:
                if hasattr(res, 'set'):
                    result.setdefault(aggr_name, {})[str(res.set) or KEY_UNKNOWN] = res.count
                else:
                    result[aggr_name] = res.count

        elif aggr_type == 'timeline':
            for res in aggr_data:
                try:
                    idx = bucket_dict[res.bucket]
                    if hasattr(res, 'set'):
                        result[ST_SKEY_TIMELINE][idx][1].setdefault(aggr_name, {})[str(res.set) or KEY_UNKNOWN] = res.count
                    else:
                        result[ST_SKEY_TIMELINE][idx][1][aggr_name] = res.count
                except KeyError:
                    raise ValueError(
                        "Timeline bucket missmatch for '{}:{}:{}' [{}]".format(
                            aggr_type,
                            aggr_name,
                            res.bucket,
                            str(res.set)
                        )
                    )

    elif aggr_type == 'aggregate':
        result[aggr_name] = default_val

    return result

def postcalculate_dbstats_events(aggr_name, result):
    """

    """
    for tlbucket in result[ST_SKEY_TIMELINE]:
        if aggr_name in tlbucket[1]:
            if isinstance(tlbucket[1][aggr_name], dict):
                for key, value in tlbucket[1][aggr_name].items():
                    _counter_inc(result, aggr_name, key, value)
            else:
                _counter_inc_one(result, aggr_name, tlbucket[1][aggr_name])

def evaluate_dbstats_events(stats):
    """

    """
    stats = truncate_stats(stats)

    # Calculate secondary statistics and mask the result to toplist of given size
    # for all timeline time windows.
    for tl_stat in stats[ST_SKEY_TIMELINE]:
        tl_stat[1] = truncate_stats_with_mask(tl_stat[1], stats)

    return stats


#-------------------------------------------------------------------------------


def group_events(events):
    """
    Group events according to the presence of the ``_Mentat.ResolvedAbuses`` (or 
    ``_CESNET.ResolvedAbuses``) key.
    Each event will be added to group ``overall`` and then to either ``internal``,
    or ``external`` based on the presence of the key mentioned above.

    :param list events: List of IDEA events to be grouped.
    :return: Structure containing event groups ``stats_overall``, ``stats_internal`` and ``stats_external``.
    :rtype: dict
    """
    result = {ST_OVERALL: [], ST_INTERNAL: [], ST_EXTERNAL: []}
    for msg in events:
        result[ST_OVERALL].append(msg)
        values = jpath_values(msg, '_Mentat.ResolvedAbuses') or jpath_values(msg, '_CESNET.ResolvedAbuses')
        if values:
            result[ST_INTERNAL].append(msg)
        else:
            result[ST_EXTERNAL].append(msg)
    return result


def evaluate_event_groups(events, stats = None):
    """
    Evaluate full statistics for given list of IDEA events. Events will be
    grouped using :py:func:`group_events` first and the statistics will be
    evaluated separatelly for each of message groups ``stats_overall``,
    ``stats_internal`` and ``external``.

    :param list events: List of IDEA events to be evaluated.
    :param dict stats: Optional dictionary structure to populate with statistics.
    :return: Structure containing evaluated event statistics.
    :rtype: dict
    """
    if stats is None:
        stats = dict()
    stats[ST_SKEY_COUNT] = len(events)

    msg_groups = group_events(events)

    for grp_key in LIST_STAT_GROUPS:
        stats[grp_key] = evaluate_events(msg_groups.get(grp_key, []))
    return stats


def aggregate_stat_groups(stats_list, result = None):
    """
    Aggregate multiple full statistical records produced by the
    :py:func:`mentat.stats.idea.evaluate_event_groups` function into single statistical
    record.

    :param list stats_list: List of full statistical records to be aggregated.
    :return: Single statistical record structure.
    :rtype: dict
    """
    if result is None:
        result = dict()
    result[ST_SKEY_COUNT] = 0

    for stat in stats_list:
        result[ST_SKEY_COUNT] += stat.count

        if ST_SKEY_DT_FROM in result:
            result[ST_SKEY_DT_FROM] = min(result[ST_SKEY_DT_FROM], stat.dt_from)
        else:
            result[ST_SKEY_DT_FROM] = stat.dt_from
        if ST_SKEY_DT_TO in result:
            result[ST_SKEY_DT_TO] = max(result[ST_SKEY_DT_TO], stat.dt_to)
        else:
            result[ST_SKEY_DT_TO] = stat.dt_to

        if not stat.count:
            continue

        for grp_key in LIST_STAT_GROUPS:
            result[grp_key] = _merge_stats(
                getattr(stat, grp_key),
                result.setdefault(grp_key, {})
            )

    for grp_key in LIST_STAT_GROUPS:
        result[grp_key] = _calculate_secondary_stats(
            result.setdefault(grp_key, {})
        )

    return result


def aggregate_timeline_groups(stats_list, dt_from, dt_to, max_count, min_step = None, result = None):
    """
    Aggregate multiple full statistical records produced by the
    :py:func:`mentat.stats.idea.evaluate_event_groups` function and later retrieved
    from database as :py:class:`mentat.datatype.sqldb.EventStatisticsModel` into
    single statistical record. Given requested timeline time interval boundaries
    will be adjusted as necessary to provide best result.

    :param list stats_list: List of full statistical records to be aggregated.
    :param datetime.datetime dt_from: Lower requested timeline time interval boundary.
    :param datetime.datetime dt_to: Upper requested timeline time interval boundary.
    :param int max_count: Maximal number of steps in timeline.
    :param int min_step: Force minimal step size in timeline.
    :param dict result: Optional dictionary structure to contain the result.
    :return: Single statistical record structure.
    :rtype: dict
    """
    if result is None:
        result = dict()
    result[ST_SKEY_COUNT] = 0

    # Do not calculate anything for empty statistical list.
    if not stats_list:
        return result

    # Calculate some overall dataset statistics.
    result[ST_SKEY_COUNT]   = sum([x.count   for x in stats_list])
    result[ST_SKEY_DT_FROM] = min([x.dt_from for x in stats_list])
    result[ST_SKEY_DT_TO]   = max([x.dt_to   for x in stats_list])

    if not result[ST_SKEY_COUNT]:
        return result

    # Process each statistical group separatelly.
    for grp_key in LIST_STAT_GROUPS:
        tmpres = result.setdefault(grp_key, {})

        # Prepare data structure for storing timeline statistics.
        if ST_SKEY_TIMELINE not in result:
            tmpres[ST_SKEY_TIMELINE], result[ST_SKEY_TLCFG] = _init_timeline(
                dt_from,
                dt_to,
                max_count,
                min_step
            )

        # Precalculate list of timeline keys for subsequent bisection search.
        tl_keys = [x[0] for x in tmpres[ST_SKEY_TIMELINE]]

        for stat in stats_list:
            # Merge this statistical record with overall result.
            _merge_stats(
                getattr(stat, grp_key),
                tmpres
            )

            # Merge this statistical record into appropriate timeline window.
            stat_dt = stat.dt_from
            tl_key_idx = bisect.bisect_right(tl_keys, stat_dt) - 1
            if tl_key_idx < 0:
                raise ValueError(
                    'Statistical record with start time {} does not fit into timeline with start time {} ({})'.format(
                        str(tl_keys[0]),
                        str(stat_dt),
                        tl_key_idx
                    )
                )
            _merge_stats(
                getattr(stat, grp_key),
                tmpres[ST_SKEY_TIMELINE][tl_key_idx][1]
            )

        # Calculate secondary statistics and truncate result to toplist of given size.
        result[grp_key] = _calculate_secondary_stats(result[grp_key])
        result[grp_key] = truncate_stats(result[grp_key])

        # Mask the result to toplist of given size for all timeline time windows.
        for tl_stat in tmpres[ST_SKEY_TIMELINE]:
            tl_stat[1] = truncate_stats_with_mask(tl_stat[1], result[grp_key])

    return result


def calculate_timeline_config(dt_from, dt_to, max_count, min_step = None):
    """
    Calculate optimal configurations for timeline chart dataset.
    """
    dt_from, dt_to, delta = _calculate_timeline_boundaries(dt_from, dt_to)  # pylint: disable=locally-disabled,unused-variable
    step, step_count = _calculate_timeline_steps(dt_from, dt_to, max_count, min_step)
    return {
        ST_SKEY_DT_FROM: dt_from,
        ST_SKEY_DT_TO: dt_to,
        'step': step,
        'count': step_count
    }


def calculate_timeline_config_daily(dt_from, dt_to):
    """
    Calculate optimal configurations for timeline chart dataset with steps forced to one day.
    """
    step = datetime.timedelta(days = 1)
    dt_from = dt_from.replace(
        hour = 0,
        minute = 0,
        second = 0,
        microsecond = 0
    )
    dt_to = dt_to.replace(
        hour = 0,
        minute = 0,
        second = 0,
        microsecond = 0
    ) + step

    step_count = int((dt_to - dt_from) / step)
    return {
        ST_SKEY_DT_FROM: dt_from,
        ST_SKEY_DT_TO: dt_to,
        'step': step,
        'count': step_count
    }


#-------------------------------------------------------------------------------


def _counter_inc(stats, stat, key, increment = 1):
    """
    Helper for incrementing given statistical parameter within given statistical
    bundle.

    :param dict stats: Structure containing all statistics.
    :param str stat: Name of the statistical category.
    :param str key: Name of the statistical key.
    :param int increment: Counter increment.
    :return: Updated structure containing statistics.
    :rtype: dict
    """

    # I have considered using setdefault() method, but the performance is worse
    # in comparison with using if (measured with cProfile module).
    if not stat in stats:
        stats[stat] = {}
    stats[stat][str(key)] = stats[stat].get(str(key), 0) + increment
    return stats


def _counter_inc_all(stats, stat, key_list, increment = 1):
    """
    Helper for incrementing multiple statistical parameters within given statistical
    bundle.

    :param dict stats: Structure containing all statistics.
    :param str stat: Name of the statistic category.
    :param str key_list: List of the names of the statistical keys.
    :param int increment: Counter increment.
    :return: Updated structure containing statistics.
    :rtype: dict
    """
    if key_list:
        for key in key_list:
            _counter_inc(stats, stat, key, increment)
    return stats

def _counter_inc_one(stats, stat, increment = 1):
    """
    Helper for incrementing given statistical parameter within given statistical
    bundle.

    :param dict stats: Structure containing all statistics.
    :param str stat: Name of the statistical category.
    :param str key: Name of the statistical key.
    :param int increment: Counter increment.
    :return: Updated structure containing statistics.
    :rtype: dict
    """

    # I have considered using setdefault() method, but the performance is worse
    # in comparison with using if (measured with cProfile module).
    if not stat in stats:
        stats[stat] = 0
    stats[stat] += increment
    return stats


def _include_event_to_stats(stats, event, recurring = False, skip = None):
    """
    Include given IDEA event into given statistical record.
    """
    stats[ST_SKEY_CNT_EVENTS] = stats.get(ST_SKEY_CNT_EVENTS, 0) + 1

    # Mark recurring events.
    if recurring:
        stats[ST_SKEY_CNT_RECURR] = stats.get(ST_SKEY_CNT_RECURR, 0) + 1

    # Evaluate event according to given list of aggregation rules.
    reg = {}
    for rule in LIST_AGGREGATIONS:
        if skip and rule[0] in skip:
            continue

        values = []
        for jpath in rule[1]:
            values = values + jpath_values(event, jpath)
        reg[rule[0]] = values

        if not values:
            _counter_inc(stats, rule[0], rule[2])
            continue

        for val in values:
            _counter_inc(stats, rule[0], val)

    # Calculate additional statistics based on the values of existing aggregation
    # rules.
    if ST_SKEY_CATEGORIES in reg and reg[ST_SKEY_CATEGORIES]:
        key = '/'.join(reg[ST_SKEY_CATEGORIES])
        _counter_inc(stats, ST_SKEY_CATEGSETS, key)

    if ST_SKEY_DETECTORS in reg and reg[ST_SKEY_DETECTORS] and ST_SKEY_ANALYZERS in reg and reg[ST_SKEY_ANALYZERS]:
        for det in reg[ST_SKEY_DETECTORS]:
            for anl in reg[ST_SKEY_ANALYZERS]:
                key = '/'.join((det, anl))
                _counter_inc(stats, ST_SKEY_DETECTORSWS, key)
    elif ST_SKEY_DETECTORS in reg and reg[ST_SKEY_DETECTORS]:
        for det in reg[ST_SKEY_DETECTORS]:
            key = det
            _counter_inc(stats, ST_SKEY_DETECTORSWS, key)


def _merge_stats(stats, result = None):
    """
    Merge given statistical record into given result record.

    :param dict stats: Statistical record to be merged.
    :param dict result: Optional data structure for merged result.
    :return: Structure containing merged event statistics.
    :rtype: dict
    """
    if result is None:
        result = dict()

    result[ST_SKEY_CNT_ALERTS] = result.get(ST_SKEY_CNT_ALERTS, 0) + stats.get(ST_SKEY_CNT_ALERTS, 0)
    result[ST_SKEY_CNT_EVENTS] = result[ST_SKEY_CNT_ALERTS]

    for key in LIST_CALCSTAT_KEYS:
        if key in stats:
            for subkey, subval in stats[key].items():
                _counter_inc(result, key, subkey, subval)

    return result


def _include_report_to_stats(stats, report):
    """
    Merge given report statistical record into given result record.

    :param dict stats: Data structure for merged result.
    :param dict stats: Report statistical record to be merged.
    :return: Structure containing merged event statistics.
    :rtype: dict
    """
    stats[ST_SKEY_CNT_REPORTS] = stats.get(ST_SKEY_CNT_REPORTS, 0) + 1
    stats[ST_SKEY_CNT_EMAILS]  = stats.get(ST_SKEY_CNT_EMAILS, 0) + len(report.mail_to or [])

    # Include the 'summary' report into the overall statistics in full.
    if report.type == REPORT_TYPE_SUMMARY:
        stats[ST_SKEY_CNT_REPS_S] = stats.get(ST_SKEY_CNT_REPS_S, 0) + 1
        stats[ST_SKEY_CNT_EVENTS] = stats.get(ST_SKEY_CNT_EVENTS, 0) + report.evcount_rep     # Number of reported events.
        stats[ST_SKEY_CNT_EVTS_A] = stats.get(ST_SKEY_CNT_EVTS_A, 0) + report.evcount_all     # Total number of all matched events.
        stats[ST_SKEY_CNT_EVTS_F] = stats.get(ST_SKEY_CNT_EVTS_F, 0) + report.evcount_flt_blk # Number of filtered out events.
        stats[ST_SKEY_CNT_EVTS_T] = stats.get(ST_SKEY_CNT_EVTS_T, 0) + report.evcount_thr_blk # Number of thresholded out events.
        stats[ST_SKEY_CNT_EVTS_N] = stats.get(ST_SKEY_CNT_EVTS_N, 0) + report.evcount_new     # Number of new events.
        stats[ST_SKEY_CNT_EVTS_R] = stats.get(ST_SKEY_CNT_EVTS_R, 0) + report.evcount_rlp     # Number of relapsed events.

        stats[ST_SKEY_DT_FROM] = min(
            report.dt_from,
            stats.get(ST_SKEY_DT_FROM, report.dt_from)
        )
        stats[ST_SKEY_DT_TO] = max(
            report.dt_to,
            stats.get(ST_SKEY_DT_TO, report.dt_to)
        )

        for key in LIST_CALCSTAT_KEYS:
            if key in report.statistics and key not in (ST_SKEY_ABUSES,):
                for subkey, subval in report.statistics[key].items():
                    _counter_inc(stats, key, subkey, subval)

        _counter_inc_all(stats, ST_SKEY_EMAILS, report.mail_to)

        # This fixes the bug with missing part of the timeline chart where some
        # data was not yet being generated.
        for group in report.groups:
            _counter_inc(stats, ST_SKEY_ABUSES, group.name, report.evcount_all)

    # Include the 'extra' report into the overall statistics.
    else:
        stats[ST_SKEY_CNT_REPS_E] = stats.get(ST_SKEY_CNT_REPS_E, 0) + 1

    return stats


def _calculate_secondary_stats(stats):
    """
    Calculate common secondary statistics.

    :param dict stats: Structure containing single statistic category.
    :return: Updated structure containing statistics.
    :rtype: dict
    """
    # Calculate unique and recurring events.
    if ST_SKEY_CNT_EVENTS in stats:
        if ST_SKEY_CNT_RECURR in stats:
            stats[ST_SKEY_CNT_UNIQUE] = stats[ST_SKEY_CNT_EVENTS] - stats[ST_SKEY_CNT_RECURR]
        else:
            stats[ST_SKEY_CNT_UNIQUE] = stats[ST_SKEY_CNT_EVENTS]
            stats[ST_SKEY_CNT_RECURR] = 0

    return stats


def _make_toplist(stats, dict_key, top_threshold, force = False):
    """
    Produce only toplist of given statistical keys.

    :param dict stats: Calculated statistics.
    :param str dict_key: Name of the dictionary key within statistics containing values.
    :param int top_threshold: Number of desired items in toplist.
    :param bool force: Force the toplist threshold even to whitelisted keys.
    :return: Updated statistics structure.
    :rtype: dict
    """
    if dict_key in TRUNCATION_WHITELIST and not force:
        top_threshold = TRUNCATION_WHITELIST_THRESHOLD

    # Convert threshold to list index.
    top_threshold -= 1

    # Store current value of __REST__ subkey to temporary variable.
    rest = None
    if ST_SKEY_REST in stats[dict_key]:
        rest = stats[dict_key][ST_SKEY_REST]
        del stats[dict_key][ST_SKEY_REST]

    # Produce list of dictionary keys sorted in reverse order by their values.
    sorted_key_list = sorted(sorted(stats[dict_key].keys()), key=lambda x: stats[dict_key][x], reverse=True)
    sorted_key_list_keep  = sorted_key_list[:top_threshold]
    sorted_key_list_throw = sorted_key_list[top_threshold:]

    # Create truncated result into temporary data structure.
    tmp = {}
    tmp = {key: stats[dict_key][key] for key in sorted_key_list_keep}

    # Calculate and store the total for what was omitted into the __REST__ subkey.
    if sorted_key_list_throw:
        tmp[ST_SKEY_REST] = sum([stats[dict_key][key] for key in sorted_key_list_throw])

    # Add previous value of the __REST__ subkey.
    if rest:
        tmp[ST_SKEY_REST] = tmp.get(ST_SKEY_REST, 0) + rest

    # Put everything back into original statistics.
    stats[dict_key] = tmp

    return stats


def _mask_toplist(stats, mask, dict_key, top_threshold, force = False):
    """
    Produce only toplist of given statistical keys. Use global statistics as mask
    to determine which items to hide.

    :param dict stats: Calculated statistics.
    :param dict mask: Calculated overall statistics for masking.
    :param str dict_key: Name of the dictionary key within statistics containing values.
    :param int top_threshold: Number of desired items in toplist.
    :param bool force: Force the toplist threshold even to whitelisted keys.
    :return: Updated statistics structure.
    :rtype: dict
    """
    if dict_key in TRUNCATION_WHITELIST and not force:
        top_threshold = TRUNCATION_WHITELIST_THRESHOLD

    # Convert threshold to list index.
    top_threshold -= 1

    # Store current value of __REST__ subkey to temporary variable.
    rest = None
    if ST_SKEY_REST in stats[dict_key]:
        rest = stats[dict_key][ST_SKEY_REST]
        del stats[dict_key][ST_SKEY_REST]

    # Produce list of desired dictionary keys by calculating list intersection
    # with given mask.
    wanted_keys = mask[dict_key].keys()
    stat_key_list = [x for x in wanted_keys if x in stats[dict_key]]
    stat_key_list_keep  = stat_key_list[:top_threshold]
    stat_key_list_throw = [x for x in stats[dict_key].keys() if x not in stat_key_list_keep]

    # Create truncated result into temporary data structure.
    tmp = {}
    tmp = {key: stats[dict_key][key] for key in stat_key_list_keep}

    # Calculate and store the total for what was omitted.
    if stat_key_list_throw:
        tmp[ST_SKEY_REST] = sum([stats[dict_key][key] for key in stat_key_list_throw])

    # Add previous value of the __REST__ subkey.
    if rest:
        tmp[ST_SKEY_REST] = tmp.get(ST_SKEY_REST, 0) + rest

    # Put everything back into original statistics.
    stats[dict_key] = tmp

    return stats


def _calculate_timeline_boundaries(dt_from, dt_to):
    """
    Calculate optimal and rounded values for lower and upper timeline boundaries
    from given timestamps.
    """
    delta_minute = datetime.timedelta(minutes = 1)
    delta_hour   = datetime.timedelta(hours = 1)
    delta_day    = datetime.timedelta(days = 1)

    delta = dt_to - dt_from

    # For delta of timeline boundaries below one hour round to the whole 5 minutes.
    if delta <= delta_hour:
        return (
            dt_from.replace(
                minute = dt_from.minute - (dt_from.minute % 5),
                second = 0,
                microsecond = 0
            ),
            dt_to.replace(
                second = 0,
                microsecond = 0
            ) + (delta_minute * (5 - (dt_to.minute % 5))),
            delta_minute * 5
        )

    # For delta of timeline boundaries below one day round to the whole hours.
    if delta <= delta_day:
        return (
            dt_from.replace(
                minute = 0,
                second = 0,
                microsecond = 0
            ),
            dt_to.replace(
                minute = 0,
                second = 0,
                microsecond = 0
            ) + delta_hour,
            delta_hour
        )

    # Everything else round to the whole days.
    return (
        dt_from.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0
        ),
        dt_to.replace(
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0
        ) + delta_day,
        delta_day
    )


def _calculate_timeline_steps(dt_from, dt_to, max_count, min_step = None):
    """
    Calculate optimal timeline step/window from given optimal lower and upper
    boundary and maximal number of steps.
    """
    delta = dt_to - dt_from
    step_size = int(math.ceil(delta.total_seconds()/max_count))

    if min_step and step_size < min_step:
        step_size = min_step

    # Attempt to optimalize the step size
    idx = bisect.bisect_left(LIST_OPTIMAL_STEPS, step_size)
    if idx != len(LIST_OPTIMAL_STEPS):
        step_size = LIST_OPTIMAL_STEPS[idx]

    step = datetime.timedelta(seconds = step_size)

    # Calculate actual step count, that will cover the requested timeline.
    step_count = int(math.ceil(delta/step))

    return (step, step_count)


def _init_time_scatter():
    """
    Init structure for time scatter chart dataset.
    """
    return [[{} for y in range(24)] for x in range(7)]


def _init_timeline(dt_from, dt_to, max_count, min_step = None):
    """
    Init structure for timeline chart dataset.
    """
    timeline_cfg = calculate_timeline_config(dt_from, dt_to, max_count, min_step)

    dt_from = timeline_cfg[ST_SKEY_DT_FROM]
    timeline = list()
    for i in range(timeline_cfg['count']):  # pylint: disable=locally-disabled,unused-variable
        timeline.append([dt_from, {}])
        dt_from = dt_from + timeline_cfg['step']
    return timeline, timeline_cfg


def _init_daily_timeline(dt_from, dt_to):
    """
    Init structure for timeline chart dataset with steps forced to one day. Given
    time interval parameters will be rounded to whole days as necessary.

    :param datetime.datetime dt_from: Lower time interval boundary.
    :param datetime.datetime dt_to: Lower time interval boundary.
    :return: Tuple containing preinitialized timeline structure and dictionary describing final timeline configuration.
    :rtype: tuple
    """
    timeline_cfg = calculate_timeline_config_daily(dt_from, dt_to)

    dt_from = timeline_cfg[ST_SKEY_DT_FROM]
    timeline = list()
    for i in range(timeline_cfg['count']):  # pylint: disable=locally-disabled,unused-variable
        timeline.append([dt_from, {}])
        dt_from = dt_from + timeline_cfg['step']
    return timeline, timeline_cfg

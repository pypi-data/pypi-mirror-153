#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains global application-wide constants for Hawat user interface.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"



CFGKEY_MENTAT_CORE = 'MENTAT_CORE'
"""Configuration key name: Core Mentat configurations."""

CFGKEY_MENTAT_CACHE_DIR = 'MENTAT_CACHE_DIR'
"""Configuration key name: Path to Mentat cache dir."""

DEFAULT_RESULT_TIMEDELTA = 7
"""Default result time delta for searching various objects."""

#
# List of all existing Context Search Action Group names (CSAG).
#
CSAG_ABUSE    = 'abuses'
CSAG_ADDRESS  = 'ips'
CSAG_CATEGORY = 'categories'
CSAG_CLASS    = 'classes'
CSAG_DETECTOR = 'detectors'
CSAG_DETTYPE  = 'detector_types'
CSAG_HOSTTYPE = 'host_types'
CSAG_PORT     = 'ports'
CSAG_PROTOCOL = 'protocols'
CSAG_SEVERITY = 'severities'

#
# List of all existing Additonal Object Data Service names (AODS).
#
AODS_IP4 = 'ip4'
AODS_IP6 = 'ip6'


ICONS = {

    #
    # General icons.
    #
    'login':     '<i class="fas fa-fw fa-sign-in-alt"></i>',
    'logout':    '<i class="fas fa-fw fa-sign-out-alt"></i>',
    'register':  '<i class="fas fa-fw fa-user-plus"></i>',
    'help':      '<i class="fas fa-fw fa-question-circle"></i>',
    'language':  '<i class="fas fa-fw fa-globe"></i>',

    'role-anonymous':  '<i class="fas fa-fw fa-user-secret"></i>',
    'role-user':       '<i class="fas fa-fw fa-user"></i>',
    'role-developer':  '<i class="fas fa-fw fa-user-md"></i>',
    'role-maintainer': '<i class="fas fa-fw fa-user-tie"></i>',
    'role-admin':      '<i class="fas fa-fw fa-user-ninja"></i>',

    #
    # Main site section icons.
    #
    'section-home':           '<i class="fas fa-fw fa-home"></i>',
    'section-dashboards':     '<i class="fas fa-fw fa-tachometer-alt"></i>',
    'section-more':           '<i class="fas fa-fw fa-puzzle-piece"></i>',
    'section-administration': '<i class="fas fa-fw fa-cogs"></i>',
    'section-development':    '<i class="fas fa-fw fa-bug"></i>',

    #
    # Built-in module icons.
    #
    'module-home':               '<i class="fas fa-fw fa-home"></i>',
    'module-auth-api':           '<i class="fas fa-fw fa-id-card-alt"></i>',
    'module-auth-dev':           '<i class="fas fa-fw fa-id-card-alt"></i>',
    'module-auth-env':           '<i class="fas fa-fw fa-id-card-alt"></i>',
    'module-changelogs':         '<i class="fas fa-fw fa-clipboard-list"></i>',
    'module-dashboards':         '<i class="fas fa-fw fa-tachometer-alt"></i>',
    'module-dbstatus':           '<i class="fas fa-fw fa-database"></i>',
    'module-design':             '<i class="fas fa-fw fa-palette"></i>',
    'module-devtools':           '<i class="fas fa-fw fa-bug"></i>',
    'module-dnsr':               '<i class="fas fa-fw fa-directions"></i>',
    'module-events':             '<i class="fas fa-fw fa-bell"></i>',
    'module-filters':            '<i class="fas fa-fw fa-filter"></i>',
    'module-geoip':              '<i class="fas fa-fw fa-map-marked-alt"></i>',
    'module-groups':             '<i class="fas fa-fw fa-users"></i>',
    'module-help':               '<i class="fas fa-fw fa-question-circle"></i>',
    'module-hosts':              '<i class="fas fa-fw fa-server"></i>',
    'module-networks':           '<i class="fas fa-fw fa-sitemap"></i>',
    'module-nerd':               '<i class="fas fa-fw fa-certificate"></i>',
    'module-pdnsr':              '<i class="fas fa-fw fa-compass"></i>',
    'module-performance':        '<i class="fas fa-fw fa-chart-bar"></i>',
    'module-reports':            '<i class="fas fa-fw fa-newspaper"></i>',
    'module-settings-reporting': '<i class="fas fa-fw fa-sliders-h"></i>',
    'module-skeleton':           '<i class="fas fa-fw fa-skull"></i>',
    'module-status':             '<i class="fas fa-fw fa-heartbeat"></i>',
    'module-timeline':           '<i class="fas fa-fw fa-chart-line"></i>',
    'module-users':              '<i class="fas fa-fw fa-user"></i>',
    'module-whois':              '<i class="fas fa-fw fa-map-signs"></i>',

    'profile': '<i class="fas fa-fw fa-id-card"></i>',

    'modal-question': '<i class="fas fa-fw fa-question-circle"></i>',

    'missing-icon': '<i class="fas fa-fw fa-question" title="Missing icon"></i>',

    #
    # Action icons.
    #
    'action-sort':         '<i class="fas fa-fw fa-sort"></i>',
    'action-sort-asc':     '<i class="fas fa-fw fa-sort-up"></i>',
    'action-sort-desc':    '<i class="fas fa-fw fa-sort-down"></i>',
    'action-more':         '<i class="fas fa-fw fa-cubes"></i>',
    'action-search':       '<i class="fas fa-fw fa-search"></i>',
    'action-show':         '<i class="fas fa-fw fa-eye"></i>',
    'action-show-user':    '<i class="fas fa-fw fa-user-circle"></i>',
    'action-create':       '<i class="fas fa-fw fa-plus-circle"></i>',
    'action-create-user':  '<i class="fas fa-fw fa-user-plus"></i>',
    'action-update':       '<i class="fas fa-fw fa-edit"></i>',
    'action-update-user':  '<i class="fas fa-fw fa-user-edit"></i>',
    'action-enable':       '<i class="fas fa-fw fa-unlock"></i>',
    'action-enable-user':  '<i class="fas fa-fw fa-user-check"></i>',
    'action-disable':      '<i class="fas fa-fw fa-lock"></i>',
    'action-disable-user': '<i class="fas fa-fw fa-user-lock"></i>',
    'action-delete':       '<i class="fas fa-fw fa-trash"></i>',
    'action-delete-user':  '<i class="fas fa-fw fa-user-slash"></i>',
    'action-add-member':   '<i class="fas fa-fw fa-user-plus"></i>',
    'action-rej-member':   '<i class="fas fa-fw fa-user-minus"></i>',
    'action-rem-member':   '<i class="fas fa-fw fa-user-times"></i>',
    'action-save':         '<i class="fas fa-fw fa-save"></i>',
    'action-download':     '<i class="fas fa-fw fa-file-download"></i>',
    'action-download-zip': '<i class="fas fa-fw fa-file-archive"></i>',
    'action-download-csv': '<i class="fas fa-fw fa-file-csv"></i>',
    'action-download-svg': '<i class="fas fa-fw fa-file-image"></i>',
    'action-download-js':  '<i class="fab fa-fw fa-js"></i>',
    'action-mail':         '<i class="fas fa-fw fa-envelope"></i>',
    'action-reload':       '<i class="fas fa-fw fa-sync-alt"></i>',
    'action-genkey':       '<i class="fas fa-fw fa-key"></i>',
    'action-stop':         '<i class="fas fa-fw fa-stop-circle"></i>',

    'alert-success': '<i class="fas fa-fw fa-check-circle"></i>',
    'alert-info':    '<i class="fas fa-fw fa-info-circle"></i>',
    'alert-warning': '<i class="fas fa-fw fa-exclamation-circle"></i>',
    'alert-danger':  '<i class="fas fa-fw fa-exclamation-triangle"></i>',

    'item-enabled':  '<i class="fas fa-fw fa-toggle-on"></i>',
    'item-disabled': '<i class="fas fa-fw fa-toggle-off"></i>',

    'r-t-summary':  '<i class="fas fa-fw fa-archive"></i>',
    'r-t-extra':    '<i class="fas fa-fw fa-file-alt"></i>',
    'r-s-unknown':  '<i class="fas fa-fw fa-thermometer-empty"></i>',
    'r-s-low':      '<i class="fas fa-fw fa-thermometer-quarter"></i>',
    'r-s-medium':   '<i class="fas fa-fw fa-thermometer-half"></i>',
    'r-s-high':     '<i class="fas fa-fw fa-thermometer-three-quarters"></i>',
    'r-s-critical': '<i class="fas fa-fw fa-thermometer-full"></i>',

    'report-data-relapsed': '<i class="fas fa-fw fa-sync-alt"></i>',
    'report-data-filtered': '<i class="fas fa-fw fa-filter"></i>',
    'report-data-test':     '<i class="fas fa-fw fa-bug"></i>',
    'report-data-mailed':   '<i class="fas fa-fw fa-envelope"></i>',

    'ajax-loader': '<i class="fas fa-fw fa-spinner fa-spin fa-4x"></i>',
    'caret-down':  '<i class="fas fa-fw fa-caret-square-down"></i>',
    'unassigned':  '<i class="fas fa-fw fa-minus"></i>',
    'undisclosed': '<i class="fas fa-fw fa-minus"></i>',
    'calendar':    '<i class="fas fa-fw fa-calendar-alt"></i>',
    'stopwatch':   '<i class="fas fa-fw fa-stopwatch"></i>',
    'clock':       '<i class="fas fa-fw fa-clock"></i>',
    'domain':      '<i class="fas fa-fw fa-tag"></i>',
    'time-from':   '<i class="fas fa-fw fa-hourglass-start"></i>',
    'time-to':     '<i class="fas fa-fw fa-hourglass-end"></i>',
    'debug':       '<i class="fas fa-fw fa-bug"></i>',
    'eventclss':   '<i class="fas fa-fw fa-book"></i>',
    'reference':   '<i class="fas fa-fw fa-external-link-alt"></i>',
    'anchor':      '<i class="fas fa-fw fa-anchor"></i>',
    'search':      '<i class="fas fa-fw fa-search"></i>',
    'weight':      '<i class="fas fa-fw fa-weight"></i>',
    'list':        '<i class="fas fa-fw fa-list-ul"></i>',
    'mail':        '<i class="fas fa-fw fa-envelope"></i>',
    'redirect':    '<i class="fas fa-fw fa-share"></i>',
    'unredirect':  '<span class="fa-layers fa-fw"><i class="fas fa-fw fa-share"></i><i class="fas fa-fw fa-ban"></i></span>',
    'mute':        '<i class="fas fa-fw fa-volume-off"></i>',
    'unmute':      '<i class="fas fa-fw fa-volume-up"></i>',
    'compress':    '<i class="fas fa-fw fa-gift"></i>',
    'uncompress':  '<span class="fa-layers fa-fw"><i class="fas fa-fw fa-gift"></i><i class="fas fa-fw fa-ban"></i></span>',
    'import':      '<i class="fas fa-fw fa-cloud-upload"></i>',
    'export':      '<i class="fas fa-fw fa-cloud-download"></i>',
    'validate':    '<i class="fas fa-fw fa-check-circle"></i>',
    'min':         '<i class="fas fa-fw fa-angle-double-down"></i>',
    'max':         '<i class="fas fa-fw fa-angle-double-up"></i>',
    'sum':         '<i class="fas fa-fw fa-plus"></i>',
    'cnt':         '<i class="fas fa-fw fa-hashtag"></i>',
    'avg':         '<i class="fas fa-fw fa-dot-circle"></i>',
    'med':         '<i class="fas fa-fw fa-bullseye"></i>',
    'na':          '<i class="fas fa-fw fa-times"></i>',
    'stats':       '<i class="fas fa-fw fa-bar-chart"></i>',
    'structure':   '<i class="fas fa-fw fa-tree"></i>',
    'actions':     '<i class="fas fa-fw fa-wrench"></i>',
    'cog':         '<i class="fas fa-fw fa-cog"></i>',
    'check':       '<i class="fas fa-fw fa-check-square"></i>',
    'check_blank': '<i class="far fa-fw fa-square"></i>',
    'ok':          '<i class="fas fa-fw fa-check"></i>',
    'ko':          '<i class="fas fa-fw fa-times"></i>',
    'sortasc':     '<i class="fas fa-fw fa-sort-asc"></i>',
    'sortdesc':    '<i class="fas fa-fw fa-sort-desc"></i>',
    'backtotop':   '<i class="fas fa-fw fa-level-up-alt"></i>',
    'first':       '<i class="fas fa-fw fa-angle-double-left"></i>',
    'previous':    '<i class="fas fa-fw fa-angle-left"></i>',
    'next':        '<i class="fas fa-fw fa-angle-right"></i>',
    'last':        '<i class="fas fa-fw fa-angle-double-right" aria-hidden="true"></i>',
    'liitem':      '<i class="fas fa-li fa-asterisk" aria-hidden="true"></i>',
    'expand':      '<i class="fas fa-fw fa-angle-left" aria-hidden="true"></i>',
    'collapse':    '<i class="fas fa-fw fa-angle-down" aria-hidden="true"></i>',
    'form-error':  '<i class="fas fa-fw fa-exclamation-triangle" aria-hidden="true"></i>',
    'table':       '<i class="fas fa-fw fa-table"></i>',
    'quicksearch': '<i class="fab fa-fw fa-searchengin"></i>',
    'playground':  '<i class="fas fa-fw fa-gamepad"></i>'
}
"""
Predefined list of selected `font-awesome <http://fontawesome.io/icons/>`__ icons
that are used in this application.
"""

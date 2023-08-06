#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base library for web interface unit test database fixtures.
"""


import vial.const


DEMO_GROUP_A = 'DEMO_GROUP_A'
DEMO_GROUP_B = 'DEMO_GROUP_B'


def get_fixtures_db(app):
    """
    Get general database object fixtures.
    """
    fixture_list = list()

    user_model  = app.get_model(vial.const.MODEL_USER)
    group_model = app.get_model(vial.const.MODEL_GROUP)

    def _gen_user(user_name):
        user = user_model(
            login = user_name,
            fullname = 'Demo {}'.format(user_name[0].upper() + user_name[1:]),
            email = '{}@bogus-domain.org'.format(user_name),
            roles = list(
                set(
                    [vial.const.ROLE_USER, user_name]
                )
            ),
            enabled = True,
            apikey = 'apikey-{}'.format(user_name)
        )
        fixture_list.append(user)
        return user

    account_user = _gen_user(vial.const.ROLE_USER)
    account_developer = _gen_user(vial.const.ROLE_DEVELOPER)
    account_maintainer = _gen_user(vial.const.ROLE_MAINTAINER)
    account_admin = _gen_user(vial.const.ROLE_ADMIN)

    def _gen_group(group_name, group_descr):
        group = group_model(
            name = group_name,
            description = group_descr,
            enabled = True
        )
        fixture_list.append(group)
        return group

    group_a = _gen_group(DEMO_GROUP_A, 'Demo Group A')
    group_b = _gen_group(DEMO_GROUP_B, 'Demo Group B')
    assert group_b      # Deliberately empty group

    group_a.members.append(account_user)
    group_a.members.append(account_developer)
    group_a.members.append(account_maintainer)
    group_a.members.append(account_admin)

    group_a.managers.append(account_developer)
    group_a.managers.append(account_maintainer)

    return fixture_list

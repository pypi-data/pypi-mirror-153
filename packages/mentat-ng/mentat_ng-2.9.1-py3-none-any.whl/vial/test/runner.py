#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base library for web interface unit tests.
"""


import vial
import vial.app
import vial.db
import vial.model.db
import vial.test.fixtures


#logging.disable(logging.CRITICAL+1000)


def _config_testapp_vial(app_config):
    """
    Configure and reconfigure application for testing before instantination.
    """

    # Customize configurations for testing purposes.
    app_config['TESTING'] = True
    app_config['WTF_CSRF_ENABLED'] = False
    app_config['DEBUG'] = False
    app_config['EXPLAIN_TEMPLATE_LOADING'] = False
    app_config['LOG_FILE'] = '/var/tmp/vial-utest.log'
    app_config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mentat:mentat@localhost/mentat_utest'
    app_config['MAIL_SERVER'] = 'localhost'
    app_config['MAIL_PORT'] = 1025
    app_config['MAIL_DEFAULT_SENDER'] = 'root@unittest'
    app_config['EMAIL_ADMINS'] = ['admin@unittest']
    app_config['MODELS'] = {
        vial.const.MODEL_USER: vial.model.db.UserModel,
        vial.const.MODEL_GROUP: vial.model.db.GroupModel,
        vial.const.MODEL_ITEM_CHANGELOG: vial.model.db.ItemChangeLogModel
    }


class TestRunnerMixin:
    def setup_app(self):
        """
        Setup application object.
        """
        return vial.create_app_full(
            vial.app.Vial,
            'vial',
            config_object = 'vial.config.TestingConfig',
            config_func = _config_testapp_vial
        )

    def get_fixtures_db(self, app):
        return vial.test.fixtures.get_fixtures_db(app)

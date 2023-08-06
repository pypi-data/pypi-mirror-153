#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base library for web interface unit tests.
"""


import io
import unittest
import pprint
import logging
import flask_mail
import vial
import vial.app
import vial.db


class do_as_user_decorator:  # pylint: disable=locally-disabled,invalid-name,too-few-public-methods
    """
    Decorator class for accessing application endpoints as given user.
    """
    def __init__(self, user_name, login_func_name = 'login_dev', login_func_params = None):
        self.user_name         = user_name
        self.login_func_name   = login_func_name
        self.login_func_params = login_func_params or {}

    def __call__(self, func):
        def wrapped_f(other_self, *args, **kwargs):
            login_func = getattr(other_self, self.login_func_name)
            response = login_func(self.user_name, **self.login_func_params)
            other_self.assertEqual(response.status_code, 200)

            func(other_self, *args, **kwargs)

            response = other_self.logout()
            other_self.assertEqual(response.status_code, 200)

        return wrapped_f


def app_context_wrapper_decorator(func):
    """
    Decorator class for conditional wrapping of given function with application context.
    """
    def wrapped_f(self, *args, **kwargs):
        if 'with_app_ctx' not in kwargs or not kwargs['with_app_ctx']:
            return func(self, *args, **kwargs)
        with self.app.app_context():
            return func(self, *args, **kwargs)

    return wrapped_f


class VialTestCase(unittest.TestCase):
    """
    Class for testing :py:class:`vial.app.Vial` application.
    """

    logger = logging.getLogger()
    logger.level = logging.DEBUG

    def on_email_sent(self, message, app):  # pylint: disable=locally-disabled,unused-argument
        """
        Signal handler for handling :py:func:`flask_mail.email_dispatched` signal.
        Log subject and recipients of all emails that have been sent.
        """
        #pprint.pprint(message)
        #app.logger.info(
        #    "Sent email '%s' to '%s'",
        #    message.subject,
        #    ', '.join(message.recipients)
        #)
        self.mailbox.append(message)

    #--------------------------------------------------------------------------

    def setUp(self):
        self.setup_logging()
        self.mailbox = []
        self.fixtures_db = []

        self.app = self.setup_app()
        self.client = self.app.test_client()
        self.setup_db()

    def setup_logging(self):
        """
        Setup logging configuration for testing purposes.
        """
        #for hdlr in self.logger.handlers:
        #    self.logger.removeHandler(hdlr)
        self.loghdlr = logging.StreamHandler(io.StringIO())
        self.logger.addHandler(self.loghdlr)

    def setup_app(self):
        """
        Setup application object.
        """
        raise NotImplementedError()

    def setup_db(self):
        """
        Perform database setup.
        """
        with self.app.app_context():
            vial.db.db_get().drop_all()
            vial.db.db_get().create_all()
            self.setup_fixtures_db()

    def get_fixtures_db(self, app):
        raise NotImplementedError()

    def setup_fixtures_db(self):
        """
        Setup general database object fixtures.
        """
        fixture_list = self.get_fixtures_db(self.app)
        for dbobject in fixture_list:
            vial.db.db_session().add(dbobject)
            vial.db.db_session().commit()
        self.fixtures_db.extend(fixture_list)

    #--------------------------------------------------------------------------

    def tearDown(self):
        self.teardown_logging()
        self.teardown_db()

    def teardown_logging(self):
        """
        Teardown logging configuration for testing purposes.
        """
        #print(
        #    "CAPTURED LOG CONTENTS:\n{}".format(
        #        self.loghdlr.stream.getvalue()
        #    )
        #)
        self.loghdlr.stream.close()
        self.logger.removeHandler(self.loghdlr)

    def teardown_db(self):
        with self.app.app_context():
            vial.db.db_get().drop_all()

    #--------------------------------------------------------------------------

    def login_dev(self, login):
        """
        Login given user with *auth_dev* module.
        """
        return self.client.post(
            '/auth_dev/login',
            data = dict(login = login, submit = 'Login'),
            follow_redirects = True
        )

    def login_pwd(self, login, password):
        """
        Login given user with *auth_pwd* module.
        """
        return self.client.post(
            '/auth_pwd/login',
            data = dict(login = login, password = password, submit = 'Login'),
            follow_redirects = True
        )

    def login_env(self, login, envvar = 'eppn'):
        """
        Login given user with *auth_env* module.
        """
        return self.client.get(
            '/auth_env/login',
            environ_base = {envvar: login},
            follow_redirects = True
        )

    def logout(self):
        """
        Logout current user.
        """
        return self.client.get(
            '/logout',
            follow_redirects = True
        )

    #--------------------------------------------------------------------------

    def log_get(self):
        """
        Get content written to log so far.
        """
        return self.loghdlr.stream.getvalue()

    def log_clear(self):
        """
        Clear log content.
        """
        self.loghdlr.stream.close()
        self.loghdlr.stream = io.StringIO()

    #--------------------------------------------------------------------------

    def mailbox_clear(self):
        """
        Clear internal mailbox.
        """
        self.mailbox = []

    def mailbox_monitoring(self, state):
        """
        Enable/disable mailbox monitoring.
        """
        if state == 'on':
            flask_mail.email_dispatched.connect(self.on_email_sent)
            return

        if state == 'off':
            flask_mail.email_dispatched.disconnect(self.on_email_sent)
            return

        raise ValueError(
            'Invalid parameter for mailbox_monitoring, must be "on" or "off", received {}'.format(
                str(state)
            )
        )

    #--------------------------------------------------------------------------

    def user_model(self):
        """
        Get user model class.
        """
        return self.app.get_model(vial.const.MODEL_USER)

    @app_context_wrapper_decorator
    def user_get(self, user_name, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Get user object according to given user name from database.
        """
        user_model = self.user_model()
        return vial.db.db_session().query(user_model).filter(user_model.login == user_name).one_or_none()

    @app_context_wrapper_decorator
    def user_save(self, user_object, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Update given user object within database.
        """
        vial.db.db_session().add(user_object)
        vial.db.db_session().commit()

    @app_context_wrapper_decorator
    def user_id(self, user_name, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Get ID of user with given name within database.
        """
        uobj = self.user_get(user_name)
        return uobj.id

    @app_context_wrapper_decorator
    def user_enabled(self, user_name, state, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Enable/disable given user within database.
        """
        user = self.user_get(user_name)
        user.enabled = state
        self.user_save(user)

    #--------------------------------------------------------------------------

    def group_model(self):
        """
        Get user model class.
        """
        return self.app.get_model(vial.const.MODEL_GROUP)

    @app_context_wrapper_decorator
    def group_get(self, group_name, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Get group object according to given group name within database.
        """
        group_model = self.group_model()
        return vial.db.db_session().query(group_model).filter(group_model.name == group_name).one_or_none()

    @app_context_wrapper_decorator
    def group_save(self, group_object, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Update given group object within database.
        """
        vial.db.db_session().add(group_object)
        vial.db.db_session().commit()

    @app_context_wrapper_decorator
    def group_id(self, group_name, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Get ID of given group within database.
        """
        gobj = self.group_get(group_name)
        return gobj.id

    @app_context_wrapper_decorator
    def group_enabled(self, group_name, state, **kwargs):  # pylint: disable=locally-disabled,unused-argument
        """
        Enable/disable given group within database.
        """
        group = self.group_get(group_name)
        group.enabled = state
        self.group_save(group)

    #--------------------------------------------------------------------------

    def assertGetURL(self, url, status_code = 200, content_checks = None, print_response = False, follow_redirects = True):  # pylint: disable=locally-disabled,invalid-name
        """
        Perform GET request and check some default assertions against the response.
        """
        response = self.client.get(
            url,
            follow_redirects = follow_redirects
        )
        if print_response:
            print("--------------------------------------------------------------------------------")
            print("Response for GET {}: {} ({})".format(url, response.status_code, response.status))
            pprint.pprint(response.headers)
            pprint.pprint(response.data)
            print("--------------------------------------------------------------------------------")
        self.assertEqual(response.status_code, status_code)
        if content_checks:
            for cch in content_checks:
                self.assertTrue(cch in response.data)
        return response

    def assertPostURL(self, url, data, status_code = 200, content_checks = None, print_response = False, follow_redirects = True):  # pylint: disable=locally-disabled,invalid-name
        """
        Perform POST request and check some default assertions against the response.
        """
        response = self.client.post(
            url,
            data = data,
            follow_redirects = follow_redirects
        )
        if print_response:
            print("--------------------------------------------------------------------------------")
            print("Response for POST {}, {}: {} ({})".format(url, pprint.pformat(data), response.status_code, response.status))
            pprint.pprint(response.headers)
            pprint.pprint(response.data)
            print("--------------------------------------------------------------------------------")
        self.assertEqual(response.status_code, status_code)
        if content_checks:
            for cch in content_checks:
                self.assertTrue(cch in response.data)
        return response

    def assertMailbox(self, checklist):  # pylint: disable=locally-disabled,invalid-name
        """
        Check internal mailbox.
        """
        for attr_name in ('subject', 'sender', 'recipients', 'cc', 'bcc', 'body', 'html'):
            if attr_name in checklist:
                self.assertEqual(
                    list(
                        map(
                            lambda x: getattr(x, attr_name),
                            self.mailbox,
                        )
                    ),
                    checklist[attr_name]
                )

class ItemCreateVialTestCase(VialTestCase):
    """
    Class for testing :py:class:`vial.app.Vial` application item creation views.
    """
    maxDiff = None

    def assertCreate(self, item_model, url, data, content_checks = None, print_response = False):  # pylint: disable=locally-disabled,invalid-name
        """
        Perform attempt to create given item.
        """

        # Verify, that the item form correctly displays.
        response = self.assertGetURL(
            url,
            200,
            [
                '<form method="POST" action="{}" id="form-{}-create'.format(
                    url,
                    item_model.__name__.lower()
                ).encode('utf8'),
                b'<div class="btn-toolbar" role="toolbar" aria-label="Form submission buttons">'
            ],
            print_response = print_response
        )

        # Attempt to send empty item form. There is always at least one mandatory
        # form field, so we should get some "This field is required." error.
        request_data = {'submit': 'Submit'}
        response = self.assertPostURL(
            url,
            request_data,
            200,
            [
                b'This field is required.',
                b'help-block form-error'
            ],
            print_response = print_response
        )

        # Attempt to send form with some mandatory fields missing.
        #for idx, param in enumerate(data):
        #    if idx == len(data) - 1:
        #        break
        #    response = self.client.post(
        #        url,
        #        follow_redirects = True,
        #        data = {
        #            i[0]: i[1] for i in data[0:idx+1]
        #        }
        #    )
        #    self.assertEqual(response.status_code, 200)
        #    self.assertTrue(b'This field is required.' in response.data)
        #    self.assertTrue(b'help-block form-error' in response.data)

        # Attempt to send form with valid data.
        request_data = {
            i[0]: i[1] for i in data
        }
        request_data['submit'] = 'Submit'
        response = self.assertPostURL(
            url,
            request_data,
            200,
            [
                b'<div class="alert alert-success alert-dismissible">'
            ],
            print_response = print_response
        )
        if content_checks:
            for cch in content_checks:
                self.assertTrue(cch in response.data)
        return response


class RegistrationVialTestCase(VialTestCase):
    """
    Class for testing :py:class:`vial.app.Vial` application registration views.
    """
    maxDiff = None

    user_fixture = {
        'apikey': None,
        'email': 'test.user@domain.org',
        'enabled': False,
        'fullname': 'Test User',
        'id': 5,
        'locale': None,
        'login': 'test',
        'logintime': 'None',
        'managements': [],
        'memberships': [],
        'memberships_wanted': [],
        'roles': ['user'],
        'timezone': None
    }

    def assertRegisterFail(self, url, data, environ_base = None):  # pylint: disable=locally-disabled,invalid-name
        response = response = self.client.get(
            url,
            follow_redirects = True,
            environ_base = environ_base,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'User account registration' in response.data)

        for idx, param in enumerate(data):
            if idx == len(data) - 1:
                break
            response = response = self.client.post(
                url,
                follow_redirects = True,
                environ_base = environ_base,
                data = {
                    i[0]: i[1] for i in data[0:idx+1]
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'This field is required.' in response.data)
            self.assertTrue(b'help-block form-error' in response.data)

        response = response = self.client.post(
            url,
            follow_redirects = True,
            environ_base = environ_base,
            data = {
                i[0]: i[1] for i in data
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'Please use different login, the &#34;user&#34; is already taken.' in response.data or \
            b'Please use different login, the "user" is already taken.' in response.data
        )


    def assertRegister(self, url, data, emails, environ_base = None):  # pylint: disable=locally-disabled,invalid-name
        uname = 'test'
        self.mailbox_monitoring('on')

        response = response = self.client.get(
            url,
            follow_redirects = True,
            environ_base = environ_base
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'User account registration' in response.data)

        for idx, param in enumerate(data):
            if idx == len(data) - 1:
                break
            response = response = self.client.post(
                url,
                follow_redirects = True,
                environ_base = environ_base,
                data = {
                    i[0]: i[1] for i in data[0:idx+1]
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'This field is required.' in response.data)
            self.assertTrue(b'help-block form-error' in response.data)

        response = response = self.client.post(
            url,
            follow_redirects = True,
            environ_base = environ_base,
            data = {
                i[0]: i[1] for i in data
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'User account <strong>test (Test User)</strong> was successfully registered.' in response.data)
        with self.app.app_context():
            uobj = self.user_get(uname)
            self.assertTrue(uobj)
        self.assertMailbox(
            {
                'subject': [
                    '[{}] Account registration - {}'.format(self.app.config['APPLICATION_NAME'], uname),
                    '[{}] Account registration - {}'.format(self.app.config['APPLICATION_NAME'], uname)
                ],
                'sender': [
                    'root@unittest',
                    'root@unittest'
                ],
                'recipients': [
                    ['admin@unittest'],
                    ['test.user@domain.org']
                ],
                'cc': [[],[]],
                'bcc': [[], ['admin@unittest']],
                'body': emails['txt'],
                'html': emails['html']
            }
        )

        self.mailbox_monitoring('off')

        with self.app.app_context():
            user = self.user_get(uname)
            user_dict = user.to_dict()
            del user_dict['createtime']
            del user_dict['password']
            self.assertEqual(
                user_dict,
                self.user_fixture
            )
        response = self.login_dev(uname)
        self.assertEqual(response.status_code, 403)
        #self.assertTrue(b'is currently disabled, you are not permitted to log in.' in response.data)

        with self.app.app_context():
            user = self.user_get(uname)
            user.set_state_enabled()
            self.user_save(user)

        with self.app.app_context():
            user = self.user_get(uname)
            user_dict = user.to_dict()
            del user_dict['createtime']
            del user_dict['password']
        response = self.login_dev(uname)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

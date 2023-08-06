#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit test utilities for :py:mod:`vial.blueprints.users`.
"""


class UsersTestCaseMixin:
    """Mixin class with unit test framework for testing user account management endpoints."""

    def _attempt_fail_list(self):
        """Check access to ``users.list`` endpoint and fail."""
        self.assertGetURL(
            '/users/list',
            403
        )

    def _attempt_succeed_list(self, content_checks = None):
        """Check access to ``users.list`` endpoint and succeed."""
        if content_checks is None:
            content_checks = [
                b'Show details of user account &quot;user&quot;',
                b'Show details of user account &quot;developer&quot;',
                b'Show details of user account &quot;maintainer&quot;',
                b'Show details of user account &quot;admin&quot;'
            ]
        self.assertGetURL(
            '/users/list',
            200,
            content_checks
        )

    def _attempt_fail_show(self, uname):
        """Check access to ``users.show`` endpoint and fail."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/show'.format(uid),
            403
        )

    def _attempt_succeed_show(self, uname):
        """Check access to ``users.show`` endpoint and succeed."""
        with self.app.app_context():
            uobj   = self.user_get(uname)
            uid    = uobj.id
            ufname = uobj.fullname
        self.assertGetURL(
            '/users/{}/show'.format(uid),
            200,
            [
                '<h3>{} ({})</h3>'.format(ufname, uname).encode('utf8'),
                b'<strong>Account created:</strong>'
            ]
        )

    def _attempt_fail_create(self):
        """Check access to ``users.create`` endpoint and fail."""
        self.assertGetURL(
            '/users/create',
            403
        )

    def _attempt_succeed_create(self, data):
        """Check access to ``users.create`` endpoint and succeed."""
        self.assertCreate(
            self.user_model(),
            '/users/create',
            data,
            [
                'User account <strong>{}</strong> was successfully created.'.format(data[0][1]).encode('utf8')
            ]
        )
        self._attempt_succeed_show(
            data[0][1]
        )
        self._attempt_succeed_list(
            [
                'Show details of user account &quot;{}&quot;'.format(data[0][1]).encode('utf8')
            ]
        )

    def _attempt_fail_update(self, uname):
        """Check access to ``users.update`` endpoint and fail."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/update'.format(uid),
            403
        )

    def _attempt_succeed_update(self, uname):
        """Check access to ``users.update`` endpoint and succeed."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/update'.format(uid),
            200,
            [
                b'Update user account details'
            ]
        )

    def _attempt_fail_enable(self, uname):
        """Check access to ``users.enable`` endpoint and fail."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/enable'.format(uid),
            403
        )

    def _attempt_succeed_enable(self, uname):
        """Check access to ``users.enable`` endpoint and succeed."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.mailbox_monitoring('on')
        self.assertGetURL(
            '/users/{}/enable'.format(uid),
            200,
            [
                b'Are you really sure you want to enable following item:'
            ]
        )
        self.assertPostURL(
            '/users/{}/enable'.format(uid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully enabled.'
            ]
        )
        self.assertMailbox(
            {
                'subject': [
                    '[{}] Account activation - {}'.format(self.app.config['APPLICATION_NAME'], uname)
                ],
                'sender': [
                    'root@unittest'
                ],
                'recipients': [
                    ['{}@bogus-domain.org'.format(uname)]
                ],
                'cc': [[]],
                'bcc': [['admin@unittest']]
            }
        )
        self.mailbox_monitoring('off')
        self.mailbox_clear()

    def _attempt_fail_disable(self, uname):
        """Check access to ``users.disable`` endpoint and fail."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/disable'.format(uid),
            403
        )

    def _attempt_succeed_disable(self, uname):
        """Check access to ``users.disable`` endpoint and succeed."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/disable'.format(uid),
            200,
            [
                b'Are you really sure you want to disable following item:'
            ]
        )
        self.assertPostURL(
            '/users/{}/disable'.format(uid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully disabled.'
            ]
        )

    def _attempt_fail_delete(self, uname):
        """Check access to ``users.delete`` endpoint and fail."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/delete'.format(uid),
            403
        )

    def _attempt_succeed_delete(self, uname):
        """Check access to ``users.delete`` endpoint and succeed."""
        uid = self.user_id(uname, with_app_ctx = True)
        self.assertGetURL(
            '/users/{}/delete'.format(uid),
            200,
            [
                b'Are you really sure you want to permanently remove following item:'
            ]
        )
        self.assertPostURL(
            '/users/{}/delete'.format(uid),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully and permanently deleted.'
            ]
        )

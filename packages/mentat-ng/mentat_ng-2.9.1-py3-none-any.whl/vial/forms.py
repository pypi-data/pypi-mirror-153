#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains usefull form related classes for *Vial* application views.
"""


import datetime
import urllib.parse
import pytz
import wtforms
import ipranges

import flask
import flask_wtf
from flask_babel import gettext, lazy_gettext

import vial.const


def default_dt_with_delta(delta = 7):
    """
    Create default timestamp for datetime form values with given time delta in days
    and adjust the result to whole hours.
    """
    return datetime.datetime.utcnow().replace(
        minute = 0, second = 0, microsecond = 0
    ) - datetime.timedelta(days = delta)

def default_dt():
    """
    Create default timestamp for datetime form values with given time delta in days
    and adjust the result to whole hours.
    """
    return datetime.datetime.utcnow().replace(
        minute = 0, second = 0, microsecond = 0
    )

def str_to_bool(value):
    """
    Convert given string value to boolean.
    """
    if str(value).lower() == 'true':
        return True
    if str(value).lower() == 'false':
        return False
    raise ValueError('Invalid string value {} to be converted to boolean'.format(str(value)))


def str_to_bool_with_none(value):
    """
    Convert given string value to boolean or ``None``.
    """
    if str(value).lower() == 'true':
        return True
    if str(value).lower() == 'false':
        return False
    if str(value).lower() == 'none':
        return None
    if  str(value).lower() == '':
        return ''
    raise ValueError('Invalid string value {} to be converted to boolean'.format(str(value)))


def str_to_int_with_none(value):
    """
    Convert given string value to boolean or ``None``.
    """
    if str(value).lower() == 'none':
        return None
    try:
        return int(value)
    except:
        raise ValueError('Invalid string value {} to be converted to integer'.format(str(value)))


#-------------------------------------------------------------------------------


def _is_safe_url(target):
    """
    Check, if the URL is safe enough to be redirected to.
    """
    ref_url  = urllib.parse.urlparse(flask.request.host_url)
    test_url = urllib.parse.urlparse(urllib.parse.urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def _is_same_path(first, second):
    """
    Check, if both URL point to same path.
    """
    first_url  = urllib.parse.urlparse(first)
    second_url = urllib.parse.urlparse(second)
    return first_url.path == second_url.path

def get_redirect_target(target_url = None, default_url = None, exclude_url = None):
    """
    Get redirection target, either from GET request variable, or from referrer header.
    """
    options = (
        target_url,
        flask.request.form.get('next'),
        flask.request.args.get('next'),
        flask.request.referrer,
        default_url,
        flask.url_for(
            flask.current_app.config['ENDPOINT_HOME']
        )
    )
    for target in options:
        if not target:
            continue
        if _is_same_path(target, flask.request.base_url):
            continue
        if exclude_url and _is_same_path(target, exclude_url):
            continue
        if _is_safe_url(target):
            return target
    raise RuntimeError("Unable to choose apropriate redirection target.")


#-------------------------------------------------------------------------------

def check_login(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating user account logins (usernames).
    """
    if vial.const.CRE_LOGIN.match(field.data):
        return
    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid login name.',
            val = str(field.data)
        )
    )

def check_email(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating user emails or account logins (usernames).
    """
    if vial.const.CRE_EMAIL.match(field.data):
        return
    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid email address.',
            val = str(field.data)
        )
    )

def check_unique_login(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating of uniqueness of user login.
    """
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    user = vial.db.db_session().query(user_model).filter_by(login = field.data).first()
    if user is not None:
        raise wtforms.validators.ValidationError(
            gettext(
                'Please use different login, the "%(val)s" is already taken.',
                val = str(field.data)
            )
        )

def check_unique_group(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating of uniqueness of group name.
    """
    group_model = flask.current_app.get_model(vial.const.MODEL_GROUP)
    group = vial.db.db_session().query(group_model).filter_by(name = field.data).first()
    if group is not None:
        raise wtforms.validators.ValidationError(
            gettext(
                'Please use different group name, the "%(val)s" is already taken.',
                val = str(field.data)
            )
        )

def check_email_list(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating list of strings.
    """
    for data in field.data:
        if vial.const.CRE_EMAIL.match(data):
            continue
        raise wtforms.validators.ValidationError(
            gettext(
                'The "%(val)s" value does not look like valid email adress.',
                val = str(data)
            )
        )

def check_ip_record(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating IP addresses.
    """
    # Valid value is a single IPv(4|6) address:
    for tconv in ipranges.IP4, ipranges.IP6:
        try:
            tconv(field.data)
            return
        except ValueError:
            pass

    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid IPv4/IPv6 address.',
            val = str(field.data)
        )
    )

def check_ip4_record(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating IP4 addresses.
    """
    # Valid value is a single IP4 address:
    for tconv in (ipranges.IP4,):
        try:
            tconv(field.data)
            return
        except ValueError:
            pass

    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid IPv4 address.',
            val = str(field.data)
        )
    )

def check_ip6_record(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating IP6 addresses.
    """
    # Valid value is a single IP6 address:
    for tconv in (ipranges.IP6,):
        try:
            tconv(field.data)
            return
        except ValueError:
            pass

    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid IPv6 address.',
            val = str(field.data)
        )
    )

def check_network_record(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating network records.
    """
    # Valid value is an IPv(4|6) address/range/network:
    try:
        ipranges.from_str(field.data)
        return
    except ValueError:
        pass

    raise wtforms.validators.ValidationError(
        gettext(
            'The "%(val)s" value does not look like valid IPv4/IPv6 address/range/network.',
            val = str(field.data)
        )
    )

def check_network_record_list(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating list of network records.
    """
    for value in field.data:
        try:
            ipranges.from_str(value)
        except ValueError:
            raise wtforms.validators.ValidationError(
                gettext(
                    'The "%(val)s" value does not look like valid IPv4/IPv6 address/range/network.',
                    val = str(value)
                )
            )

def check_port_list(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating list of ports.
    """
    for data in field.data:
        try:
            if int(data) < 0 or int(data) > 65535:
                raise wtforms.validators.ValidationError(
                    gettext(
                        'The "%(val)s" value does not look like valid port number.',
                        val = str(data)
                    )
                )
        except ValueError:
            raise wtforms.validators.ValidationError(
                gettext(
                    'The "%(val)s" value does not look like valid port number.',
                    val = str(data)
                )
            )

def check_int_list(form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating list of positive integers.
    """
    for data in field.data:
        try:
            if int(data) < 0:
                raise wtforms.validators.ValidationError(
                    gettext(
                        'The "%(val)s" value does not look like valid positive integer.',
                        val = str(data)
                    )
                )
        except ValueError:
            raise wtforms.validators.ValidationError(
                gettext(
                    'The "%(val)s" value does not look like valid positive integer.',
                    val = str(data)
                )
            )


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    group_model = flask.current_app.get_model(vial.const.MODEL_GROUP)
    return vial.db.db_query(group_model).\
        order_by(group_model.name).\
        all()

def get_available_users():
    """
    Query the database for list of users.
    """
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    return vial.db.db_query(user_model).\
        order_by(user_model.fullname).\
        all()

def get_available_group_sources():
    """
    Query the database for list of network record sources.
    """
    group_model = flask.current_app.get_model(vial.const.MODEL_GROUP)
    result = vial.db.db_query(group_model)\
        .distinct(group_model.source)\
        .order_by(group_model.source)\
        .all()
    return [x.source for x in result]

#-------------------------------------------------------------------------------


class CommaListField(wtforms.Field):
    """
    Custom widget representing list of strings as comma separated list.
    """
    widget = wtforms.widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        return u''

    def process_formdata(self, valuelist):
        self.data = []  # pylint: disable=locally-disabled,attribute-defined-outside-init
        if valuelist:
            for val in valuelist[0].split(','):
                if val == '':
                    continue
                self.data.append(val.strip())
            self.data = list(self._remove_duplicates(self.data))  # pylint: disable=locally-disabled,attribute-defined-outside-init

    @classmethod
    def _remove_duplicates(cls, seq):
        """
        Remove duplicates in a case insensitive, but case preserving manner.
        """
        tmpd = {}
        for item in seq:
            if item.lower() not in tmpd:
                tmpd[item.lower()] = True
                yield item


class DateTimeLocalField(wtforms.DateTimeField):
    """
    DateTimeField that assumes input is in app-configured timezone and converts
    to UTC for further processing/storage.
    """
    def process_data(self, value):
        """
        Process the Python data applied to this field and store the result.
        This will be called during form construction by the form's `kwargs` or
        `obj` argument.
        :param value: The python object containing the value to process.
        """
        localtz = pytz.timezone(flask.session['timezone'])
        if value:
            dt_utc = pytz.utc.localize(value, is_dst = None)
            self.data = dt_utc.astimezone(localtz)  # pylint: disable=locally-disabled,attribute-defined-outside-init
        else:
            self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init

    def process_formdata(self, valuelist):
        """
        Process data received over the wire from a form.
        This will be called during form construction with data supplied
        through the `formdata` argument.
        :param valuelist: A list of strings to process.
        """
        localtz = pytz.timezone(flask.session['timezone'])
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                dt_naive  = datetime.datetime.strptime(date_str, self.format)
                dt_local  = localtz.localize(dt_naive, is_dst = None)
                self.data = dt_local.astimezone(pytz.utc)  # pylint: disable=locally-disabled,attribute-defined-outside-init
            except ValueError:
                self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init
                raise ValueError(self.gettext('Not a valid datetime value'))


class SmartDateTimeField(wtforms.Field):
    """
    DateTimeField that assumes input is in app-configured timezone and converts
    to UTC for further processing/storage. This widget allows multiple datetime
    representations on input and is smart to recognize ISO formated timestamp in
    UTC on input, which greatly simplifies generating URLs from within the
    application.
    """
    widget = wtforms.widgets.TextInput()
    utcisoformat = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, label = None, validators = None, formats = None, **kwargs):
        super(SmartDateTimeField, self).__init__(label, validators, **kwargs)
        if formats is None:
            self.formats = [
                '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'
            ]
        else:
            self.formats = formats
        self.format = self.formats[0]

    def _value(self):
        """
        This method is called when rendering the widget to determine the value to
        display to the user within the widget.
        """
        if self.data:
            localtz = pytz.timezone(flask.session['timezone'])
            return localtz.normalize(
                self.data.astimezone(localtz)
            ).strftime(self.format)
        return ''

    def process_data(self, value):
        """
        Process the Python data applied to this field and store the result.
        This will be called during form construction by the form's `kwargs` or
        `obj` argument.
        :param value: The python object containing the value to process.
        """
        if value:
            self.data = pytz.utc.localize(value, is_dst = None)  # pylint: disable=locally-disabled,attribute-defined-outside-init
        else:
            self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init

    def process_formdata(self, valuelist):
        """
        Process data received over the wire from a form.
        This will be called during form construction with data supplied
        through the `formdata` argument.
        :param valuelist: A list of strings to process.
        """
        localtz = pytz.timezone(flask.session['timezone'])
        if valuelist:
            date_str = ' '.join(valuelist)
            # Try all explicitly defined valid datetime formats.
            for fmt in self.formats:
                try:
                    dt_naive  = datetime.datetime.strptime(date_str, fmt)
                    dt_local  = localtz.localize(dt_naive, is_dst = None)
                    self.data = dt_local.astimezone(pytz.utc)  # pylint: disable=locally-disabled,attribute-defined-outside-init
                    self.format = fmt
                    print("Received datetime value in format {}, naive: {}, local: {}, utc: {}".format(
                        fmt,
                        dt_naive.isoformat(),
                        dt_local.isoformat(),
                        self.data.isoformat(),
                    ))
                except ValueError:
                    self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init
                else:
                    break
            # In case of failure try UTC ISO format (YYYY-MM-DDTHH:MM:SSZ).
            if self.data is None:
                try:
                    dt_naive  = datetime.datetime.strptime(date_str, self.utcisoformat)
                    self.data = pytz.utc.localize(dt_naive, is_dst = None)  # pylint: disable=locally-disabled,attribute-defined-outside-init
                    print("Received UTC ISO datetime value, naive: {}, utc: {}".format(
                        dt_naive.isoformat(),
                        self.data.isoformat(),
                    ))
                except ValueError:
                    self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init
            if self.data is None:
                raise ValueError(
                    self.gettext('Value did not match any of datetime formats.')
                )


class RadioFieldWithNone(wtforms.RadioField):
    """
    RadioField that accepts None as valid choice.
    """
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0]) if valuelist[0] != 'None' else None  # pylint: disable=locally-disabled,attribute-defined-outside-init
            except ValueError:
                raise ValueError(self.gettext("Invalid Choice: could not coerce"))

    def pre_validate(self, form):
        for val, _ in self.choices:
            if self.data == val:
                break
        else:
            raise ValueError(self.gettext("Not a valid choice"))


class SelectFieldWithNone(wtforms.SelectField):
    """
    SelectField that accepts None as valid choice.
    """
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0]) if valuelist[0].lower() != 'none' else None  # pylint: disable=locally-disabled,attribute-defined-outside-init
            except ValueError:
                raise ValueError(self.gettext("Invalid Choice: could not coerce"))
        else:
            self.data = None  # pylint: disable=locally-disabled,attribute-defined-outside-init

    def pre_validate(self, form):
        for val, _ in self.choices:
            if self.data == val:
                break
        else:
            raise ValueError(self.gettext("Not a valid choice"))


class BaseItemForm(flask_wtf.FlaskForm):
    """
    Class representing generic item action (create/update/delete) form for Vial
    application.

    This form contains support for redirection back to original page.
    """
    next = wtforms.HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the redirection URL.
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    @staticmethod
    def is_multivalue(field_name):  # pylint: disable=locally-disabled,unused-argument
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False


class ItemActionConfirmForm(BaseItemForm):
    """
    Class representing generic item action confirmation form for Vial application.

    This form contains nothing else but two buttons, one for confirmation, one for
    canceling the delete action. Actual item identifier is passed as part of the URL.
    """
    submit = wtforms.SubmitField(
        lazy_gettext('Confirm')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )


class BaseSearchForm(flask_wtf.FlaskForm):
    """
    Class representing generic item search form for Vial application.

    This form contains support for result limiting and paging.
    """
    limit = wtforms.SelectField(
        lazy_gettext('Pager limit:'),
        validators = [
            wtforms.validators.Optional()
        ],
        filters = [int],
        choices = vial.const.PAGER_LIMIT_CHOICES,
        default = vial.const.DEFAULT_PAGER_LIMIT
    )
    page = wtforms.IntegerField(
        lazy_gettext('Page number:'),
        validators = [
            wtforms.validators.Optional(),
            wtforms.validators.NumberRange(min=1)
        ],
        filters = [int],
        default = 1
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )

    @staticmethod
    def is_multivalue(field_name):  # pylint: disable=locally-disabled,unused-argument
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False

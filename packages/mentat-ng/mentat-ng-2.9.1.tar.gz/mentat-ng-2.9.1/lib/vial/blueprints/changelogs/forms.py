#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom item changelog search form for Hawat.
"""


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
import flask
import flask_wtf
from flask_babel import lazy_gettext

import vial.const
import vial.forms
import vial.db


def get_item_operation_choices():
    """
    Return select choices for item changelog operations.
    """
    item_changelog_model = flask.current_app.get_model(vial.const.MODEL_ITEM_CHANGELOG)
    operations_list = vial.db.db_query(item_changelog_model).\
        distinct(item_changelog_model.operation).\
        all()
    return list(
        zip(
            [x.operation for x in operations_list],
            [lazy_gettext(x.operation) for x in operations_list]
        )
    )

def get_item_model_choices():
    """
    Return select choices for item changelog item models.
    """
    item_changelog_model = flask.current_app.get_model(vial.const.MODEL_ITEM_CHANGELOG)
    models_list = vial.db.db_query(item_changelog_model).\
        distinct(item_changelog_model.model).\
        all()
    return list(
        zip(
            [x.model for x in models_list],
            [lazy_gettext(x.model) for x in models_list]
        )
    )

class ItemChangeLogSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing item changelog search form.
    """
    authors = QuerySelectMultipleField(
        lazy_gettext('Authors:'),
        query_factory = vial.forms.get_available_users,
        get_label = lambda x: '{} ({})'.format(x.fullname, x.login)
    )
    operations = wtforms.SelectMultipleField(
        lazy_gettext('Operations:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        filters = [lambda x: x or []]
    )
    imodel = wtforms.SelectField(
        lazy_gettext('Item model:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [('', lazy_gettext('Nothing selected'))],
        filters = [lambda x: x or None],
        default = ''
    )
    imodel_id = wtforms.IntegerField(
        lazy_gettext('Model ID:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = lambda: vial.forms.default_dt_with_delta(vial.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operations.choices = get_item_operation_choices()
        self.imodel.choices[1:] = get_item_model_choices()

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        if field_name in ('authors', 'operations'):
            return True
        return False


class ItemChangeLogDashboardForm(flask_wtf.FlaskForm):
    """
    Class representing item changelog dashboard search form.
    """
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = lambda: vial.forms.default_dt_with_delta(vial.const.DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Calculate')
    )

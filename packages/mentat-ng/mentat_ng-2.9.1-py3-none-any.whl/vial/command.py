#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom commands for ``vial-cli`` command line interface.
"""


__author__ = "Honza Mach <honza.mach.ml@gmail.com>"


import re
import sys
import traceback
import functools
import sqlalchemy

import click
import flask
from flask.cli import AppGroup

import vial.const
import vial.db


def account_exists(func):
    """
    Decorator: Catch SQLAlchemy exceptions for non existing user accounts.
    """
    @functools.wraps(func)
    def wrapper_account_exists(login, *args, **kwargs):
        try:
            return func(login, *args, **kwargs)
        except sqlalchemy.orm.exc.NoResultFound:
            click.secho(
                "[FAIL] User account '{}' was not found.".format(login),
                fg = 'red'
            )

        except Exception:  # pylint: disable=locally-disabled,broad-except
            vial.db.db_session().rollback()
            click.echo(
                traceback.TracebackException(*sys.exc_info())
            )
    return wrapper_account_exists


def validate_email(ctx, param, value):
    """Validate ``login/email`` command line parameter."""
    if value:
        if vial.const.CRE_EMAIL.match(value):
            return value
        raise click.BadParameter(
            "Value '{}' does not look like valid email address.".format(value)
        )

def validate_roles(ctx, param, value):
    """Validate ``role`` command line parameter."""
    if value:
        for val in value:
            if val not in vial.const.ROLES:
                raise click.BadParameter(
                    "Value '{}' does not look like valid user role.".format(val)
                )
        return value


user_cli = AppGroup('users', help = "User account management module.")

@user_cli.command('create')
@click.argument('login', callback = validate_email)
@click.argument('fullname')
@click.option('--email', callback = validate_email, help = 'Optional email, login will be used as default')
@click.password_option()
@click.option('--enabled/--no-enabled', default = False)
@click.option('--role', callback = validate_roles, help = 'Role to be assigned to the user (multiple)', multiple = True)
def users_create(login, fullname, email, password, enabled, role):
    """Create new user account."""
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    sqlobj = user_model()

    sqlobj.login    = login
    sqlobj.fullname = fullname
    sqlobj.email    = email or login
    sqlobj.roles    = role or [vial.const.ROLE_USER]
    sqlobj.enabled  = enabled
    if password:
        sqlobj.set_password(password)

    click.echo("Creating new user account:")
    click.echo("    - Login:     {}".format(sqlobj.login))
    click.echo("    - Full name: {}".format(sqlobj.fullname))
    click.echo("    - Email:     {}".format(sqlobj.email))
    click.echo("    - Roles:     {}".format(','.join(sqlobj.roles)))
    click.echo("    - Enabled:   {}".format(sqlobj.enabled))
    click.echo("    - Password:  {}".format(sqlobj.password))
    try:
        vial.db.db_session().add(sqlobj)
        vial.db.db_session().commit()
        click.secho(
            "[OK] User account was successfully created",
            fg = 'green'
        )

    except sqlalchemy.exc.IntegrityError as exc:
        vial.db.db_session().rollback()
        match = re.search(r'Key \((\w+)\)=\(([^)]+)\) already exists.', str(exc))
        if match:
            click.secho(
                "[FAIL] User account with {} '{}' already exists.".format(
                    match.group(1),
                    match.group(2)
                ),
                fg = 'red'
            )
        else:
            click.secho(
                "[FAIL] There already is an user account with similar data.",
                fg = 'red'
            )
            click.secho(
                "\n{}".format(exc),
                fg = 'blue'
            )

    except Exception:  # pylint: disable=locally-disabled,broad-except
        vial.db.db_session().rollback()
        click.echo(
            traceback.TracebackException(*sys.exc_info())
        )

@user_cli.command('passwd')
@click.argument('login', callback = validate_email)
@click.password_option()
@account_exists
def users_passwd(login, password):
    """Change/set password to given user account."""
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    if password:
        click.echo("Setting password for user account '{}'".format(login))
        item.set_password(password)
        vial.db.db_session().add(item)
        vial.db.db_session().commit()
        click.secho(
            "[OK] User account was successfully updated",
            fg = 'green'
        )


@user_cli.command('roleadd')
@click.argument('login', callback = validate_email)
@click.argument('role', callback = validate_roles, nargs = -1)
@account_exists
def users_roleadd(login, role):
    """Add role(s) to given user account."""
    if not role:
        return
    click.echo("Adding roles '{}' to user account '{}'".format(','.join(role), login))
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    current_roles = set(item.roles)
    for i in role:
        current_roles.add(i)
    item.roles = list(current_roles)

    vial.db.db_session().add(item)
    vial.db.db_session().commit()
    click.secho(
        "[OK] User account was successfully updated",
        fg = 'green'
    )

@user_cli.command('roledel')
@click.argument('login', callback = validate_email)
@click.argument('role', callback = validate_roles, nargs = -1)
@account_exists
def users_roledel(login, role):
    """Delete role(s) to given user account."""
    click.echo("Deleting roles '{}' from user account '{}'".format(','.join(role), login))
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    current_roles = set(item.roles)
    for i in role:
        try:
            current_roles.remove(i)
        except KeyError:
            pass
    item.roles = list(current_roles)

    vial.db.db_session().add(item)
    vial.db.db_session().commit()
    click.secho(
        "[OK] User account was successfully updated",
        fg = 'green'
    )

@user_cli.command('enable')
@click.argument('login', callback = validate_email)
@account_exists
def users_enable(login):
    """Enable given user account."""
    click.echo("Enabling user account '{}'".format(login))
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    if not item.enabled:
        item.enabled = True

        vial.db.db_session().add(item)
        vial.db.db_session().commit()
        click.secho(
            "[OK] User account was successfully enabled",
            fg = 'green'
        )
    else:
        click.secho(
            "[OK] User account was already enabled",
            fg = 'green'
        )

@user_cli.command('disable')
@click.argument('login', callback = validate_email)
@account_exists
def users_disable(login):
    """Disable given user account."""
    click.echo("Disabling user account '{}'".format(login))
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    if item.enabled:
        item.enabled = False

        vial.db.db_session().add(item)
        vial.db.db_session().commit()
        click.secho(
            "[OK] User account was successfully disabled",
            fg = 'green'
        )
    else:
        click.secho(
            "[OK] User account was already disabled",
            fg = 'green'
        )

@user_cli.command('delete')
@click.argument('login', callback = validate_email)
@account_exists
def users_delete(login):
    """Delete existing user account."""
    click.echo("Deleting user account '{}'".format(login))
    user_model = flask.current_app.get_model(vial.const.MODEL_USER)
    item = vial.db.db_session().query(
        user_model
    ).filter(
        user_model.login == login
    ).one()

    vial.db.db_session().delete(item)
    vial.db.db_session().commit()
    click.secho(
        "[OK] User account was successfully deleted",
        fg = 'green'
    )

@user_cli.command('list')
def users_list():
    """List all available user accounts."""
    try:
        user_model = flask.current_app.get_model(vial.const.MODEL_USER)
        items = vial.db.db_session().query(user_model).all()
        if items:
            click.echo("List of existing user accounts:")
            for item in items:
                click.echo("    - {}: {} ({})".format(item.login, item.fullname, ','.join(item.roles)))
        else:
            click.echo("There are currently no user accounts in the database.")

    except Exception:  # pylint: disable=locally-disabled,broad-except
        vial.db.db_session().rollback()
        click.echo(
            traceback.TracebackException(*sys.exc_info())
        )


#-------------------------------------------------------------------------------


def setup_cli(app):
    """
    Setup custom application CLI commands.
    """
    app.cli.add_command(user_cli)

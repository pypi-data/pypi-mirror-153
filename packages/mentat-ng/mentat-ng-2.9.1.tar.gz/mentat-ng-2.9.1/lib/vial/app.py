#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains extended :py:class:`flask.Flask` and :py:class:`flask.Blueprint`
classes that form the new base of *Vial* application.
"""


import sys
import traceback
import datetime
import weakref
import json
import jinja2

import werkzeug.routing
import werkzeug.utils
import flask
import flask.app
import flask.views
import flask_babel
import flask_migrate
import flask_login
import flask_principal

import vial.const
import vial.acl
import vial.log
import vial.mailer
import vial.intl
import vial.errors
import vial.utils
import vial.jsglue
import vial.view
import vial.menu
import vial.command


class VialException(Exception):
    """
    Custom class for :py:class:`vial.app.Vial` application exceptions.
    """


class Vial(flask.Flask):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Custom implementation of :py:class:`flask.Flask` class. This class extends the
    capabilities of the base class with following additional features:

    Configuration based blueprint registration
        The application configuration file contains a directive describing list
        of requested blueprints/modules, that should be registered into the
        application. This enables administrator to very easily fine tune the
        application setup for each installation. See the :py:func:`vial.app.Vial.register_blueprints`
        for more information on the topic.

    Application main menu management
        The application provides three distinct menus, that are at a disposal for
        blueprint/module designer.
    """

    def __init__(self, import_name, **kwargs):
        super().__init__(import_name, **kwargs)

        self.csrf = None

        self.mailer = None

        self.menu_main = vial.menu.Menu()
        self.menu_auth = vial.menu.Menu()
        self.menu_anon = vial.menu.Menu()

        self.sign_ins    = {}
        self.sign_ups    = {}
        self.resources   = {}
        self.infomailers = {}

    @property
    def icons(self):
        """
        Application icon registry.
        """
        return self.config.get('ICONS')

    @flask.app.setupmethod
    def add_url_rule(self, rule, endpoint = None, view_func = None, provide_automatic_options = None, **options):
        """
        Reimplementation of :py:func:`flask.Flask.add_url_rule` method. This method
        is capable of disabling selected application endpoints. Keep in mind, that
        some URL rules (like application global 'static' endpoint) are created during
        the :py:func:`flask.app.Flask.__init__` method and cannot be disabled,
        because at that point the configuration of the application is not yet loaded.
        """
        if self.config.get('DISABLED_ENDPOINTS', None) and self.config['DISABLED_ENDPOINTS'] and endpoint:
            if endpoint in self.config['DISABLED_ENDPOINTS']:
                self.logger.warning(  # pylint: disable=locally-disabled,no-member
                    "Application endpoint '%s' is disabled by configuration.",
                    endpoint
                )
                return
        #self.logger.debug(  # pylint: disable=locally-disabled,no-member
        #    "Registering URL route %s:%s:%s:%s",
        #    str(rule),
        #    str(endpoint),
        #    str(view_func),
        #    str(view_func.view_class) if hasattr(view_func, 'view_class') else '---none---',
        #)
        super().add_url_rule(rule, endpoint, view_func, provide_automatic_options, **options)

    def register_blueprint(self, blueprint, **options):
        """
        Reimplementation of :py:func:`flask.Flask.register_blueprint` method. This
        method will perform standart blueprint registration and on top of that will
        perform following additional tasks:

            * Register blueprint into custom internal registry. The registry lies
              within application`s ``config`` under key :py:const:`vial.const.CFGKEY_ENABLED_BLUEPRINTS`.
            * Call blueprint`s ``register_app`` method, if available, with ``self`` as only argument.

        :param vial.app.VialBlueprint blueprint: Blueprint to be registered.
        :param dict options: Additional options, will be passed down to :py:func:`flask.Flask.register_blueprint`.
        """
        super().register_blueprint(blueprint, **options)

        if isinstance(blueprint, VialBlueprint):
            if hasattr(blueprint, 'register_app'):
                blueprint.register_app(self)

            self.sign_ins.update(blueprint.sign_ins)
            self.sign_ups.update(blueprint.sign_ups)

    def register_blueprints(self):
        """
        Register all configured application blueprints. The configuration comes
        from :py:const:`vial.const.CFGKEY_ENABLED_BLUEPRINTS` configuration
        subkey, which must contain list of string names of required blueprints.
        The blueprint module must provide ``get_blueprint`` factory method, that
        must return valid instance of :py:class:`vial.app.VialBlueprint`. This
        method will call the :py:func:`vial.app.Vial.register_blueprint` for
        each blueprint, that is being registered into the application.

        :raises vial.app.VialException: In case the factory method ``get_blueprint`` is not provided by loaded module.
        """
        for name in self.config[vial.const.CFGKEY_ENABLED_BLUEPRINTS]:
            self.logger.debug(  # pylint: disable=locally-disabled,no-member
                "Loading pluggable module %s",
                name
            )
            mod = werkzeug.utils.import_string(name)
            if hasattr(mod, 'get_blueprint'):
                self.register_blueprint(mod.get_blueprint())
            else:
                raise VialException(
                    "Invalid blueprint module '{}', does not provide the 'get_blueprint' factory method.".format(name)
                )

    def log_exception(self, exc_info):
        """
        Reimplementation of :py:func:`flask.Flask.log_exception` method.
        """
        self.logger.error(  # pylint: disable=locally-disabled,no-member
            "Exception on %s [%s]" % (flask.request.full_path, flask.request.method),
            exc_info = exc_info
        )

    def log_exception_with_label(self, tbexc, label = ''):
        """
        Log given exception traceback into application logger.
        """
        self.logger.error(  # pylint: disable=locally-disabled,no-member
            '%s%s',
            label,
            ''.join(tbexc.format())
        )

    #--------------------------------------------------------------------------

    def get_modules(self, filter_func = None):
        """
        Get all currently registered application modules.
        """
        if not filter_func:
            return self.blueprints
        return {
            k: v for k, v in self.blueprints.items() if filter_func(k, v)
        }

    def has_endpoint(self, endpoint):
        """
        Check if given routing endpoint is available.

        :param str endpoint: Application routing endpoint.
        :return: ``True`` in case endpoint exists, ``False`` otherwise.
        :rtype: bool
        """
        return endpoint in self.view_functions

    def get_endpoints(self, filter_func = None):
        """
        Get all currently registered application endpoints.
        """
        if not filter_func:
            return {
                k: v.view_class for k, v in self.view_functions.items() if hasattr(v, 'view_class')
            }
        return {
            k: v.view_class for k, v in self.view_functions.items() if hasattr(v, 'view_class') and filter_func(k, v.view_class)
        }

    def get_endpoint_class(self, endpoint, quiet = False):
        """
        Get reference to view class registered to given routing endpoint.

        :param str endpoint: Application routing endpoint.
        :param bool quiet: Suppress the exception in case given endpoint does not exist.
        :return: Reference to view class.
        :rtype: class
        """
        if not endpoint in self.view_functions:
            if quiet:
                return None
            raise VialException(
                "Unknown endpoint name '{}'.".format(endpoint)
            )
        try:
            return self.view_functions[endpoint].view_class
        except AttributeError:
            return vial.view.DecoratedView(self.view_functions[endpoint])

    def can_access_endpoint(self, endpoint, **kwargs):
        """
        Check, that the current user can access given endpoint/view.

        :param str endpoint: Application routing endpoint.
        :param dict kwargs: Optional endpoint parameters.
        :return: ``True`` in case user can access the endpoint, ``False`` otherwise.
        :rtype: bool
        """
        try:
            view_class = self.get_endpoint_class(endpoint)

            # Reject unauthenticated users in case view requires authentication.
            if view_class.authentication:
                if not flask_login.current_user.is_authenticated:
                    return False

            # Check view authorization rules.
            if view_class.authorization:
                for auth_rule in view_class.authorization:
                    if not auth_rule.can():
                        return False

            # Check item action authorization callback, if exists.
            if hasattr(view_class, 'authorize_item_action'):
                if not view_class.authorize_item_action(**kwargs):
                    return False

            return True

        except VialException:
            return False

    def get_model(self, name):
        """
        Return reference to class of given model.

        :param str name: Name of the model.
        """
        return self.config[vial.const.CFGKEY_MODELS][name]

    def get_resource(self, name):
        """
        Return reference to given registered resource.

        :param str name: Name of the resource.
        """
        return self.resources[name]()

    def set_resource(self, name, resource):
        """
        Store reference to given resource.

        :param str name: Name of the resource.
        :param resource: Resource to be registered.
        """
        self.resources[name] = weakref.ref(resource)

    def set_infomailer(self, name, mailer):
        """
        Register mailer handle to be usable by different web interface components.

        :param str name: Name of the informailer.
        :param callable mailer: Mailer handle.
        """
        self.infomailers.setdefault(name, []).append(mailer)

    def send_infomail(self, name, **kwargs):
        """
        Send emails through all registered infomailer handles.

        :param str name: Name of the informailer.
        :param **kwargs: Additional mailer arguments.
        """
        for mailer in self.infomailers[name]:
            mailer(**kwargs)

    #--------------------------------------------------------------------------

    def setup_app(self):
        """
        Perform setup of the whole application.
        """
        self._setup_app_logging()
        self._setup_app_mailer()
        self._setup_app_core()
        self._setup_app_db()
        self._setup_app_auth()
        self._setup_app_acl()
        self._setup_app_intl()
        self._setup_app_menu()
        self._setup_app_blueprints()
        self._setup_app_cli()

    def _setup_app_logging(self):
        """
        Setup logging to file and via email for given Vial application. Logging
        capabilities are adjustable by application configuration.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        vial.log.setup_logging_default(self)
        vial.log.setup_logging_file(self)
        if not self.debug:
            vial.log.setup_logging_email(self)

        return self

    def _setup_app_mailer(self):
        """
        Setup mailer service for Vial application.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        vial.mailer.MAILER.init_app(self)
        self.mailer = vial.mailer.MAILER

        return self

    def _setup_app_core(self):
        """
        Setup application core for given Vial application. The application core
        contains following features:

            * Error handlers
            * Default routes
            * Additional custom Jinja template variables
            * Additional custom Jinja template macros

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        @self.errorhandler(400)
        def eh_badrequest(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 400 error."""
            flask.current_app.logger.critical(
                "BAD REQUEST\n\nRequest: %s\nTraceback:\n%s",
                flask.request.full_path,
                ''.join(
                    traceback.TracebackException(
                        *sys.exc_info()
                    ).format()
                )
            )
            return vial.errors.error_handler_switch(400, err)

        @self.errorhandler(403)
        def eh_forbidden(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 403 error."""
            return vial.errors.error_handler_switch(403, err)

        @self.errorhandler(404)
        def eh_page_not_found(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 404 error."""
            return vial.errors.error_handler_switch(404, err)

        @self.errorhandler(405)
        def eh_method_not_allowed(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 405 error."""
            return vial.errors.error_handler_switch(405, err)

        @self.errorhandler(410)
        def eh_gone(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 410 error."""
            return vial.errors.error_handler_switch(410, err)

        @self.errorhandler(500)
        def eh_internal_server_error(err):  # pylint: disable=locally-disabled,unused-variable
            """Flask error handler to be called to service HTTP 500 error."""
            flask.current_app.logger.critical(
                "INTERNAL SERVER ERROR\n\nRequest: %s\nTraceback:\n%s",
                flask.request.full_path,
                ''.join(
                    traceback.TracebackException(
                        *sys.exc_info()
                    ).format()
                ),
            )
            return vial.errors.error_handler_switch(500, err)

        @self.before_request
        def before_request():  # pylint: disable=locally-disabled,unused-variable
            """
            Use Flask`s :py:func:`flask.Flask.before_request` hook for performing
            various usefull tasks before each request.
            """
            flask.g.requeststart = datetime.datetime.utcnow()

        @self.context_processor
        def jinja_inject_variables():  # pylint: disable=locally-disabled,unused-variable
            """
            Inject additional variables into Jinja2 global template namespace.
            """
            return dict(
                vial_appname           = flask.current_app.config['APPLICATION_NAME'],
                vial_appid             = flask.current_app.config['APPLICATION_ID'],
                vial_current_app       = flask.current_app,
                vial_current_menu_main = flask.current_app.menu_main,
                vial_current_menu_auth = flask.current_app.menu_auth,
                vial_current_menu_anon = flask.current_app.menu_anon,
                vial_current_view      = self.get_endpoint_class(flask.request.endpoint, True),
                vial_logger            = flask.current_app.logger,
                vial_cdt_utc           = datetime.datetime.utcnow(),
                vial_cdt_local         = datetime.datetime.now(),
            )

        @self.context_processor
        def jinja2_inject_functions():  # pylint: disable=locally-disabled,unused-variable,too-many-locals
            """
            Register additional helpers into Jinja2 global template namespace.
            """
            def get_modules_dict():
                """
                Return dictionary of all registered application pluggable modules.
                """
                return flask.current_app.blueprints

            def get_endpoints_dict():
                """
                Return dictionary of all registered application view endpoints.
                """
                return { k: v.view_class for k, v in flask.current_app.view_functions.items() if hasattr(v, 'view_class') }

            def get_endpoint_class(endpoint, quiet = False):
                """
                Return class reference to given view endpoint.

                :param str endpoint: Name of the view endpoint.
                :param bool quiet: Suppress the exception in case given endpoint does not exist.
                """
                return self.get_endpoint_class(endpoint, quiet)

            def check_endpoint_exists(endpoint):
                """
                Check, that given application view endpoint exists and is registered within
                the application.

                :param str endpoint: Name of the view endpoint.
                :return: ``True`` in case endpoint exists, ``False`` otherwise.
                :rtype: bool
                """
                return endpoint in self.view_functions

            def get_icon(icon_name, default_icon = 'missing-icon'):
                """
                Get HTML icon markup for given icon.

                :param str icon_name: Name of the icon.
                :param str default_icon: Name of the default icon.
                :return: Icon including HTML markup.
                :rtype: flask.Markup
                """
                return flask.Markup(
                    self.config.get('ICONS').get(
                        icon_name,
                        self.config.get('ICONS').get(default_icon)
                    )
                )

            def get_module_icon(endpoint, default_icon = 'missing-icon'):
                """
                Get HTML icon markup for parent module of given view endpoint.

                :param str endpoint: Name of the view endpoint.
                :param str default_icon: Name of the default icon.
                :return: Icon including HTML markup.
                :rtype: flask.Markup
                """
                return flask.Markup(
                    self.config.get('ICONS').get(
                        self.get_endpoint_class(endpoint).module_ref().get_module_icon(),
                        self.config.get('ICONS').get(default_icon)
                    )
                )

            def get_endpoint_icon(endpoint, default_icon = 'missing-icon'):
                """
                Get HTML icon markup for given view endpoint.

                :param str endpoint: Name of the view endpoint.
                :return: Icon including HTML markup.
                :rtype: flask.Markup
                """
                return flask.Markup(
                    self.config.get('ICONS').get(
                        self.get_endpoint_class(endpoint).get_view_icon(),
                        self.config.get('ICONS').get(default_icon)
                    )
                )

            def get_country_flag(country):
                """
                Get URL to static country flag file.

                :param str country: Name of the icon.
                :return: Country including HTML markup.
                :rtype: flask.Markup
                """
                if not vial.const.CRE_COUNTRY_CODE.match(country):
                    return get_icon('flag')

                return flask.Markup(
                    '<img src="{}">'.format(
                        flask.url_for(
                            'static',
                            filename = 'images/country-flags/flags-iso/shiny/16/{}.png'.format(
                                country.upper()
                            )
                        )
                    )
                )

            def include_raw(filename):
                """
                Include given file in raw form directly into the generated content.
                This may be usefull for example for including JavaScript files
                directly into the HTML page.
                """
                return jinja2.Markup(
                    self.jinja_loader.get_source(self.jinja_env, filename)[0]
                )

            return dict(
                get_modules_dict      = get_modules_dict,
                get_endpoints_dict    = get_endpoints_dict,
                get_endpoint_class    = get_endpoint_class,
                check_endpoint_exists = check_endpoint_exists,

                get_icon          = get_icon,
                get_module_icon   = get_module_icon,
                get_endpoint_icon = get_endpoint_icon,
                get_country_flag  = get_country_flag,

                get_timedelta       = vial.utils.get_timedelta,
                get_datetime_utc    = vial.utils.get_datetime_utc,
                get_datetime_local  = vial.utils.get_datetime_local,
                parse_datetime      = vial.utils.parse_datetime,

                get_datetime_window = vial.view.mixin.VialUtils.get_datetime_window,

                check_file_exists = vial.utils.check_file_exists,

                in_query_params       = vial.utils.in_query_params,
                generate_query_params = vial.utils.generate_query_params,

                current_datetime_utc = datetime.datetime.utcnow(),

                include_raw         = include_raw,
                json_to_yaml        = vial.utils.json_to_yaml,
                get_uuid4           = vial.utils.get_uuid4,
                load_json_from_file = vial.utils.load_json_from_file,
                make_copy_deep      = vial.utils.make_copy_deep
            )

        @self.template_filter('tojson_pretty')
        def to_pretty_json(value):
            return json.dumps(
                value,
                sort_keys = True,
                indent = 4
            )

        class VialJSONEncoder(flask.json.JSONEncoder):
            """
            Custom JSON encoder for converting anything into JSON strings.
            """
            def default(self, obj):  # pylint: disable=locally-disabled,method-hidden,arguments-differ
                try:
                    if isinstance(obj, datetime.datetime):
                        return obj.isoformat() + 'Z'
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                try:
                    return obj.to_dict()
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                try:
                    return str(obj)
                except:  # pylint: disable=locally-disabled,bare-except
                    pass
                return flask.json.JSONEncoder.default(self, obj)

        self.json_encoder = VialJSONEncoder

        @self.route('/app-main.js')
        def mainjs():  # pylint: disable=locally-disabled,unused-variable
            """
            Default route for main application JavaScript file.
            """
            return flask.make_response(
                flask.render_template('app-main.js'),
                200,
                {'Content-Type': 'text/javascript'}
            )

        # Initialize JSGlue plugin for using `flask.url_for()` method in JavaScript.
        #jsglue = flask_jsglue.JSGlue()
        jsglue = vial.jsglue.JSGlue()
        jsglue.init_app(self)

        @self.template_filter()
        def pprint_item(item):  # pylint: disable=locally-disabled,unused-variable
            """
            Custom Jinja2 filter for full object attribute dump/pretty-print.
            """
            res = []
            for key in dir(item):
                res.append('%r: %r' % (key, getattr(item, key)))
            return '\n'.join(res)

        return self

    def _setup_app_db(self):
        """
        Setup application database service for given Vial application.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        dbh = vial.db.db_setup(**self.config['SQLALCHEMY_SETUP_ARGS'])
        dbh.init_app(self)

        # Initialize database migration service and register it among the application
        # resources for possible future use.
        migrate = flask_migrate.Migrate(
            app       = self,
            db        = dbh,
            directory = self.config['MIGRATE_DIRECTORY']
        )
        self.set_resource(vial.const.RESOURCE_MIGRATE, migrate)

        self.logger.debug(
            "Connected to database via SQLAlchemy ({})".format(
                self.config['SQLALCHEMY_DATABASE_URI']
            )
        )

        return self


    def _setup_app_auth(self):
        """
        Setup application authentication features.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """

        lim = flask_login.LoginManager()
        lim.init_app(self)
        lim.login_view = self.config['ENDPOINT_LOGIN']
        lim.login_message = flask_babel.gettext("Please log in to access this page.")
        lim.login_message_category = self.config['LOGIN_MSGCAT']

        self.set_resource(vial.const.RESOURCE_LOGIN_MANAGER, lim)

        @lim.user_loader
        def load_user(user_id):  # pylint: disable=locally-disabled,unused-variable
            """
            Flask-Login callback for loading current user`s data.
            """
            user_model = self.get_model(vial.const.MODEL_USER)
            return vial.db.db_get().session.query(user_model).filter(user_model.id == user_id).one_or_none()

        @self.route('/logout')
        @flask_login.login_required
        def logout():  # pylint: disable=locally-disabled,unused-variable
            """
            Flask-Login callback for logging out current user.
            """
            flask.current_app.logger.info(
                "User '{}' just logged out.".format(
                    str(flask_login.current_user)
                )
            )
            flask_login.logout_user()
            flask.flash(
                flask_babel.gettext('You have been successfully logged out.'),
                vial.const.FLASH_SUCCESS
            )

            # Remove session keys set by Flask-Principal.
            for key in ('identity.name', 'identity.auth_type'):
                flask.session.pop(key, None)

            # Tell Flask-Principal the identity changed.
            flask_principal.identity_changed.send(
                flask.current_app._get_current_object(),  # pylint: disable=locally-disabled,protected-access
                identity = flask_principal.AnonymousIdentity()
            )

            # Force user to index page.
            return flask.redirect(
                flask.url_for(
                    flask.current_app.config['ENDPOINT_LOGOUT_REDIRECT']
                )
            )

        return self

    def _setup_app_acl(self):
        """
        Setup application ACL features.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        fpp = flask_principal.Principal(self, skip_static = True)
        self.set_resource(vial.const.RESOURCE_PRINCIPAL, fpp)

        @flask_principal.identity_loaded.connect_via(self)
        def on_identity_loaded(sender, identity):  # pylint: disable=locally-disabled,unused-variable,unused-argument
            """
            Flask-Principal callback for populating user identity object after login.
            """
            # Set the identity user object.
            identity.user = flask_login.current_user

            if not flask_login.current_user.is_authenticated:
                flask.current_app.logger.debug(
                    "Loaded ACL identity for anonymous user '{}'.".format(
                        str(flask_login.current_user)
                    )
                )
                return
            flask.current_app.logger.debug(
                "Loading ACL identity for user '{}'.".format(
                    str(flask_login.current_user)
                )
            )

            # Add the UserNeed to the identity.
            if hasattr(flask_login.current_user, 'get_id'):
                identity.provides.add(
                    flask_principal.UserNeed(flask_login.current_user.id)
                )

            # Assuming the User model has a list of roles, update the
            # identity with the roles that the user provides.
            if hasattr(flask_login.current_user, 'roles'):
                for role in flask_login.current_user.roles:
                    identity.provides.add(
                        flask_principal.RoleNeed(role)
                    )

            # Assuming the User model has a list of group memberships, update the
            # identity with the groups that the user is member of.
            if hasattr(flask_login.current_user, 'memberships'):
                for group in flask_login.current_user.memberships:
                    identity.provides.add(
                        vial.acl.MembershipNeed(group.id)
                    )

            # Assuming the User model has a list of group managements, update the
            # identity with the groups that the user is manager of.
            if hasattr(flask_login.current_user, 'managements'):
                for group in flask_login.current_user.managements:
                    identity.provides.add(
                        vial.acl.ManagementNeed(group.id)
                    )

        @self.context_processor
        def utility_acl_processor():  # pylint: disable=locally-disabled,unused-variable
            """
            Register additional helpers related to authorization into Jinja global
            namespace to enable them within the templates.
            """
            def can_access_endpoint(endpoint, item = None):
                """
                Check if currently logged-in user can access given endpoint/view.

                :param str endpoint: Name of the application endpoint.
                :param item: Optional item for additional validations.
                :return: ``True`` in case user can access the endpoint, ``False`` otherwise.
                :rtype: bool
                """
                return flask.current_app.can_access_endpoint(endpoint, item = item)

            def permission_can(permission_name):
                """
                Manually check currently logged-in user for given permission.

                :param str permission_name: Name of the permission.
                :return: Check result.
                :rtype: bool
                """
                return vial.acl.PERMISSIONS[permission_name].can()

            def is_it_me(item):
                """
                Check if given user account is mine.
                """
                return item.id == flask_login.current_user.id

            return dict(
                can_access_endpoint = can_access_endpoint,
                permission_can      = permission_can,
                is_it_me            = is_it_me
            )

        return self

    def _setup_app_intl(self):
        """
        Setup application`s internationalization sybsystem.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        vial.intl.BABEL.init_app(self)
        self.set_resource(vial.const.RESOURCE_BABEL, vial.intl.BABEL)

        @self.route('/locale/<code>')
        def locale(code):  # pylint: disable=locally-disabled,unused-variable
            """
            Application route providing users with the option of changing locale.
            """
            if code not in flask.current_app.config['SUPPORTED_LOCALES']:
                return flask.abort(404)

            if flask_login.current_user.is_authenticated:
                flask_login.current_user.locale = code
                # Make sure current user is in SQLAlchemy session. Turns out, this
                # step is not necessary and current user is already in session,
                # because it was fetched from database few moments ago.
                #vial.db.db_session().add(flask_login.current_user)
                vial.db.db_session().commit()

            flask.session['locale'] = code
            flask_babel.refresh()

            flask.flash(
                flask.Markup(flask_babel.gettext(
                    'Locale was succesfully changed to <strong>%(lcln)s (%(lclc)s)</strong>.',
                    lclc = code,
                    lcln = flask.current_app.config['SUPPORTED_LOCALES'][code]
                )),
                vial.const.FLASH_SUCCESS
            )

            # Redirect user back to original page.
            return flask.redirect(
                vial.forms.get_redirect_target(
                    default_url = flask.url_for(
                        flask.current_app.config['ENDPOINT_HOME']
                    )
                )
            )

        @self.before_request
        def before_request():  # pylint: disable=locally-disabled,unused-variable
            """
            Use Flask`s :py:func:`flask.Flask.before_request` hook for storing
            currently selected locale and timezone to request`s session storage.
            """
            if 'locale' not in flask.session:
                flask.session['locale'] = vial.intl.get_locale()
            if 'timezone' not in flask.session:
                flask.session['timezone'] = vial.intl.get_timezone()

        @self.context_processor
        def utility_processor():  # pylint: disable=locally-disabled,unused-variable
            """
            Register additional internationalization helpers into Jinja global namespace.
            """

            return dict(
                babel_get_locale         = vial.intl.get_locale,
                babel_get_timezone       = vial.intl.get_timezone,
                babel_format_datetime    = flask_babel.format_datetime,
                babel_format_date        = flask_babel.format_date,
                babel_format_time        = flask_babel.format_time,
                babel_format_timedelta   = flask_babel.format_timedelta,
                babel_format_decimal     = flask_babel.format_decimal,
                babel_format_percent     = flask_babel.format_percent,
                babel_format_bytes       = vial.intl.babel_format_bytes,
                babel_translate_locale   = vial.intl.babel_translate_locale,
                babel_language_in_locale = vial.intl.babel_language_in_locale
            )

        return self

    def _setup_app_menu(self):
        """
        Setup default application menu skeleton.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        for entry in self.config[vial.const.CFGKEY_MENU_MAIN_SKELETON]:
            self.menu_main.add_entry(**entry)

        return self

    def _setup_app_blueprints(self):
        """
        Setup application blueprints.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        self.register_blueprints()

        return self

    def _setup_app_cli(app):
        """
        Setup application command line interface.

        :param vial.app.VialApp app: Vial application to be modified.
        :return: Modified Vial application
        :rtype: vial.app.VialApp
        """
        vial.command.setup_cli(app)

        return app


class VialBlueprint(flask.Blueprint):
    """
    Custom implementation of :py:class:`flask.Blueprint` class. This class extends
    the capabilities of the base class with additional features:

        * Support for better integration into application and registration of view classes.
        * Support for custom tweaking of application object.
        * Support for custom style of authentication and authorization decorators
    """
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        self.sign_ins     = {}
        self.sign_ups     = {}

    @classmethod
    def get_module_title(cls):
        """
        Get human readable name for this blueprint/module.

        :return: Name (short summary) of the blueprint/module.
        :rtype: str
        """
        raise NotImplementedError()

    def get_module_icon(self):
        """
        Return icon name for the module. Given name will be used as index to
        built-in icon registry.

        :return: Icon for the module.
        :rtype: str
        """
        return 'module-{}'.format(self.name).replace('_', '-')

    def register_app(self, app):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        """
        *Hook method:* Custom callback, which will be called from
        :py:func:`vial.app.Vial.register_blueprint` method and which can
        perform additional tweaking of Vial application object.

        :param vial.app.Vial app: Application object.
        """
        return

    def register_view_class(self, view_class, route_spec):
        """
        Register given view class into the internal blueprint registry.

        :param vial.view.BaseView view_class: View class (not instance!)
        :param str route_spec: Routing information for the view.
        """
        view_class.module_ref  = weakref.ref(self)
        view_class.module_name = self.name

        # Obtain view function.
        view_func = view_class.as_view(view_class.get_view_name())

        # Apply authorization decorators (if requested).
        if view_class.authorization:
            for auth in view_class.authorization:
                view_func = auth.require(403)(view_func)

        # Apply authentication decorators (if requested).
        if view_class.authentication:
            view_func = flask_login.login_required(view_func)

        # Register endpoint to the application.
        self.add_url_rule(route_spec, view_func = view_func)

        # Register SIGN IN and SIGN UP views to enable further special handling.
        if hasattr(view_class, 'is_sign_in') and view_class.is_sign_in:
            self.sign_ins[view_class.get_view_endpoint()] = view_class
        if hasattr(view_class, 'is_sign_up') and view_class.is_sign_up:
            self.sign_ups[view_class.get_view_endpoint()] = view_class

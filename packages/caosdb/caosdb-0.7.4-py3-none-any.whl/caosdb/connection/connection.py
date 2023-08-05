# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (c) 2019 Daniel Hornung
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
"""Connection to a CaosDB server."""
from __future__ import absolute_import, print_function, unicode_literals

import logging
import ssl
import sys
from builtins import str  # pylint: disable=redefined-builtin
from errno import EPIPE as BrokenPipe
from socket import error as SocketError

from caosdb.configuration import get_config
from caosdb.exceptions import (CaosDBException, HTTPClientError,
                               ConfigurationError,
                               CaosDBConnectionError,
                               HTTPForbiddenError,
                               LoginFailedError,
                               HTTPResourceNotFoundError,
                               HTTPServerError,
                               HTTPURITooLongError)
try:
    from caosdb.version import version
except ModuleNotFoundError:
    version = "uninstalled"

from pkg_resources import resource_filename

from .interface import CaosDBHTTPResponse, CaosDBServerConnection
from .streaminghttp import StreamingHTTPSConnection
from .utils import make_uri_path, parse_url, urlencode

try:
    from urllib.parse import quote, urlparse
except ImportError:
    from urllib import quote
    from urlparse import urlparse

# pylint: disable=missing-docstring

_LOGGER = logging.getLogger(__name__)


class _WrappedHTTPResponse(CaosDBHTTPResponse):

    def __init__(self, response):
        self.response = response

    @property
    def reason(self):
        return self.response.reason

    @property
    def status(self):
        return self.response.status

    def read(self, size=None):
        return self.response.read(size)

    def getheader(self, name, default=None):
        return self.response.getheader(name=name, default=default)

    def getheaders(self):
        return self.response.getheaders()

    def close(self):
        self.response.close()


class _DefaultCaosDBServerConnection(CaosDBServerConnection):
    """_DefaultCaosDBServerConnection.

    Methods
    -------
    configure
    request
    """

    def __init__(self):
        self._useragent = ("caosdb-pylib/{version} - {implementation}".format(
            version=version, implementation=type(self).__name__))
        self._http_con = None
        self._base_path = None

    def request(self, method, path, headers=None, body=None, **kwargs):
        """request.

        Send a HTTP request to the server.

        Parameters
        ----------
        method : str
            The HTTP request method.
        path : str
            An URI path segment (without the 'scheme://host:port/' parts),
            including query and frament segments.
        headers : dict of str -> str, optional
            HTTP request headers. (Defautl: None)
        body : str or bytes or readable, opional
            The body of the HTTP request. Bytes should be a utf-8 encoded
            string.
        **kwargs :
            Any keyword arguments will be ignored.
            TODO: Why are they allowed then?

        Returns
        -------
            TODO: What?
        """

        if headers is None:
            headers = {}
        headers["User-Agent"] = self._useragent
        try:
            self._http_con = StreamingHTTPSConnection(
                # TODO looks as if configure needs to be done first.
                # That is however not assured.
                host=self.setup_fields["host"],
                timeout=self.setup_fields["timeout"],
                context=self.setup_fields["context"],
                socket_proxy=self.setup_fields["socket_proxy"])
            self._http_con.request(method=method, url=self._base_path + path,
                                   headers=headers, body=body)
        except SocketError as socket_err:
            raise CaosDBConnectionError(
                "Connection failed. Network or server down? " + str(socket_err)
            )

        return _WrappedHTTPResponse(self._http_con.getresponse())

    def configure(self, **config):
        """configure.

        Configure the http connection.

        Parameters
        ----------
        cacert : str
            Path to the CA certificate which will be used to identify the
            server.
        url : str
            The url of the CaosDB Server, e.g.
            `https://example.com:443/rootpath`, including a possible root path.
        **config :
            Any further keyword arguments are being ignored.

        Raises
        ------
        CaosDBConnectionError
            If no url has been specified, or if the CA certificate cannot be
            loaded.
        """

        if "ssl_version" in config and config["cacert"] is not None:
            ssl_version = getattr(ssl, config["ssl_version"])
        else:
            try:
                ssl_version = ssl.PROTOCOL_TLS
            except AttributeError:
                # deprecated since Python 3.6, but necessary until there.
                try:
                    ssl_version = ssl.PROTOCOL_TLSv1_2
                except AttributeError:
                    print("It seems as if your Python version does not support current encryption"
                          "standards (such as TLS > 1.0), please upgrade to at least Python 3.4.")
                    sys.exit(1)
        context = ssl.SSLContext(ssl_version)
        context.verify_mode = ssl.CERT_REQUIRED

        if config.get("ssl_insecure"):
            _LOGGER.warning("*** Warning! ***\n"
                            "Insecure SSL mode, certificate will not be checked! "
                            "Please consider removing the `ssl_insecure` configuration option.\n"
                            "****************")
            context.verify_mode = ssl.CERT_NONE

        if (not context.verify_mode == ssl.CERT_NONE and
                hasattr(context, "check_hostname")):
            context.check_hostname = True

        if ("cacert" in config and config["cacert"] is not None and
                config["cacert"]):
            try:
                context.load_verify_locations(config["cacert"])
            except Exception as exc:
                raise CaosDBConnectionError("Could not load the cacert in"
                                            "`{}`: {}".format(config["cacert"],
                                                              exc))

        context.load_default_certs()

        if "url" in config:
            parsed_url = parse_url(config["url"])
            host = parsed_url.netloc
            self._base_path = parsed_url.path
        else:
            raise CaosDBConnectionError(
                "No connection url specified. Please "
                "do so via caosdb.configure_connection(...) or in a config "
                "file.")

        socket_proxy = None

        if "socket_proxy" in config:
            socket_proxy = config["socket_proxy"]

        self.setup_fields = {
            "host": host,
            "timeout": int(config.get("timeout")),
            "context": context,
            "socket_proxy": socket_proxy}


def _make_conf(*conf):
    """_make_conf.

    Merge several config dicts into one. The precedence goes to latter dicts in
    the function call.

    Parameters
    ----------
    *conf : dict
        One ore more dicts with lower case option names (i.e. keys).

    Returns
    -------
    dict
        A merged config dict.
    """
    result = {}

    for conf_dict in conf:
        result.update(conf_dict)

    return result


_DEFAULT_CONF = {
    "password_method": "input",
    "implementation": _DefaultCaosDBServerConnection,
    "timeout": 210,
    "cacert": resource_filename("caosdb", 'cert/indiscale.ca.crt')
}


def _get_authenticator(**config):
    """_get_authenticator.

    Import and configure the password_method.

    Parameters
    ----------
    password_method : str
        The simple name of a submodule of caosdb.connection.authentication.
        Currently, there are four valid values for this parameter: 'plain',
        'pass', 'keyring' and 'auth_token'.
    **config :
        Any other keyword arguments are passed the configre method of the
        password_method.

    Returns
    -------
    AbstractAuthenticator
        An object which implements the password_method and which already
        configured.

    Raises
    ------
    ConfigurationError
        If the password_method string cannot be resolved to a CaosAuthenticator
        class.
    """
    auth_module = ("caosdb.connection.authentication." +
                   config["password_method"])
    _LOGGER.debug("import auth_module %s", auth_module)
    try:
        __import__(auth_module)

        auth_provider = sys.modules[auth_module].get_authentication_provider()
        auth_provider.configure(**config)

        return auth_provider

    except ImportError:
        raise ConfigurationError("Password method \"{}\" not implemented. "
                                 "Try `plain`, `pass`, `keyring`, or "
                                 "`auth_token`."
                                 .format(config["password_method"]))


def configure_connection(**kwargs):
    """Configures the caosdb connection and returns the Connection object.

    The effective configuration is governed by the default values (see
    'Parameters'), the global configuration (see `caosdb.get_config()`) and the
    parameters which are passed to this function, with ascending priority.

    The parameters which are listed here, are possibly not sufficient for a
    working configuration of the connection. Check the `configure` method of
    the implementation class and the password_method for more details.

    Parameters
    ----------

    username : str
        Username for login; e.g. 'admin'.

    password : str
        Password for login if 'plain' is used as password_method.

    password_method : str
        The name of a submodule of caosdb.connection.authentication which
        implements the AbstractAuthenticator interface. (Default: 'plain')
        Possible values are, for example:
        - "plain"    Need username and password arguments.
        - "input"    Asks for the password.
        - "pass"     Uses the `pass` password manager.
        - "keyring"  Uses the `keyring` library.
        - "auth_token" Uses only a given auth_token.

    timeout : int
        A connection timeout in seconds. (Default: 210)

    ssl_insecure : bool
        Whether SSL certificate warnings should be ignored. Only use this for
        development purposes! (Default: False)

    auth_token : str (optional)
        An authentication token which has been issued by the CaosDB Server.
        Implies `password_method="auth_token"` if set.  An example token string would be `["O","OneTimeAuthenticationToken","anonymous",["administration"],[],1592995200000,604800000,"3ZZ4WKRB-5I7DG2Q6-ZZE6T64P-VQ","197d0d081615c52dc18fb323c300d7be077beaad4020773bb58920b55023fa6ee49355e35754a4277b9ac525c882bcd3a22e7227ba36dfcbbdbf8f15f19d1ee9",1,30000]`.

    implementation : CaosDBServerConnection
        The class which implements the connection. (Default:
        _DefaultCaosDBServerConnection)

    Returns
    -------
    _Connection
        The singleton instance of the _Connection class.
    """
    global_conf = {}
    conf = get_config()
    # Convert config to dict, with preserving types
    int_opts = ["timeout"]
    bool_opts = ["ssl_insecure"]

    if conf.has_section("Connection"):
        global_conf = dict(conf.items("Connection"))
        # Integer options

        for opt in int_opts:
            if opt in global_conf:
                global_conf[opt] = conf.getint("Connection", opt)
        # Boolean options

        for opt in bool_opts:
            if opt in global_conf:
                global_conf[opt] = conf.getboolean("Connection", opt)
    local_conf = _make_conf(_DEFAULT_CONF, global_conf, kwargs)

    connection = _Connection.get_instance()
    connection.configure(**local_conf)

    return connection


def get_connection():
    """Return the connection.

    If the connection was not configured yet `configure_connection` will
    be called inside this function without arguments.
    """
    connection = _Connection.get_instance()

    if connection.is_configured:
        return connection

    return configure_connection()


def _handle_response_status(http_response):

    status = http_response.status

    if status == 200:
        return

    # emtpy response buffer
    body = http_response.read()

    if status == 404:
        raise HTTPResourceNotFoundError("This resource has not been found.")
    elif status > 499:
        raise HTTPServerError(body=body)

    reason = http_response.reason
    standard_message = ("Request failed. The response returned with status "
                        "{} - {}.".format(status, reason))
    if status == 401:
        raise LoginFailedError(standard_message)
    elif status == 403:
        raise HTTPForbiddenError(standard_message)
    elif status in (413, 414):
        raise HTTPURITooLongError(standard_message)
    elif 399 < status < 500:
        raise HTTPClientError(msg=standard_message, status=status, body=body)
    else:
        raise CaosDBException(standard_message)


class _Connection(object):  # pylint: disable=useless-object-inheritance
    """This connection class provides the interface to the database connection
    allowing for retrieval, insertion, update, etc. of entities, files, users,
    roles and much more.

    It wrapps an instance of CaosDBServerConnection which actually does the
    work (how, depends on the instance).

    It is a singleton and should not be instanciated or modified by any client.
    Use the methods `get_connection` and `configure_connection` for this
    purpose.
    """

    __instance = None

    def __init__(self):
        self._delegate_connection = None
        self._authenticator = None
        self.is_configured = False

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = _Connection()

        return cls.__instance

    def configure(self, **config):
        self.is_configured = True

        if "implementation" not in config:
            raise ConfigurationError(
                "Missing CaosDBServerConnection implementation. You did not "
                "specify an `implementation` for the connection.")
        try:
            self._delegate_connection = config["implementation"]()

            if not isinstance(self._delegate_connection,
                              CaosDBServerConnection):
                raise TypeError("The `implementation` callable did not return "
                                "an instance of CaosDBServerConnection.")
        except TypeError as type_err:
            raise ConfigurationError(
                "Bad CaosDBServerConnection implementation. The "
                "implementation must be a callable object which returns an "
                "instance of `CaosDBServerConnection` (e.g. a constructor "
                "or a factory).\n{}".format(type_err.args[0]))
        self._delegate_connection.configure(**config)

        if "auth_token" in config:
            # deprecated, needed for older scripts
            config["password_method"] = "auth_token"
        if "password_method" not in config:
            raise ConfigurationError("Missing password_method. You did "
                                     "not specify a `password_method` for"
                                     "the connection.")
        self._authenticator = _get_authenticator(
            connection=self._delegate_connection, **config)

        return self

    def retrieve(self, entity_uri_segments=None, query_dict=None, **kwargs):
        path = make_uri_path(entity_uri_segments, query_dict)

        http_response = self._http_request(method="GET", path=path, **kwargs)

        return http_response

    def delete(self, entity_uri_segments=None, query_dict=None, **kwargs):
        path = make_uri_path(entity_uri_segments, query_dict)

        http_response = self._http_request(
            method="DELETE", path=path, **kwargs)

        return http_response

    def update(self, entity_uri_segment, query_dict=None, **kwargs):
        path = make_uri_path(entity_uri_segment, query_dict)

        http_response = self._http_request(method="PUT", path=path, **kwargs)

        return http_response

    def activate_user(self, link):
        self._authenticator.logout()
        fullurl = urlparse(link)
        path = fullurl.path
        query = fullurl.query
        http_response = self._http_request(
            method="GET", path=path + "?" + query)

        return http_response

    def put_form_data(self, entity_uri_segment, params):
        return self._form_data_request(
            method="PUT", path=entity_uri_segment, params=params)

    def post_form_data(self, entity_uri_segment, params):
        return self._form_data_request(
            method="POST",
            path=entity_uri_segment,
            params=params)

    def _form_data_request(self, method, path, params):
        body = urlencode(params)
        headers = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = self._http_request(
            method=method,
            path=quote(path),
            body=body,
            headers=headers)

        return response

    def insert(self, entity_uri_segment, query_dict=None, body=None, **kwargs):
        path = make_uri_path(entity_uri_segment, query_dict)

        http_response = self._http_request(
            method="POST", path=path, body=body, **kwargs)

        return http_response

    def download_file(self, path):
        """This function downloads a file via HTTP from the Caosdb file
        system."""
        try:
            uri_segments = ["FileSystem"]
            uri_segments.extend(path.split("/"))

            return self.retrieve(entity_uri_segments=uri_segments)
        except HTTPResourceNotFoundError:
            raise HTTPResourceNotFoundError("This file does not exist.")

    def _login(self):
        self._authenticator.login()

    def _logout(self):
        self._authenticator.logout()

    def _http_request(self, method, path, headers=None, body=None, **kwargs):
        try:
            return self._retry_http_request(method=method, path=path,
                                            headers=headers, body=body,
                                            **kwargs)
        except SocketError as e:
            if e.errno != BrokenPipe:
                raise

            return self._retry_http_request(method=method, path=path,
                                            headers=headers, body=body,
                                            reconnect=False,
                                            **kwargs)
        except LoginFailedError:
            if kwargs.get("reconnect", True) is True:
                self._login()

                return self._retry_http_request(method=method, path=path,
                                                headers=headers, body=body,
                                                reconnect=False,
                                                **kwargs)
            raise

    def _retry_http_request(self, method, path, headers, body, **kwargs):

        if hasattr(body, "encode"):
            # python3
            body = body.encode("utf-8")

        if headers is None:
            headers = {}
        self._authenticator.on_request(method=method, path=path,
                                       headers=headers)
        _LOGGER.debug("request: %s %s %s", method, path, str(headers))
        http_response = self._delegate_connection.request(
            method=method,
            path=path,
            headers=headers,
            body=body, **kwargs)
        _LOGGER.debug("response: %s %s", str(http_response.status),
                      str(http_response.getheaders()))
        self._authenticator.on_response(http_response)
        _handle_response_status(http_response)

        return http_response

    def get_username(self):
        """
        Return the username of the current connection.

        Shortcut for: get_connection()._authenticator._credentials_provider.username
        """
        return self._authenticator._credentials_provider.username

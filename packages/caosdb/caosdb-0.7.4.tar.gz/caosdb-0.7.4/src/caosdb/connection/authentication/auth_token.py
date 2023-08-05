#! -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <f.fitschen@indiscale.com>
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
"""auth_token.

An Authentictor which only uses only a pre-supplied authentication token.
"""
from __future__ import absolute_import, unicode_literals, print_function
from .interface import AbstractAuthenticator, CaosDBServerConnection
from caosdb.connection.utils import auth_token_to_cookie
from caosdb.exceptions import LoginFailedError


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which only uses a pre-supplied authentication
    token.

    Returns
    -------
    AuthTokenAuthenticator
    """
    return AuthTokenAuthenticator()


class AuthTokenAuthenticator(AbstractAuthenticator):
    """AuthTokenAuthenticator.

    Subclass of AbstractAuthenticator which provides authentication only via
    a given authentication token.

    Methods
    -------
    login
    logout
    configure
    """

    def __init__(self):
        super(AuthTokenAuthenticator, self).__init__()
        self.auth_token = None
        self._connection = None

    def login(self):
        self._login()

    def _login(self):
        raise LoginFailedError("The authentication token is expired or you "
                               "have been logged out otherwise. The "
                               "auth_token authenticator cannot log in "
                               "again. You must provide a new "
                               "authentication token.")

    def logout(self):
        self._logout()

    def _logout(self):
        self.logger.debug("[LOGOUT]")
        if self.auth_token is not None:
            headers = {'Cookie': auth_token_to_cookie(self.auth_token)}
            self._connection.request(method="DELETE", path="logout",
                                     headers=headers)
        self.auth_token = None

    def configure(self, **config):
        if "auth_token" in config:
            self.auth_token = config["auth_token"]
        if "connection" in config:
            self._connection = config["connection"]
            if not isinstance(self._connection, CaosDBServerConnection):
                raise Exception("""Bad configuration of the caosdb connection.
                                The `connection` must be an instance of
                                `CaosDBConnection`.""")

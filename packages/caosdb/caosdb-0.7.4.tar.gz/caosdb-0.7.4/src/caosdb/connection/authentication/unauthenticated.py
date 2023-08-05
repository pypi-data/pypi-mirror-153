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
"""unauthenticated.

An Authenticator which suppresses any authentication and also ignores auth_token
cookies.
"""
from __future__ import absolute_import, unicode_literals, print_function
from .interface import AbstractAuthenticator, CaosDBServerConnection
from caosdb.exceptions import LoginFailedError


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which only uses a pre-supplied authentication
    token.

    Returns
    -------
    AuthTokenAuthenticator
    """
    return Unauthenticated()


class Unauthenticated(AbstractAuthenticator):
    """Unauthenticated.

    Subclass of AbstractAuthenticator which suppresses any authentication and
    also ignores auth_token cookies.

    Methods
    -------
    login
    logout
    configure
    on_request
    on_response
    """

    def __init__(self):
        super(Unauthenticated, self).__init__()
        self.auth_token = None
        self._connection = None

    def login(self):
        self._login()

    def _login(self):
        raise LoginFailedError("This caosdb client is configured to stay "
                               "unauthenticated. Change your "
                               "`password_method` and provide an "
                               "`auth_token` or credentials if you want "
                               "to authenticate this client.")

    def logout(self):
        self._logout()

    def _logout(self):
        self.auth_token = None

    def configure(self, **config):
        self.auth_token = None

    def on_request(self, method, path, headers, **kwargs):
        # pylint: disable=unused-argument
        """on_request.

        This implementation does not attempt to login or authenticate in any
        form.

        Parameters
        ----------
        method
            unused
        path
            unused
        headers
            unused
        **kwargs
            unused
        """
        pass

    def on_response(self, response):
        # pylint: disable=unused-argument
        """on_response.

        This implementation ignores any auth_token cookie sent by the server.

        Parameters
        ----------
        response
            unused
        """
        pass

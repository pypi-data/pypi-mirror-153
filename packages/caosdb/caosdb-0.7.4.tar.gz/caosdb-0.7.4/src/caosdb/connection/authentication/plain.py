# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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
"""plain.

A CredentialsProvider which reads the password from the configuration
dict.
"""
from __future__ import absolute_import, unicode_literals, print_function
from .interface import CredentialsProvider, CredentialsAuthenticator


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which uses plain text username/password credentials.

    Returns
    -------
    CredentialsAuthenticator
        with a PlainTextCredentialsProvider as back-end.
    """
    return CredentialsAuthenticator(PlainTextCredentialsProvider())


class PlainTextCredentialsProvider(CredentialsProvider):
    """PlainTextCredentialsProvider.

    A class for storing username/password credentials as plain text strings.

    Methods
    -------
    configure

    Attributes
    ----------
    password
    username
    """

    def __init__(self):
        super(PlainTextCredentialsProvider, self).__init__()
        self._password = None
        self._username = None

    def configure(self, **config):
        """configure.

        Parameters
        ----------
        **config
            Keyword arguments containing at least keywords "username" and "password".

        Returns
        -------
        None
        """
        if "password" in config:
            self._password = config["password"]
        if "username" in config:
            self._username = config["username"]

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

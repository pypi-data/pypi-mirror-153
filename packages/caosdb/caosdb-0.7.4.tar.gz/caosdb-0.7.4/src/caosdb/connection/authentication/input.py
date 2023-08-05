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
"""input.

A CredentialsProvider which reads the password from the input line.
"""
from __future__ import absolute_import, unicode_literals, print_function
from .interface import CredentialsProvider, CredentialsAuthenticator

import getpass


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which uses the input for username/password credentials.

    Returns
    -------
    CredentialsAuthenticator
        with an InputCredentialsProvider as back-end.
    """
    return CredentialsAuthenticator(InputCredentialsProvider())


class InputCredentialsProvider(CredentialsProvider):
    """InputCredentialsProvider.

    A class for obtaining the password directly from the user.

    Methods
    -------
    configure

    Attributes
    ----------
    password
    username
    """

    def __init__(self):
        super(InputCredentialsProvider, self).__init__()
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
        if config.get("username"):
            self._username = config["username"]
        else:
            self._username = input("Please enter the user name: ")

        url = config["url"]
        self._password = getpass.getpass(
            "Please enter the password for `{}` at `{}`: ".format(
                self._username, url))

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

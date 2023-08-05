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
"""keyring.

A CredentialsProvider which uses the external 'keyring' library to
retrieve the password.
"""

import sys
import importlib
from getpass import getpass
from caosdb.exceptions import ConfigurationError
from .external_credentials_provider import ExternalCredentialsProvider
from .interface import CredentialsAuthenticator


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which uses plain text username/password credentials.
    The difference to the `plain` module is that this implementation retrieves
    the password from the external gnome keyring.

    Returns
    -------
    CredentialsAuthenticator
        with a 'KeyringCaller' as back-end.
    """
    return CredentialsAuthenticator(KeyringCaller(callback=_call_keyring))


def _get_external_keyring():
    try:
        return importlib.import_module("keyring")
    except ImportError:
        raise RuntimeError(
            "The keyring password method requires installation of the"
            "keyring python package. On linux with python < 3.5, "
            "this requires the installation of dbus-python as a "
            "system package.")


def _call_keyring(**config):
    if "username" not in config:
        raise ConfigurationError("Your configuration did not provide a "
                                 "`username` which is needed by the "
                                 "`KeyringCaller` to retrieve the "
                                 "password in question.")
    url = config.get("url")
    username = config.get("username")
    app = "caosdb — {}".format(url)
    external_keyring = _get_external_keyring()
    password = external_keyring.get_password(app, username)
    if password is None:
        print("No password for user {} on {} found in keyring."
              .format(username, app))
        password = getpass("Enter password to save "
                           "in system keyring/wallet: ")
        external_keyring.set_password(app, username, password)
    return password


class KeyringCaller(ExternalCredentialsProvider):
    """KeyringCaller.

    A class for retrieving the password from the external 'gnome keyring' and
    storing the username/password credentials as plain text strings.

    Methods
    -------
    configure

    Attributes
    ----------
    password
    username
    """

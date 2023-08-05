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
"""pass.

A CredentialsProvider which calls the external program 'pass' for the
password.
"""

from subprocess import check_output, CalledProcessError
from caosdb.exceptions import ConfigurationError
from .interface import CredentialsAuthenticator
from .external_credentials_provider import ExternalCredentialsProvider


def get_authentication_provider():
    """get_authentication_provider.

    Return an authenticator which uses plain text username/password credentials.
    The difference to the `plain` module is that this implementation retrieves
    the password from the external program 'pass'.

    Returns
    -------
    CredentialsAuthenticator
        with a 'PassCaller' as back-end.
    """
    return CredentialsAuthenticator(PassCaller(callback=_call_pass))


def _call_pass(**config):
    if "password_identifier" not in config:
        raise ConfigurationError("Your configuration did not provide a "
                                 "`password_identifier` which is needed "
                                 "by the `PassCaller` to retrieve the "
                                 "password in question.")

    try:
        return check_output(
            "pass " + config["password_identifier"],
            shell=True).splitlines()[0].decode("UTF-8")
    except CalledProcessError as exc:
        raise RuntimeError(
            "Password manager returned error code {}. This usually "
            "occurs if the password_identifier in .pycaosdb.ini is "
            "incorrect or missing.".format(exc.returncode))


class PassCaller(ExternalCredentialsProvider):
    """PassCaller.

    A class for retrieving the password from the external program 'pass' and
    storing the username/password credentials as plain text strings.

    Methods
    -------
    configure

    Attributes
    ----------
    password
    username
    """
    # all the work is done in _call_pass and the super class
    pass

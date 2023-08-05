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
"""external_credentials_provider."""
from __future__ import absolute_import, unicode_literals
from abc import ABCMeta
import logging
from .plain import PlainTextCredentialsProvider

# meta class compatible with Python 2 *and* 3:
ABC = ABCMeta(str('ABC'), (object, ), {str('__slots__'): ()})


class ExternalCredentialsProvider(PlainTextCredentialsProvider, ABC):
    """ExternalCredentialsProvider.

    Abstract subclass of PlainTextCredentialsProvider which should be used to
    implement external credentials provider (e.g. pass, keyring, or any other call
    to an external program, which presents the plain text password, which is to be
    used for the authentication.

    Parameters
    ----------
    callback: Function
        A function which has **kwargs argument. This funktion will be called
        each time a password is needed with the current connection
        configuration as parameters.
    """

    def __init__(self, callback):
        super(ExternalCredentialsProvider, self).__init__()
        self._callback = callback
        self._config = None

    def configure(self, **config):
        """configure.

        Parameters
        ----------
        **config
            Keyword arguments containing the necessary arguments for the
            concrete implementation of this class.

        Attributes
        ----------
        password : str
            The password. This password is not stored in this class. A callback
            is called to provide the password each time this property is
            called.

        Returns
        -------
        None
        """
        if "password" in config:
            if "password_method" in config:
                authm = "`{}`".format(config["password_method"])
            else:
                authm = "an external credentials provider"
            self.logger.log(logging.WARNING,
                            ("`password` defined. You configured caosdb to "
                             "use %s as authentication method and yet "
                             "provided a password yourself. This indicates "
                             "a misconfiguration (e.g. in your "
                             "pycaosdb.ini) and should be avoided."),
                            authm)
        self._config = dict(config)
        super(ExternalCredentialsProvider, self).configure(**config)

    @property
    def password(self):
        return self._callback(**self._config)

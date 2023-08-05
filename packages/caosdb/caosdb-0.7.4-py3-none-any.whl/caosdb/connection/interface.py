# -*- encoding: utf-8 -*-
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
"""This module defines the CaosDBServerConnection interface."""
from abc import ABCMeta, abstractmethod, abstractproperty

# meta class compatible with Python 2 *and* 3:
ABC = ABCMeta('ABC', (object, ), {'__slots__': ()})


class CaosDBHTTPResponse(ABC):
    """An abstract class which defines a minimal interface for responses of the
    CaosDBServer."""

    @abstractmethod
    def read(self, size=-1):
        """Read up to *size* bytes from the response body.

        If size is unspecified or -1, all bytes until EOF are returned.
        """

    @abstractmethod
    def getheader(self, name, default=None):
        """Return the value of the header *name* or the value of *default* if
        there is no such header.

        If there are multiple headers with that name, return all of the
        values joined by ', '. If default is an iterable, its elements
        are returned likewise.
        """

    @abstractproperty
    def status(self):
        """Status code of the response."""

    @abstractmethod
    def getheaders(self):
        """Return all headers."""

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.close()

    @abstractmethod
    def close(self):
        """close.

        Close this response. Depending on the implementation this might
        also close underlying streams, sockets etc.
        """


class CaosDBServerConnection(ABC):
    """Abstract class which defines the interface for sending requests to the
    caosdb server."""

    @abstractmethod
    def request(self, method, path, headers=None, body=None, **kwargs):
        """Abstract method. Implement this method for HTTP requests to the
        caosdb server.

        Returns
        -------
        CaosDBHTTPResponse
        """

    @abstractmethod
    def configure(self, **kwargs):
        """Configure the connection. This method is to be called by
        configure_connection.

        Returns
        -------
        None
        """

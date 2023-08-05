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
"""Classes and functions to immitate a caosdb server without actually setting
up a tcp connection."""

from __future__ import unicode_literals, print_function
from io import StringIO
from .connection import CaosDBServerConnection, CaosDBHTTPResponse


def _request_log_message(method, path, headers, body, **kwargs):
    return "{method}: {path}{nl0}{kwargs}{nl1}{headers}{nl2}{body}".format(
        method=method,
        path=path,
        headers=headers if headers else "",
        body=body if body else "",
        kwargs=kwargs if kwargs else "",
        nl0="\n" if kwargs else "",
        nl1="\n" if headers else "",
        nl2="\n" if body else "")


class MockUpResponse(CaosDBHTTPResponse):
    """A class for the responses of a request to the MockUpServerConnection."""

    def __init__(self, status, headers, body):
        self._status = status
        self.headers = headers
        self.response = StringIO(body)

    @property
    def status(self):
        """Return the status of the response."""
        return self._status

    def read(self, size=-1):
        """Return the body of the response."""
        return self.response.read(size)

    def getheader(self, name, default=None):
        """Get the contents of the header `name`, or `default` if there is no
        matching header."""
        return self.headers[name] if name in self.headers else default

    def getheaders(self):
        return self.headers

    def close(self):
        pass


class MockUpServerConnection(CaosDBServerConnection):
    """The mock-up connection which does not actually connect to anything but
    just returns predefined responses which mimic the caosdb server."""

    def __init__(self):
        self.resources = [self._login]

    def _login(self, method, path, headers, body):
        if method == "POST" and path == "login":
            return MockUpResponse(200,
                                  headers={"AuthToken":
                                           "mockup-auth-token"},
                                  body="")

    def configure(self, **kwargs):
        """This configure method does nothing."""

    def request(self, method, path, headers=None, body=None, **kwargs):
        """Search a resource in the `resources` list which is answering to the
        request and return the response or raise a RuntimeError."""
        for resource in self.resources:
            response = resource(
                method=method, path=path, headers=headers, body=body, **kwargs)
            if response:
                return response
        raise RuntimeError(
            "No response for this request - " +
            _request_log_message(method, path, headers, body, **kwargs))

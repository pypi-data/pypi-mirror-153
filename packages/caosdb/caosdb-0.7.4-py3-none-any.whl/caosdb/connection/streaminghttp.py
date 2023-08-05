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
# Original work Copyright (c) 2011 Chris AtLee
# Modified work Copyright (c) 2017 Biomedical Physics, MPI for Dynamics and Self-Organization
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Streaming HTTP uploads module.

This module extends the standard httplib and http.client HTTPConnection so that
iterable objects can be used in the body of HTTP requests.

**N.B.** You must specify a Content-Length header if using an iterable object
since there is no way to determine in advance the total size that will be
yielded, and there is no way to reset an interator.
"""

from __future__ import unicode_literals, print_function, absolute_import
import socks
import socket
try:
    # python3
    from http import client as client
except ImportError:
    # python2
    import httplib as client


__all__ = ['StreamingHTTPSConnection']


class StreamingHTTPSConnection(client.HTTPSConnection, object):
    """Subclass of `http.client.HTTSConnection` or `httplib.HTTPSConnection`
    that overrides the `send()` method to support iterable body objects."""
    # pylint: disable=unused-argument, arguments-differ

    def __init__(self, socket_proxy=None, **kwargs):
        if socket_proxy is not None:
            host, port = socket_proxy.split(":")
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host,
                                  int(port))
            socket.socket = socks.socksocket
        super(StreamingHTTPSConnection, self).__init__(**kwargs)

    def _send_output(self, body, **kwargs):
        """Send the currently buffered request and clear the buffer.

        Appends an extra \\r\\n to the buffer.
        A message_body may be specified, to be appended to the request.

        This method is implemented in differently in the various python
        versions (which is extremely annoying). So we provide a unified but
        relatively dumb implementaion which only serves our needs.
        """
        self._buffer.extend(("".encode("utf-8"), "".encode("utf-8")))
        headers = "\r\n".encode("utf-8").join(self._buffer)
        del self._buffer[:]

        self.send(headers)
        if body is not None:
            self.send(body)

    # pylint: disable=too-many-branches

    def send(self, value):
        """Send ``value`` to the server.

        ``value`` can be a string-like object which supports a 'encode' method,
        a file-like object that supports a .read() method, or an iterable object
        that supports a .next() method.

        An encode()able ``value`` will be utf-8 encoded before sending.
        """
        # Based on python 2.6's httplib.HTTPConnection.send()
        if self.sock is None:
            if self.auto_open:
                self.connect()
            else:
                raise client.NotConnected()

        # send the data to the server. if we get a broken pipe, then close
        # the socket. we want to reconnect when somebody tries to send again.
        #
        # NOTE: we DO propagate the error, though, because we cannot simply
        #       ignore the error... the caller will know if they can retry.
        if self.debuglevel > 0:
            print("send: ", repr(value))
        try:
            blocksize = 8192
            if hasattr(value, 'read'):
                if hasattr(value, 'seek'):
                    value.seek(0)
                if self.debuglevel > 0:
                    print("sendIng a read()able")
                data = value.read(blocksize)
                while data:
                    self.sock.sendall(data)
                    data = value.read(blocksize)
            elif hasattr(value, 'next'):
                if hasattr(value, 'reset'):
                    value.reset()
                if self.debuglevel > 0:
                    print("sendIng an iterable")
                for data in value:
                    if hasattr(data, "encode"):
                        self.sock.sendall(data.encode('utf-8'))
                    else:
                        self.sock.sendall(data)
            else:
                if self.debuglevel > 0:
                    print("sendIng a byte-like")
                self.sock.sendall(value)
        except socket.error as err:
            if err.args[0] == 32:      # Broken pipe
                self.close()
            raise

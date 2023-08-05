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
"""Utility functions for the connection module."""
from __future__ import unicode_literals, print_function
try:
    from builtins import str, unicode  # pylint: disable=redefined-builtin
except ImportError:
    from builtins import str as unicode
try:  # pragma: no cover
    # python3
    from urllib.parse import (urlencode as _urlencode, quote as _quote,
                              urlparse, urlunparse, unquote as _unquote)
except ImportError:  # pragma: no cover
    # python2
    from urllib import (urlencode as _urlencode, quote as _quote, unquote as
                        _unquote)
    from urlparse import urlparse, urlunparse
import re


def urlencode(query):
    """Convert a dict of into a url-encoded (unicode) string.

    This is basically a python2/python3 compatibility wrapper for the respective
    functions in the urllib module with some slight modifications.

    1) A `None` is translated to an empty string.
    >>> urlencode({'key': None})
    'key='

    2) Unicode strings are allowed for python2.
    >>> urlencode({'kèy': 'välüe'})
    'k%C3%A8y=v%C3%A4l%C3%BCe'

    3) All other parameters which can be passed to the respective functions are
    not implemented here and the default parameters will be used.
    >>> urlencode({'key': ['val1', 'val2']}, doseq=True)
    Traceback (most recent call last):
        ...
    TypeError: urlencode() got an unexpected keyword argument 'doseq'

    Otherwise, this functions works exactly as its counterparts in the urllib
    modules when they are called with only the query parameter.

    Parameters
    ----------
    query : dict
        A dict of str or unicode keys with None, unicode or str values.

    Returns
    -------
    str
        A series of `key=value` pairs separated by `&`.

    Raises
    ------
    AttributeError
        If a key or a value does not have a 'encode' method.
    """
    return str(
        _urlencode({
            key.encode("utf-8"): (val.encode("utf-8")
                                  if val is not None else '')
            for key, val in query.items()
        }))


def make_uri_path(segments=None, query=None):
    """Url-encode all segments, concat them with slashes and append the query.

    Examples
    --------
    >>> make_uri_path(['a','b'])
    'a/b'
    >>> make_uri_path(['a','ö'])
    'a/%C3%B6'
    >>> make_uri_path(['a','b'], {'key': 'val'})
    'a/b?key=val'

    Parameters
    ----------
    segments : list of str
        The segments of the path
    query: dict
        A dict of str keys with None or str values.

    Returns
    -------
    str
        A relative uri path (no host information, possibly no root path).
    """
    path_no_query = ("/".join([quote(segment) for segment in segments])
                     if segments else "")
    return str(path_no_query if query is None else "?".join([
        path_no_query, "&".join([
            quote(key) + "=" +
            (quote(query[key]) if query[key] is not None else "")
            for key in query
        ])
    ]))


def quote(string):
    enc = unicode(string).encode('utf-8')
    return _quote(enc).replace('/', '%2F')


def parse_url(url):
    fullurl = urlparse(url)
    # make sure the path ends with a slash
    if not fullurl.path.endswith("/"):
        parse_result = list(fullurl)
        parse_result[2] += "/"
        fullurl = urlparse(urlunparse(parse_result))
    return fullurl


def check_python_ssl_version(hexversion):
    """Check the python version.

    If `version < 2.7.9` or `3.0 <= version < 3.2` the ssl library does not
    actually verify the ssl certificates send by the server. That is evil and
    these versions shall not be used.

    Parameters
    ----------
    hexversion : int
        A python version.

    Raises
    ------
    Exception
        If the version does not fully support ssl encryption.
    """
    if hexversion < 0x02070900:
        raise Exception(
            "version " + str(hex(hexversion)) +
            "\nPython version is smaller than 2.7.9. It is not does not fully support SSL encryption. Please update your Python to 2.7.9 or greater, or 3.2 or greater."
        )
    elif hexversion >= 0x03000000 and hexversion < 0x03020000:
        raise Exception(
            "version " + str(hex(hexversion)) +
            "\nPython 3 version is smaller than 3.2. It is not does not fully support SSL encryption. Please update your Python to 2.7.9 or greater, or 3.2 or greater."
        )


_PATTERN = re.compile(r"^SessionToken=([^;]*);.*$")


def unquote(string):
    """unquote.

    Decode an urlencoded string into a plain text string.
    """
    bts = _unquote(string)
    if hasattr(bts, "decode"):
        # python 2
        return bts.decode("utf-8")
    return bts


def parse_auth_token(cookie):
    """parse_auth_token.

    Parse an auth token from a cookie.

    Parameters
    ----------
    cookie : str
        A cookie with an urlencoded authtoken.

    Returns
    -------
    str
        An auth token string.
    """
    auth_token = None
    if cookie is not None and _PATTERN.match(cookie):
        auth_token = unquote(_PATTERN.split(cookie)[1])
    return auth_token


def auth_token_to_cookie(auth_token):
    """auth_token_to_cookie.

    Urlencode an auth token string and format it as a cookie.

    Parameters
    ----------
    auth_token : str
        The plain auth token string.

    Raises
    ------
    TypeError
        If the auth_token was None

    Returns
    -------
    str
        A cookie
    """
    if auth_token is None:
        raise TypeError("Parameter `auth_token` was None.")
    return "SessionToken=" + quote(auth_token) + ";"

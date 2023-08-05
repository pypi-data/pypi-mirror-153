# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
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
"""server_side_scripting

Helper functions for calling server-side scripts.
"""
from urllib.parse import quote
from lxml import etree

from caosdb.connection.connection import get_connection
from caosdb.connection.utils import urlencode
from caosdb.connection.encode import MultipartParam, multipart_encode


def _make_params(pos_args, opts):
    """Create and return option string components.

The return value is a dict with be something like `-O<key>`:`<value>` from `opts` and
`-p{0,1,2,3,...}`:`<value>` from `pos_args`.

    """
    result = {}
    for key, val in opts.items():
        result["-O{key}".format(key=key)] = str(val)
    for i, val in enumerate(pos_args):
        result["-p{i}".format(i=i)] = str(val)
    return result


def _make_multipart_request(call, pos_args, opts, files):
    """Return body and header for an HTTP request.
    """
    parts = list()
    params = _make_params(pos_args, opts)

    parts.append(MultipartParam("call", call))
    for key, val in params.items():
        parts.append(MultipartParam(key, val))

    for paramname, filename in files.items():
        parts.append(MultipartParam.from_file(paramname=paramname,
                                              filename=filename))

    body, headers = multipart_encode(parts)
    return body, headers


def _make_form_request(call, pos_args, opts):
    """Return URL from call and argumewnts, and headers for urlencoding."""
    form = dict()
    form["call"] = call

    params = _make_params(pos_args, opts)
    for key, val in params.items():
        form[key] = val

    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    return urlencode(form), headers


def _make_request(call, pos_args, opts, files=None):
    """
    Multipart if with files, otherwise url-encoded.

    Return
    ------
    path_segments, body, headers
    """

    if files is not None:
        return _make_multipart_request(call, pos_args, opts, files)

    return _make_form_request(call, pos_args, opts)


def run_server_side_script(call, *args, files=None, **kwargs):
    """

    Return
    ------
    response : ScriptingResponse
    """
    body, headers = _make_request(call=call, pos_args=args,
                                  opts=kwargs, files=files)
    response = get_connection()._http_request(method="POST",
                                              path=quote("scripting"),
                                              body=body,
                                              headers=headers)
    xml = etree.parse(response)
    code = int(xml.xpath("/Response/script/@code")[0])
    call = xml.xpath("/Response/script/call")[0].text
    stdout = xml.xpath("/Response/script/stdout")[0].text
    stderr = xml.xpath("/Response/script/stderr")[0].text

    return ScriptingResponse(call=call,
                             code=code,
                             stdout=stdout,
                             stderr=stderr)


class ScriptingResponse():
    """ScriptingResponse

    A data class for the response of server-side scripting calls.

    Properties
    ----------
    code : int
        The return code of the script process.
    call : str
        The complete call of the script minus the absolute path and the
        auth_token.
    stdout : str
        The STDOUT of the script process.
    stderr : str
        The STDERR of the script process.

    """

    def __init__(self, call, code, stdout, stderr):
        self.call = call
        self.code = code
        self.stdout = stdout
        self.stderr = stderr

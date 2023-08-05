# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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

"""missing docstring."""

import re
import string
import random
from caosdb.common.utils import xml2str
from caosdb.connection.connection import get_connection
from caosdb.exceptions import (EntityDoesNotExistError, HTTPClientError,
                               HTTPForbiddenError, HTTPResourceNotFoundError,
                               ServerConfigurationException)
from lxml import etree


def set_server_property(key, value):
    """set_server_property.

    Set a server property.

    Parameters
    ----------
    key : str
        The name of the server property.
    value : str
        The value of the server property.


    Returns
    -------
    None
    """
    con = get_connection()
    try:
        con._form_data_request(method="POST", path="_server_properties",
                               params={key: value}).read()
    except EntityDoesNotExistError:
        raise ServerConfigurationException(
            "Debug mode in server is probably disabled.") from None


def get_server_properties():
    """get_server_properties.

    Get all server properties as a dict.

    Returns
    -------
    dict
        The server properties.
    """
    con = get_connection()
    try:
        body = con._http_request(
            method="GET", path="_server_properties").response
    except EntityDoesNotExistError:
        raise ServerConfigurationException(
            "Debug mode in server is probably disabled.") from None

    xml = etree.parse(body)
    props = dict()

    for elem in xml.getroot():
        props[elem.tag] = elem.text

    return props


def get_server_property(key):
    """get_server_property.

    Get a server property.

    Parameters
    ----------
    key : str
        The name of the server property

    Returns
    -------
    value : str
        The string value of the server property.

    Raises
    ------
    KeyError
        If the server property is no defined.
    """

    return get_server_properties()[key]


def generate_password(length: int):
    """Create a random password that fulfills the security requirements

    Parameters
    ----------
    length : int
        Length of the generated password.  Has to be greater than 7.

    Returns
    -------
    password : string
        Generated random password of the given length

    Raises
    ------
    ValueError:
        If the length is less than 8.
    """
    minimum_password_length = 8
    if length < minimum_password_length:
        raise ValueError("CaosDB passwords have to be at least {} characters.".format(
            minimum_password_length))
    sample_letters = string.ascii_letters + string.digits + "!#$%*+-/:;?_"
    password = ''.join((random.choice(sample_letters) for i in range(length)))

    while not re.match(r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}",
                       password):
        password = ''.join((random.choice(sample_letters)
                            for i in range(length)))

    return password


def _retrieve_user(name, realm=None, **kwargs):
    con = get_connection()
    try:
        return con._http_request(method="GET", path="User/" + (realm + "/" + name if realm is not None else name), **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to retrieve this user."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "User does not exist."
        raise


def _delete_user(name, **kwargs):
    con = get_connection()
    try:
        return con._http_request(method="DELETE", path="User/" + name, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to delete this user."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "User does not exist."
        raise


def _update_user(name, realm=None, password=None, status=None,
                 email=None, entity=None, **kwargs):
    con = get_connection()
    params = {}

    if password is not None:
        params["password"] = password

    if status is not None:
        params["status"] = status

    if email is not None:
        params["email"] = email

    if entity is not None:
        params["entity"] = str(entity)
    try:
        return con.put_form_data(entity_uri_segment="User/" + (realm + "/" + name if realm is not None else name), params=params, **kwargs).read()
    except HTTPResourceNotFoundError as e:
        e.msg = "User does not exist."
        raise e
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to update this user."
        raise e
    except HTTPClientError as e:
        if e.status == 409:
            e.msg = "Entity does not exist."

        if e.status == 422:
            e.msg = """Maybe the password does not match the required standard?
                        The current requirements are:
                        - at least 8 characters
                        - at least 1 number
                        - at least 1 lower case character
                        - at least 1 upper case character
                        - at least 1 special character"""
        raise


def _insert_user(name, password=None, status=None, email=None, entity=None, **kwargs):
    con = get_connection()
    params = {"username": name}

    if password is not None:
        params["password"] = password

    if status is not None:
        params["status"] = status

    if email is not None:
        params["email"] = email

    if entity is not None:
        params["entity"] = entity
    try:
        return con.post_form_data(entity_uri_segment="User", params=params, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to insert a new user."
        raise e
    except HTTPClientError as e:
        if e.status == 409:
            e.msg = "User name is already in use."

        if e.status == 422:
            e.msg = """Maybe the password does not match the required standard?
                        The current requirements are:
                        - at least 8 characters
                        - at least 1 number
                        - at least 1 lower case character
                        - at least 1 upper case character
                        - at least 1 special character"""
        raise e


def _insert_role(name, description, **kwargs):
    con = get_connection()
    try:
        return con.post_form_data(entity_uri_segment="Role", params={"role_name": name, "role_description": description}, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to insert a new role."
        raise
    except HTTPClientError as e:
        if e.status == 409:
            e.msg = "Role name is already in use. Choose a different name."
        raise


def _update_role(name, description, **kwargs):
    con = get_connection()
    try:
        return con.put_form_data(entity_uri_segment="Role/" + name, params={"role_description": description}, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to update this role."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "Role does not exist."
        raise


def _retrieve_role(name, **kwargs):
    con = get_connection()
    try:
        return con._http_request(method="GET", path="Role/" + name, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to retrieve this role."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "Role does not exist."
        raise


def _delete_role(name, **kwargs):
    con = get_connection()
    try:
        return con._http_request(method="DELETE", path="Role/" + name, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to delete this role."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "Role does not exist."
        raise


def _set_roles(username, roles, realm=None, **kwargs):
    xml = etree.Element("Roles")

    for r in roles:
        xml.append(etree.Element("Role", name=r))

    body = xml2str(xml)
    con = get_connection()
    try:
        body = con._http_request(method="PUT", path="UserRoles/" + (realm + "/" +
                                                                    username if realm is not None else username), body=body, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to set this user's roles."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "User does not exist."
        raise
    except HTTPClientError as e:
        if e.status == 409:
            e.msg = "Role does not exist."
        raise
    ret = set()

    for r in etree.fromstring(body)[0]:
        if r.tag == "Role":
            ret.add(r.get("name"))

    return ret


def _get_roles(username, realm=None, **kwargs):
    con = get_connection()
    try:
        body = con._http_request(method="GET", path="UserRoles/" + (
            realm + "/" + username if realm is not None else username), **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to retrieve this user's roles."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "User does not exist."
        raise
    ret = set()

    for r in etree.fromstring(body).xpath('/Response/Roles')[0]:
        if r.tag == "Role":
            ret.add(r.get("name"))

    return ret


def _set_permissions(role, permission_rules, **kwargs):
    """Set permissions for a role.

Parameters
----------

role : str
    The role for which the permissions are set.

permission_rules : iterable<PermissionRule>
    An iterable with PermissionRule objects.

**kwargs :
    Additional arguments which are passed to the HTTP request.

Returns
-------
    None
    """
    xml = etree.Element("PermissionRules")

    for p in permission_rules:
        xml.append(p._to_xml())

    body = xml2str(xml)
    con = get_connection()
    try:
        return con._http_request(method="PUT", path="PermissionRules/" + role, body=body, **kwargs).read()
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to set this role's permissions."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "Role does not exist."
        raise


def _get_permissions(role, **kwargs):
    con = get_connection()
    try:
        return PermissionRule._parse_body(con._http_request(method="GET", path="PermissionRules/" + role, **kwargs).read())
    except HTTPForbiddenError as e:
        e.msg = "You are not permitted to retrieve this role's permissions."
        raise
    except HTTPResourceNotFoundError as e:
        e.msg = "Role does not exist."
        raise


class PermissionRule():
    """Permission rules.

Parameters
----------
action : str
    Either "grant" or "deny"

permission : str
    For example "RETRIEVE:*".

priority : bool, optional
    Whether the priority shall be set, defaults is False.
    """

    @staticmethod
    def _parse_boolean(bstr):
        return str(bstr) in ["True", "true", "TRUE", "yes"]

    def __init__(self, action, permission, priority=False):
        self._action = action
        self._permission = permission
        self._priority = PermissionRule._parse_boolean(priority)

    def _to_xml(self):
        xml = etree.Element(self._action)
        xml.set("permission", self._permission)

        if self._priority is True:
            xml.set("priority", "true")

        return xml

    @staticmethod
    def _parse_element(elem):
        return PermissionRule(elem.tag, elem.get(
            "permission"), elem.get("priority"))

    @staticmethod
    def _parse_body(body):
        xml = etree.fromstring(body)
        ret = set()

        for c in xml:
            if c.tag in ["Grant", "Deny"]:
                ret.add(PermissionRule._parse_element(c))

        return ret

    def __str__(self):
        return str(self._action) + "(" + str(self._permission) + ")" + \
            ("P" if self._priority is True else "")

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self).lower())

    def __eq__(self, other):
        return str(other).lower() == str(self).lower()

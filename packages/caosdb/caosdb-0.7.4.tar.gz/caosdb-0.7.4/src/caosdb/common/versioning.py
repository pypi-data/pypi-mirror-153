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
""" Versioning module for anything related to entity versions.

Currently this module defines nothing but a single class, `Version`.
"""

from __future__ import absolute_import
from caosdb.common.utils import xml2str
from lxml import etree


class Version():
    """The version of an entity.

    An entity version has a version id (string), a date (UTC timestamp), a
    list of predecessors and a list of successors.

    Parameters
    ----------
    id : str, optional
        See attribute `id`. Default: None
    date : str, optional
        See attribute `date`. Default: None
    username : str, optional
        See attribute `username`. Default: None
    realm : str, optional
        See attribute `realm`. Default: None
    predecessors : list of Version, optional
        See attribute `predecessors`. Default: empty list.
    successors : list of Version, optional
        See attribute `successors`. Default: empty list.
    is_head : bool
        See attribute `is_head`. Default: False
    is_complete_history : bool
        See attribute `is_complete_history`. Default: False

    Attributes
    ----------
    id : str
        Version ID (not the entity's id).
    date : str
        UTC Timestamp of the version, i.e. the date and time when the entity of
        this version has been inserted or modified.
    username : str
        The username of the user who inserted or updated this version.
    realm : str
        The realm of the user who inserted or updated this version.
    predecessors : list of Version
        Predecessors are the older entity versions which have been modified
        into this version. Usually, there is only one predecessor. However,
        this API allows for entities to be merged into one entity, which would
        result in more than one predecessor.
    successors : list of Version
        Successors are newer versions of this entity. If there are successors,
        this version is not the latest version of this entity. Usually, there
        is only one successor. However, this API allows that a single entity
        may co-exist in several versions (e.g. several proposals for the next
        entity status). That would result in more than one successor.
    is_head : bool or string
        If true, this indicates that this version is the HEAD if true.
        Otherwise it is not known whether this is the head or not.  Any string
        matching "true" (case-insensitively) is regarded as True.
        Nota bene: This property should typically be set if the server response
        indicated that this is the head version.
    is_complete_history : bool or string
        If true, this indicates that this version contains the full version
        history. That means, that the predecessors and successors have their
        respective predecessors and successors attached as well and the tree is
        completely available.  Any string matching "true" (case-insensitively)
        is regarded as True.
        Nota bene: This property should typically be set if the server response
        indicated that the full version history is included in its response.
    """

    # pylint: disable=redefined-builtin
    def __init__(self, id=None, date=None, username=None, realm=None,
                 predecessors=None, successors=None, is_head=False,
                 is_complete_history=False):
        """Typically the `predecessors` or `successors` should not "link back" to an existing Version
object."""
        self.id = id
        self.date = date
        self.username = username
        self.realm = realm
        self.predecessors = predecessors if predecessors is not None else []
        self.successors = successors if successors is not None else []
        self.is_head = str(is_head).lower() == "true"
        self.is_complete_history = str(is_complete_history).lower() == "true"

    def get_history(self):
        """ Returns a flat list of Version instances representing the history
        of the entity.

        The list items are ordered by the relation between the versions,
        starting with the oldest version.

        The items in the list have no predecessors or successors attached.

        Note: This method only returns reliable results if
        `self.is_complete_history is True` and it will not retrieve the full
        version history if it is not present.

        Returns
        -------
        list of Version
        """
        versions = []
        for p in self.predecessors:
            # assuming that predecessors don't have any successors
            versions = p.get_history()
        versions.append(Version(id=self.id, date=self.date,
                                username=self.username, realm=self.realm))
        for s in self.successors:
            # assuming that successors don't have any predecessors
            versions.extend(s.get_history())
        return versions

    def to_xml(self, tag="Version"):
        """Serialize this version to xml.

        The tag name is 'Version' per default. But since this method is called
        recursively for the predecessors and successors as well, the tag name
        can be configured.

        The resulting xml element contains attributes 'id' and 'date' and
        'Predecessor' and 'Successor' child elements.

        Parameters
        ----------
        tag : str, optional
            The name of the returned xml element. Defaults to 'Version'.

        Returns
        -------
        xml : etree.Element
        """
        xml = etree.Element(tag)
        if self.id is not None:
            xml.set("id", self.id)
        if self.date is not None:
            xml.set("date", self.date)
        if self.username is not None:
            xml.set("username", self.username)
        if self.realm is not None:
            xml.set("realm", self.realm)
        if self.predecessors is not None:
            for p in self.predecessors:
                xml.append(p.to_xml(tag="Predecessor"))
        if self.is_head is True:
            xml.set("head", "true")
        if self.successors is not None:
            for s in self.successors:
                xml.append(s.to_xml(tag="Successor"))
        return xml

    def __str__(self):
        """Return a stringified xml representation."""
        return self.__repr__()

    def __repr__(self):
        """Return a stringified xml representation."""
        return xml2str(self.to_xml())

    @staticmethod
    def from_xml(xml):
        """Parse a version object from a 'Version' xml element.

        Parameters
        ----------
        xml : etree.Element
            A 'Version' xml element, with 'id', possibly 'date', `username`,
            `realm`, and `head` attributes as well as 'Predecessor' and
            'Successor' child elements.

        Returns
        -------
        version : Version
            a new version instance
        """
        predecessors = [Version.from_xml(p) for p in xml if p.tag.lower() == "predecessor"]
        successors = [Version.from_xml(s) for s in xml if s.tag.lower() == "successor"]
        return Version(id=xml.get("id"), date=xml.get("date"),
                       is_head=xml.get("head"),
                       is_complete_history=xml.get("completeHistory"),
                       username=xml.get("username"), realm=xml.get("realm"),
                       predecessors=predecessors, successors=successors)

    def __hash__(self):
        """Hash of the version instance.

        Also hashes the predecessors and successors.
        """
        return (hash(self.id)
                + hash(self.date)
                + (Version._hash_list(self.predecessors)
                   if self.predecessors else 26335)
                + (Version._hash_list(self.successors)
                   if self.successors else -23432))

    @staticmethod
    def _hash_list(_list):
        """Hash a list by hashing each element and its index."""
        result = 12352
        for idx, val in enumerate(_list):
            result += hash(val) + idx
        return result

    @staticmethod
    def _eq_list(this, that):
        """List equality.

        List equality is defined as equality of each element, the order
        and length.
        """
        if len(this) != len(that):
            return False
        for v1, v2 in zip(this, that):
            if v1 != v2:
                return False
        return True

    def __eq__(self, other):
        """Equality of versions is defined by equality of id, date, and list
        equality of the predecessors and successors."""
        return (self.id == other.id
                and self.date == other.date
                and Version._eq_list(self.predecessors, other.predecessors)
                and Version._eq_list(self.successors, other.successors))

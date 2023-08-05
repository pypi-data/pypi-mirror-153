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

"""!!! Deprecated !!! YAML interface for the database (caosdb)"""

import yaml
from lxml import etree
from lxml.etree import Element
import re
import caosdb
import caosdb.common.utils as utils
from caosdb.connection.connection import get_connection
import warnings


def append_sublist(v, newel, def_entity_type):
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    if v is None:
        return
    for i in v:
        if isinstance(i, dict):
            entity_type = def_entity_type
            if "entity" in i:
                entity_type = i["entity"]
                del i["entity"]
            newel.append(kv_to_xml(entity_type, i))


def kv_to_xml(k, v):
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    newel = Element(k)
    # code.interact(local=locals())
    if isinstance(v, list):  # Top level loop
        append_sublist(v, newel, "Property")
    elif isinstance(v, dict):
        if "value" in v:
            newel.text = v["value"]
            del v["value"]
        subdict = {"properties": "Property", "parents": "Parent"}
        for jk, jv in subdict.items():
            if jk in v:
                append_sublist(v[jk], newel, jv)
                del v[jk]
        for k2, v2 in v.items():
            newel.set(k2, str(v2))
    return newel


def dict_to_xml(d):
    """
    d: The dictionary (possibly loaded from yaml)
       to convert to caosdb-xml.
    """
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    return kv_to_xml("Entities", d)


def yaml_to_xml(yamlstr):
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    """Load a yaml document from yamlstr and converts it to XML.

    Parameters
    ----------
    yamlstr : str
        The string to load the yaml document from.

    """
    return dict_to_xml(yaml.load(yamlstr, Loader=yaml.SafeLoader))


def process(text):
    """Do some replacements on the original file to obtain valid yaml."""
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    processed = re.sub(
        "^(\\s*)-\\s*\\{?(.*)\\}?\\s*$",
        "\\1- {\\2}",
        text,
        flags=re.MULTILINE)
    processed = re.sub("^(\\s*)\\+\\s*(.*)\\s*$", "\\1- \\2",
                       processed, flags=re.MULTILINE)
    print(processed)
    return processed


def yaml_file_to_xml(yamlfilename):
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    with open(yamlfilename, "r") as f:
        return yaml_to_xml(process(f.read()))


def insert_yaml_file(yamlfilename, simulate=False):
    """Inserts the contents of 'yamlfilename' into the database.

    Set 'simulate' to True if you don't actually want to insert the xml,
    but only receive what would be sent.
    """
    warnings.warn("""
                  This function is deprecated and will be removed with the next release.
                  Please use caosdb-advanced-user-tools/models/data_model.py for a
                  similar functionality.""", DeprecationWarning)
    con = get_connection()
    prs = etree.XMLParser(remove_blank_text=True)
    sent_xml = etree.tostring(
        etree.fromstring(
            etree.tostring(
                yaml_file_to_xml(yamlfilename)),
            prs),
        pretty_print=True)
    if simulate:
        return "", sent_xml.decode("utf-8")
    response = con.insert(entity_uri_segment="Entity/",
                          body=sent_xml)
    resp_text = response.readall()
    resp_elem = etree.fromstring(resp_text, prs)
    for i in resp_elem.iter("Error"):
        print("ERROR: " + i.get("description"))
        child = i.getparent()
        while child is not None:
            childname = ""
            childid = ""
            # print(etree.tostring(child))
            if child.get("name") is not None:
                childname = child.get("name")
            if child.get("id") is not None:
                childid = child.get("id")
            print("  in " + child.tag + " " + childname + " " + childid)
            child = child.getparent()
    return etree.tostring(resp_elem,
                          pretty_print=True).decode(
                              "utf-8"), sent_xml.decode("utf-8")

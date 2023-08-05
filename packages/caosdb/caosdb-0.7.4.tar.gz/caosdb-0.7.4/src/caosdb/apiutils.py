# -*- coding: utf-8 -*-
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2020-2022 IndiScale GmbH <info@indiscale.com>
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
"""API-Utils:

Some simplified functions for generation of records etc.
"""

import sys
import tempfile
import warnings
from collections.abc import Iterable
from subprocess import call

from typing import Optional, Any, Dict, List

from caosdb.common.datatype import (BOOLEAN, DATETIME, DOUBLE, FILE, INTEGER,
                                    REFERENCE, TEXT, is_reference)
from caosdb.common.models import (Container, Entity, File, Property, Query,
                                  Record, RecordType, execute_query,
                                  get_config, SPECIAL_ATTRIBUTES)

import logging


def new_record(record_type, name=None, description=None,
               tempid=None, insert=False, **kwargs):
    """Function to simplify the creation of Records.

    record_type: The name of the RecordType to use for this record.
                 (ids should also work.)
    name: Name of the new Record.
    kwargs: Key-value-pairs for the properties of this Record.

    Returns: The newly created Record.

    Of course this functions requires an open database connection!
    """

    rt = RecordType(name=record_type)
    rt.retrieve()

    r = Record(name)
    r.add_parent(rt)

    if tempid is not None:
        r.id = tempid

    if description is not None:
        r.description = description

    # Add all additional properties, treat iterables als multiple
    # additions.

    for k, v in kwargs.items():
        if hasattr(v, "encode") or not isinstance(v, Iterable):
            v = [v]

        for vv in v:
            p = Property(k)
            p.retrieve()
            p.value = vv
            r.add_property(p)

    if insert:
        r.insert()

    return r


def id_query(ids):
    warnings.warn("Please use 'create_id_query', which only creates"
                  "the string.", DeprecationWarning)

    return execute_query(create_id_query(ids))


def create_id_query(ids):
    return "FIND ENTITY WITH " + " OR ".join(
        ["ID={}".format(id) for id in ids])


def get_type_of_entity_with(id_):
    objs = retrieve_entities_with_ids([id_])

    if len(objs) == 0:
        raise RuntimeError("ID {} not found.".format(id_))

    if len(objs) > 1:
        raise RuntimeError(
            "ID {} is not unique. This is probably a bug in the CaosDB server." .format(id_))
    obj = objs[0]

    if isinstance(obj, Record):
        return Record
    elif isinstance(obj, RecordType):
        return RecordType
    elif isinstance(obj, Property):
        return Property
    elif isinstance(obj, File):
        return File
    elif isinstance(obj, Entity):
        return Entity


def retrieve_entity_with_id(eid):
    return execute_query("FIND ENTITY WITH ID={}".format(eid), unique=True)


def retrieve_entities_with_ids(entities):
    collection = Container()
    step = 20

    for i in range(len(entities)//step+1):
        collection.extend(
            execute_query(
                create_id_query(entities[i*step:(i+1)*step])))

    return collection


def getOriginUrlIn(folder):
    """return the Fetch URL of the git repository in the given folder."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as t:
        call(["git", "remote", "show", "origin"], stdout=t, cwd=folder)
    with open(t.name, "r") as t:
        urlString = "Fetch URL:"

        for line in t.readlines():
            if urlString in line:
                return line[line.find(urlString) + len(urlString):].strip()

    return None


def getDiffIn(folder, save_dir=None):
    """returns the name of a file where the out put of "git diff" in the given
    folder is stored."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w", dir=save_dir) as t:
        call(["git", "diff"], stdout=t, cwd=folder)

    return t.name


def getBranchIn(folder):
    """returns the current branch of the git repository in the given folder.

    The command "git branch" is called in the given folder and the
    output is returned
    """
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as t:
        call(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=t, cwd=folder)
    with open(t.name, "r") as t:
        return t.readline().strip()


def getCommitIn(folder):
    """returns the commit hash in of the git repository in the given folder.

    The command "git log -1 --format=%h" is called in the given folder
    and the output is returned
    """

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as t:
        call(["git", "log", "-1", "--format=%h"], stdout=t, cwd=folder)
    with open(t.name, "r") as t:
        return t.readline().strip()


def compare_entities(old_entity: Entity, new_entity: Entity):
    """
    Compare two entites.

    Return a tuple of dictionaries, the first index belongs to additional information for old
    entity, the second index belongs to additional information for new entity.

    Additional information means in detail:
    - Additional parents (a list under key "parents")
    - Information about properties:
      - Each property lists either an additional property or a property with a changed:
        - ... datatype
        - ... importance or
        - ... value (not implemented yet)
        In case of changed information the value listed under the respective key shows the
        value that is stored in the respective entity.
    """
    olddiff: Dict[str, Any] = {"properties": {}, "parents": []}
    newdiff: Dict[str, Any] = {"properties": {}, "parents": []}

    if old_entity is new_entity:
        return (olddiff, newdiff)

    for attr in SPECIAL_ATTRIBUTES:
        try:
            oldattr = old_entity.__getattribute__(attr)
            old_entity_attr_exists = True
        except BaseException:
            old_entity_attr_exists = False
        try:
            newattr = new_entity.__getattribute__(attr)
            new_entity_attr_exists = True
        except BaseException:
            new_entity_attr_exists = False

        if old_entity_attr_exists and (oldattr == "" or oldattr is None):
            old_entity_attr_exists = False

        if new_entity_attr_exists and (newattr == "" or newattr is None):
            new_entity_attr_exists = False

        if not old_entity_attr_exists and not new_entity_attr_exists:
            continue

        if ((old_entity_attr_exists ^ new_entity_attr_exists)
                or (oldattr != newattr)):

            if old_entity_attr_exists:
                olddiff[attr] = oldattr

            if new_entity_attr_exists:
                newdiff[attr] = newattr

    # properties

    for prop in old_entity.properties:
        matching = [p for p in new_entity.properties if p.name == prop.name]

        if len(matching) == 0:
            olddiff["properties"][prop.name] = {}
        elif len(matching) == 1:
            newdiff["properties"][prop.name] = {}
            olddiff["properties"][prop.name] = {}

            if (old_entity.get_importance(prop.name) !=
                    new_entity.get_importance(prop.name)):
                olddiff["properties"][prop.name]["importance"] = \
                    old_entity.get_importance(prop.name)
                newdiff["properties"][prop.name]["importance"] = \
                    new_entity.get_importance(prop.name)

            if (prop.datatype != matching[0].datatype):
                olddiff["properties"][prop.name]["datatype"] = prop.datatype
                newdiff["properties"][prop.name]["datatype"] = \
                    matching[0].datatype

            if (prop.unit != matching[0].unit):
                olddiff["properties"][prop.name]["unit"] = prop.unit
                newdiff["properties"][prop.name]["unit"] = \
                    matching[0].unit

            if (prop.value != matching[0].value):
                olddiff["properties"][prop.name]["value"] = prop.value
                newdiff["properties"][prop.name]["value"] = \
                    matching[0].value

            if (len(newdiff["properties"][prop.name]) == 0
                    and len(olddiff["properties"][prop.name]) == 0):
                newdiff["properties"].pop(prop.name)
                olddiff["properties"].pop(prop.name)

        else:
            raise NotImplementedError(
                "Comparison not implemented for multi-properties.")

    for prop in new_entity.properties:
        if len([0 for p in old_entity.properties if p.name == prop.name]) == 0:
            newdiff["properties"][prop.name] = {}

    # parents

    for parent in old_entity.parents:
        if len([0 for p in new_entity.parents if p.name == parent.name]) == 0:
            olddiff["parents"].append(parent.name)

    for parent in new_entity.parents:
        if len([0 for p in old_entity.parents if p.name == parent.name]) == 0:
            newdiff["parents"].append(parent.name)

    return (olddiff, newdiff)


def merge_entities(entity_a: Entity, entity_b: Entity):
    """
    Merge entity_b into entity_a such that they have the same parents and properties.

    datatype, unit, value, name and description will only be changed in entity_a if they
    are None for entity_a and set for entity_b. If there is a corresponding value
    for entity_a different from None a RuntimeError will be raised informing of an
    unresolvable merge conflict.

    The merge operation is done in place.

    Returns entity_a.

    WARNING: This function is currently experimental and insufficiently tested. Use with care.
    """

    logging.warning(
        "This function is currently experimental and insufficiently tested. Use with care.")

    # Compare both entities:
    diff_r1, diff_r2 = compare_entities(entity_a, entity_b)

    # Go through the comparison and try to apply changes to entity_a:
    for key in diff_r2["parents"]:
        entity_a.add_parent(entity_b.get_parent(key))

    for key in diff_r2["properties"]:
        if key in diff_r1["properties"]:
            if ("importance" in diff_r1["properties"][key] and
                    "importance" in diff_r2["properties"][key]):
                if (diff_r1["properties"][key]["importance"] !=
                        diff_r2["properties"][key]["importance"]):
                    raise NotImplementedError()
            elif ("importance" in diff_r1["properties"][key] or
                  "importance" in diff_r2["properties"][key]):
                raise NotImplementedError()

            for attribute in ("datatype", "unit", "value"):
                if diff_r1["properties"][key][attribute] is None:
                    setattr(entity_a.get_property(key), attribute,
                            diff_r2["properties"][key][attribute])
                else:
                    raise RuntimeError("Merge conflict.")
        else:
            # TODO: This is a temporary FIX for
            #       https://gitlab.indiscale.com/caosdb/src/caosdb-pylib/-/issues/105
            entity_a.add_property(id=entity_b.get_property(key).id,
                                  name=entity_b.get_property(key).name,
                                  datatype=entity_b.get_property(key).datatype,
                                  value=entity_b.get_property(key).value,
                                  unit=entity_b.get_property(key).unit,
                                  importance=entity_b.get_importance(key))
            # entity_a.add_property(
            #     entity_b.get_property(key),
            #     importance=entity_b.get_importance(key))

    for special_attribute in ("name", "description"):
        sa_a = getattr(entity_a, special_attribute)
        sa_b = getattr(entity_b, special_attribute)
        if sa_a != sa_b:
            if sa_a is None:
                setattr(entity_a, special_attribute, sa_b)
            else:
                raise RuntimeError("Merge conflict.")
    return entity_a


def describe_diff(olddiff, newdiff, name=None, as_update=True):
    description = ""

    for attr in list(set(list(olddiff.keys()) + list(newdiff.keys()))):
        if attr == "parents" or attr == "properties":
            continue
        description += "{} differs:\n".format(attr)
        description += "old version: {}\n".format(
            olddiff[attr] if attr in olddiff else "not set")
        description += "new version: {}\n\n".format(
            newdiff[attr] if attr in newdiff else "not set")

    if len(olddiff["parents"]) > 0:
        description += ("Parents that are only in the old version:\n"
                        + ", ".join(olddiff["parents"]))

    if len(newdiff["parents"]) > 0:
        description += ("Parents that are only in the new version:\n"
                        + ", ".join(olddiff["parents"]))

    for prop in list(set(list(olddiff["properties"].keys())
                         + list(newdiff["properties"].keys()))):
        description += "property {} differs:\n".format(prop)

        if prop not in olddiff["properties"]:
            description += "it does not exist in the old version: \n"
        elif prop not in newdiff["properties"]:
            description += "it does not exist in the new version: \n"
        else:
            description += "old version: {}\n".format(
                olddiff["properties"][prop])
            description += "new version: {}\n\n".format(
                newdiff["properties"][prop])

    if description != "":
        description = ("## Difference between the old and the new "
                       "version of {}\n\n".format(name))+description

    return description


def apply_to_ids(entities, func):
    """ Apply a function to all ids.

    All ids means the ids of the entities themselves but also to all parents,
    properties and referenced entities.

    Parameters
    ----------
    entities : list of Entity
    func : function with one parameter.
    """

    for entity in entities:
        _apply_to_ids_of_entity(entity, func)


def _apply_to_ids_of_entity(entity, func):
    entity.id = func(entity.id)

    for par in entity.parents:
        par.id = func(par.id)

    for prop in entity.properties:
        prop.id = func(prop.id)
        isref = is_reference(prop.datatype)

        if isref:
            if isinstance(prop.value, list):
                prop.value = [func(el) for el in prop.value]
            else:
                if prop.value is not None:
                    prop.value = func(prop.value)


def resolve_reference(prop: Property):
    """resolves the value of a reference property

    The integer value is replaced with the entity object.
    If the property is not a reference, then the function returns without
    change.
    """

    if not prop.is_reference(server_retrieval=True):
        return

    if isinstance(prop.value, list):
        referenced = []

        for val in prop.value:
            if isinstance(val, int):
                referenced.append(retrieve_entity_with_id(val))
            else:
                referenced.append(val)
        prop.value = referenced
    else:
        if isinstance(prop.value, int):
            prop.value = retrieve_entity_with_id(prop.value)


def create_flat_list(ent_list: List[Entity], flat: List[Entity]):
    """
    Recursively adds all properties contained in entities from ent_list to
    the output list flat. Each element will only be added once to the list.

    TODO: Currently this function is also contained in newcrawler module crawl.
          We are planning to permanently move it to here.
    """
    for ent in ent_list:
        for p in ent.properties:
            # For lists append each element that is of type Entity to flat:
            if isinstance(p.value, list):
                for el in p.value:
                    if isinstance(el, Entity):
                        if el not in flat:
                            flat.append(el)
                        # TODO: move inside if block?
                        create_flat_list([el], flat)
            elif isinstance(p.value, Entity):
                if p.value not in flat:
                    flat.append(p.value)
                # TODO: move inside if block?
                create_flat_list([p.value], flat)

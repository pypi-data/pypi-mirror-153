# -*- coding: utf-8 -*-
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2020-2022 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2022 Alexander Schlemmer <alexander.schlemmer@ds.mpg.de>
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

"""
A high level API for accessing CaosDB entities from within python.

This is refactored from apiutils.
"""

from caosdb.common.datatype import (BOOLEAN, DATETIME, DOUBLE, FILE, INTEGER,
                                    REFERENCE, TEXT,
                                    is_list_datatype,
                                    get_list_datatype,
                                    is_reference)
import caosdb as db

from .apiutils import get_type_of_entity_with, create_flat_list
import warnings

from typing import Any, Optional, List, Union, Dict

import yaml

from dataclasses import dataclass, fields
from datetime import datetime
from dateutil import parser

warnings.warn("""EXPERIMENTAL! The high_level_api module is experimental and may be changed or
removed in future. Its purpose is to give an impression on how the Python client user interface
might be changed.""")


def standard_type_for_high_level_type(high_level_record: "CaosDBPythonEntity",
                                      return_string: bool = False):
    """
    For a given CaosDBPythonEntity either return the corresponding
    class in the standard CaosDB API or - if return_string is True - return
    the role as a string.
    """
    if type(high_level_record) == CaosDBPythonRecord:
        if not return_string:
            return db.Record
        return "Record"
    elif type(high_level_record) == CaosDBPythonFile:
        if not return_string:
            return db.File
        return "File"
    elif type(high_level_record) == CaosDBPythonProperty:
        if not return_string:
            return db.Property
        return "Property"
    elif type(high_level_record) == CaosDBPythonRecordType:
        if not return_string:
            return db.RecordType
        return "RecordType"
    elif type(high_level_record) == CaosDBPythonEntity:
        if not return_string:
            return db.Entity
        return "Entity"
    raise RuntimeError("Incompatible type.")


def high_level_type_for_role(role: str):
    if role == "Record":
        return CaosDBPythonRecord
    if role == "File":
        return CaosDBPythonFile
    if role == "Property":
        return CaosDBPythonProperty
    if role == "RecordType":
        return CaosDBPythonRecordType
    if role == "Entity":
        return CaosDBPythonEntity
    raise RuntimeError("Unknown role.")


def high_level_type_for_standard_type(standard_record: db.Entity):
    if not isinstance(standard_record, db.Entity):
        raise ValueError()
    role = standard_record.role
    if role == "Record" or type(standard_record) == db.Record:
        return CaosDBPythonRecord
    elif role == "File" or type(standard_record) == db.File:
        return CaosDBPythonFile
    elif role == "Property" or type(standard_record) == db.Property:
        return CaosDBPythonProperty
    elif role == "RecordType" or type(standard_record) == db.RecordType:
        return CaosDBPythonRecordType
    elif role == "Entity" or type(standard_record) == db.Entity:
        return CaosDBPythonEntity
    raise RuntimeError("Incompatible type.")


@dataclass
class CaosDBPropertyMetaData:
    # name is already the name of the attribute
    unit: Optional[str] = None
    datatype: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None
    importance: Optional[str] = None


class CaosDBPythonUnresolved:
    pass


@dataclass
class CaosDBPythonUnresolvedParent(CaosDBPythonUnresolved):
    """
    Parents can be either given by name or by ID.

    When resolved, both fields should be set.
    """

    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class CaosDBPythonUnresolvedReference(CaosDBPythonUnresolved):

    def __init__(self, id=None):
        self.id = id


class CaosDBPythonEntity(object):

    def __init__(self):
        """
        Initialize a new CaosDBPythonEntity for the high level python api.

        Parents are either unresolved references or CaosDB RecordTypes.

        Properties are stored directly as attributes for the object.
        Property metadata is maintained in a dctionary _properties_metadata that should
        never be accessed directly, but only using the get_property_metadata function.
        If property values are references to other objects, they will be stored as
        CaosDBPythonUnresolvedReference objects that can be resolved later into
        CaosDBPythonRecords.
        """

        # Parents are either unresolved references or CaosDB RecordTypes
        self._parents: List[Union[
            CaosDBPythonUnresolvedParent, CaosDBPythonRecordType]] = []
        # self._id: int = CaosDBPythonEntity._get_new_id()
        self._id: Optional[int] = None
        self._name: Optional[str] = None
        self._description: Optional[str] = None
        self._version: Optional[str] = None

        self._file: Optional[str] = None
        self._path: Optional[str] = None

        # name: name of property, value: property metadata
        self._properties_metadata: Dict[CaosDBPropertyMetaData] = dict()

        # Store all current attributes as forbidden attributes
        # which must not be changed by the set_property function.
        self._forbidden = dir(self) + ["_forbidden"]

    def use_parameter(self, name, value):
        self.__setattr__(name, value)
        return value

    @property
    def id(self):
        """
        Getter for the id.
        """
        return self._id

    @id.setter
    def id(self, val: int):
        self._id = val

    @property
    def name(self):
        """
        Getter for the name.
        """
        return self._name

    @name.setter
    def name(self, val: str):
        self._name = val

    @property
    def file(self):
        """
        Getter for the file.
        """
        if type(self) != CaosDBPythonFile:
            raise RuntimeError("Please don't use the file attribute for entities"
                               " that are no files.")
        return self._file

    @file.setter
    def file(self, val: str):
        if val is not None and type(self) != CaosDBPythonFile:
            raise RuntimeError("Please don't use the file attribute for entities"
                               " that are no files.")
        self._file = val

    @property
    def path(self):
        """
        Getter for the path.
        """
        if type(self) != CaosDBPythonFile:
            raise RuntimeError("Please don't use the path attribute for entities"
                               " that are no files.")
        return self._path

    @path.setter
    def path(self, val: str):
        if val is not None and type(self) != CaosDBPythonFile:
            raise RuntimeError("Please don't use the path attribute for entities"
                               " that are no files.")
        self._path = val

    @property
    def description(self):
        """
        Getter for the description.
        """
        return self._description

    @description.setter
    def description(self, val: str):
        self._description = val

    @property
    def version(self):
        """
        Getter for the version.
        """
        return self._version

    @version.setter
    def version(self, val: str):
        self._version = val

    def _set_property_from_entity(self, ent: db.Entity, importance: str,
                                  references: Optional[db.Container]):
        """
        Set a new property using an entity from the normal python API.

        ent : db.Entity
              The entity to be set.
        """

        if ent.name is None:
            raise RuntimeError("Setting properties without name is impossible.")

        if ent.name in self.get_properties():
            raise RuntimeError("Multiproperty not implemented yet.")

        val = self._type_converted_value(ent.value, ent.datatype,
                                         references)
        self.set_property(
            ent.name,
            val,
            datatype=ent.datatype)
        metadata = self.get_property_metadata(ent.name)

        for prop_name in fields(metadata):
            k = prop_name.name
            if k == "importance":
                metadata.importance = importance
            else:
                metadata.__setattr__(k, ent.__getattribute__(k))

    def get_property_metadata(self, prop_name: str) -> CaosDBPropertyMetaData:
        """
        Retrieve the property metadata for the property with name prop_name.

        If the property with the given name does not exist or is forbidden, raise an exception.
        Else return the metadata associated with this property.

        If no metadata does exist yet for the given property, a new object will be created
        and returned.

        prop_name: str
                   Name of the property to retrieve metadata for.
        """

        if not self.property_exists(prop_name):
            raise RuntimeError("The property with name {} does not exist.".format(prop_name))

        if prop_name not in self._properties_metadata:
            self._properties_metadata[prop_name] = CaosDBPropertyMetaData()

        return self._properties_metadata[prop_name]

    def property_exists(self, prop_name: str):
        """
        Check whether a property exists already.
        """
        return prop_name not in self._forbidden and prop_name in self.__dict__

    def set_property(self,
                     name: str,
                     value: Any,
                     overwrite: bool = False,
                     datatype: Optional[str] = None):
        """
        Set a property for this entity with a name and a value.

        If this property is already set convert the value into a list and append the value.
        This behavior can be overwritten using the overwrite flag, which will just overwrite
        the existing value.

        name: str
              Name of the property.

        value: Any
               Value of the property.

        overwrite: bool
                   Use this if you definitely only want one property with
                   that name (set to True).
        """

        if name in self._forbidden:
            raise RuntimeError("Entity cannot be converted to a corresponding "
                               "Python representation. Name of property " +
                               name + " is forbidden!")

        already_exists = self.property_exists(name)

        if already_exists and not overwrite:
            # each call to set_property checks first if it already exists
            #        if yes: Turn the attribute into a list and
            #                place all the elements into that list.
            att = self.__getattribute__(name)

            if isinstance(att, list):
                # just append, see below
                pass
            else:
                old_att = self.__getattribute__(name)
                self.__setattr__(name, [old_att])
            att = self.__getattribute__(name)
            att.append(value)
        else:
            self.__setattr__(name, value)

    def __setattr__(self, name: str, val: Any):
        """
        Allow setting generic properties.
        """

        # TODO: implement checking the value to correspond to one of the datatypes
        #       known for conversion.

        super().__setattr__(name, val)

    def _type_converted_list(self,
                             val: List,
                             pr: str,
                             references: Optional[db.Container]):
        """
        Convert a list to a python list of the correct type.

        val: List
             The value of a property containing the list.

        pr: str
            The datatype according to the database entry.
        """
        if not is_list_datatype(pr) and not isinstance(val, list):
            raise RuntimeError("Not a list.")

        return [
            self._type_converted_value(i, get_list_datatype(pr), references
                                       ) for i in val]

    def _type_converted_value(self,
                              val: Any,
                              pr: str,
                              references: Optional[db.Container]):
        """
        Convert val to the correct type which is indicated by the database
        type string in pr.

        References with ids will be turned into CaosDBPythonUnresolvedReference.
        """

        if val is None:
            return None
        elif isinstance(val, db.Entity):
            # this needs to be checked as second case as it is the ONLY
            # case which does not depend on pr
            # TODO: we might need to pass through the reference container
            return convert_to_python_object(val, references)
        elif isinstance(val, list):
            return self._type_converted_list(val, pr, references)
        elif pr is None:
            return val
        elif pr == DOUBLE:
            return float(val)
        elif pr == BOOLEAN:
            return bool(val)
        elif pr == INTEGER:
            return int(val)
        elif pr == TEXT:
            return str(val)
        elif pr == FILE:
            return CaosDBPythonUnresolvedReference(val)
        elif pr == REFERENCE:
            return CaosDBPythonUnresolvedReference(val)
        elif pr == DATETIME:
            return self._parse_datetime(val)
        elif is_list_datatype(pr):
            return self._type_converted_list(val, pr, references)
        else:
            # Generic references to entities:
            return CaosDBPythonUnresolvedReference(val)

    def _parse_datetime(self, val: Union[str, datetime]):
        """
        Convert val into a datetime object.
        """
        if isinstance(val, datetime):
            return val
        return parser.parse(val)

    def get_property(self, name: str):
        """
        Return the value of the property with name name.

        Raise an exception if the property does not exist.
        """
        if not self.property_exists(name):
            raise RuntimeError("Property {} does not exist.".format(name))
        att = self.__getattribute__(name)
        return att

    def attribute_as_list(self, name: str):
        """
        This is a workaround for the problem that lists containing only one
        element are indistinguishable from simple types in this
        representation.

        TODO: still relevant? seems to be only a problem if LIST types are not used.
        """
        att = self.get_property(name)

        if isinstance(att, list):
            return att
        else:
            return [att]

    def add_parent(self, parent: Union[
            CaosDBPythonUnresolvedParent, "CaosDBPythonRecordType", str]):
        """
        Add a parent to this entity. Either using an unresolved parent or
        using a real record type.

        Strings as argument for parent will automatically be converted to an
        unresolved parent. Likewise, integers as argument will be automatically converted
        to unresolved parents with just an id.
        """

        if isinstance(parent, str):
            parent = CaosDBPythonUnresolvedParent(name=parent)

        if isinstance(parent, int):
            parent = CaosDBPythonUnresolvedParent(id=parent)

        if self.has_parent(parent):
            raise RuntimeError("Duplicate parent.")
        self._parents.append(parent)

    def get_parents(self):
        """
        Returns all parents of this entity.

        Use has_parent for checking for existence of parents
        and add_parent for adding parents to this entity.
        """
        return self._parents

    def has_parent(self, parent: Union[
            CaosDBPythonUnresolvedParent, "CaosDBPythonRecordType"]):
        """
        Check whether this parent already exists for this entity.

        Strings as argument for parent will automatically be converted to an
        unresolved parent. Likewise, integers as argument will be automatically converted
        to unresolved parents with just an id.
        """

        if isinstance(parent, str):
            parent = CaosDBPythonUnresolvedParent(name=parent)

        if isinstance(parent, int):
            parent = CaosDBPythonUnresolvedParent(id=parent)

        for p in self._parents:
            if p.id is not None and p.id == parent.id:
                return True
            elif p.name is not None and p.name == parent.name:
                return True
        return False

    def _resolve_caosdb_python_unresolved_reference(self, propval, deep,
                                                    references, visited):
        # This does not make sense for unset ids:
        if propval.id is None:
            raise RuntimeError("Unresolved property reference without an ID.")
        # have we encountered this id before:
        if propval.id in visited:
            # self.__setattr__(prop, visited[propval.id])
            # don't do the lookup in the references container
            return visited[propval.id]

        if references is None:
            ent = db.Entity(id=propval.id).retrieve()
            obj = convert_to_python_object(ent, references)
            visited[propval.id] = obj
            if deep:
                obj.resolve_references(deep, references, visited)
            return obj

        # lookup in container:
        for ent in references:
            # Entities in container without an ID will be skipped:
            if ent.id is not None and ent.id == propval.id:
                # resolve this entity:
                obj = convert_to_python_object(ent, references)
                visited[propval.id] = obj
                # self.__setattr__(prop, visited[propval.id])
                if deep:
                    obj.resolve_references(deep, references, visited)
                return obj
        return propval

    def resolve_references(self, deep: bool, references: db.Container,
                           visited: Dict[Union[str, int],
                                         "CaosDBPythonEntity"] = None):
        """
        Resolve this entity's references. This affects unresolved properties as well
        as unresolved parents.

        deep: bool
              If True recursively resolve references also for all resolved references.

        references: Optional[db.Container]
                    A container with references that might be resolved.
                    If None is passed as the container, this function tries to resolve entities from a running
                    CaosDB instance directly.
        """

        # This parameter is used in the recursion to keep track of already visited
        # entites (in order to detect cycles).
        if visited is None:
            visited = dict()

        for parent in self.get_parents():
            # TODO
            if isinstance(parent, CaosDBPythonUnresolvedParent):
                pass

        for prop in self.get_properties():
            propval = self.__getattribute__(prop)
            # Resolve all previously unresolved attributes that are entities:
            if deep and isinstance(propval, CaosDBPythonEntity):
                propval.resolve_references(deep, references)
            elif isinstance(propval, list):
                resolvedelements = []
                for element in propval:
                    if deep and isinstance(element, CaosDBPythonEntity):
                        element.resolve_references(deep, references)
                        resolvedelements.append(element)
                    if isinstance(element, CaosDBPythonUnresolvedReference):
                        resolvedelements.append(
                            self._resolve_caosdb_python_unresolved_reference(element, deep,
                                                                             references, visited))
                    else:
                        resolvedelements.append(element)
                self.__setattr__(prop, resolvedelements)

            elif isinstance(propval, CaosDBPythonUnresolvedReference):
                val = self._resolve_caosdb_python_unresolved_reference(propval, deep,
                                                                       references, visited)
                self.__setattr__(prop, val)

    def get_properties(self):
        """
        Return the names of all properties.
        """

        return [p for p in self.__dict__
                if p not in self._forbidden]

    @staticmethod
    def deserialize(serialization: dict):
        """
        Deserialize a yaml representation of an entity in high level API form.
        """

        if "role" in serialization:
            entity = high_level_type_for_role(serialization["role"])()
        else:
            entity = CaosDBPythonRecord()

        for parent in serialization["parents"]:
            if "unresolved" in parent:
                id = None
                name = None
                if "id" in parent:
                    id = parent["id"]
                if "name" in parent:
                    name = parent["name"]
                entity.add_parent(CaosDBPythonUnresolvedParent(
                    id=id, name=name))
            else:
                raise NotImplementedError()

        for baseprop in ("name", "id", "description", "version"):
            if baseprop in serialization:
                entity.__setattr__(baseprop, serialization[baseprop])

        if type(entity) == CaosDBPythonFile:
            entity.file = serialization["file"]
            entity.path = serialization["path"]

        for p in serialization["properties"]:
            # The property needs to be set first:

            prop = serialization["properties"][p]
            if isinstance(prop, dict):
                if "unresolved" in prop:
                    entity.__setattr__(p, CaosDBPythonUnresolvedReference(
                        id=prop["id"]))
                else:
                    entity.__setattr__(p,
                                       entity.deserialize(prop))
            else:
                entity.__setattr__(p, prop)

            # if there is no metadata in the yaml file just initialize an empty metadata object
            if "metadata" in serialization and p in serialization["metadata"]:
                metadata = serialization["metadata"][p]
                propmeta = entity.get_property_metadata(p)

                for f in fields(propmeta):
                    if f.name in metadata:
                        propmeta.__setattr__(f.name, metadata[f.name])
            else:
                raise NotImplementedError()

        return entity

    def serialize(self, without_metadata: bool = False, visited: dict = None):
        """
        Serialize necessary information into a dict.

        without_metadata: bool
                          If True don't set the metadata field in order to increase
                          readability. Not recommended if deserialization is needed.
        """

        if visited is None:
            visited = dict()

        if self in visited:
            return visited[self]

        metadata: Dict[str, Any] = dict()
        properties = dict()
        parents = list()

        # The full information to be returned:
        fulldict = dict()
        visited[self] = fulldict

        # Add CaosDB role:
        fulldict["role"] = standard_type_for_high_level_type(self, True)

        for parent in self._parents:
            if isinstance(parent, CaosDBPythonEntity):
                parents.append(parent.serialize(without_metadata, visited))
            elif isinstance(parent, CaosDBPythonUnresolvedParent):
                parents.append({"name": parent.name, "id": parent.id,
                                "unresolved": True})
            else:
                raise RuntimeError("Incompatible class used as parent.")

        for baseprop in ("name", "id", "description", "version"):
            val = self.__getattribute__(baseprop)
            if val is not None:
                fulldict[baseprop] = val

        if type(self) == CaosDBPythonFile:
            fulldict["file"] = self.file
            fulldict["path"] = self.path

        for p in self.get_properties():
            m = self.get_property_metadata(p)
            metadata[p] = dict()
            for f in fields(m):
                val = m.__getattribute__(f.name)
                if val is not None:
                    metadata[p][f.name] = val

            val = self.get_property(p)
            if isinstance(val, CaosDBPythonUnresolvedReference):
                properties[p] = {"id": val.id, "unresolved": True}
            elif isinstance(val, CaosDBPythonEntity):
                properties[p] = val.serialize(without_metadata, visited)
            elif isinstance(val, list):
                serializedelements = []
                for element in val:
                    if isinstance(element, CaosDBPythonUnresolvedReference):
                        elm = dict()
                        elm["id"] = element.id
                        elm["unresolved"] = True
                        serializedelements.append(elm)
                    elif isinstance(element, CaosDBPythonEntity):
                        serializedelements.append(
                            element.serialize(without_metadata,
                                              visited))
                    else:
                        serializedelements.append(element)
                properties[p] = serializedelements
            else:
                properties[p] = val

        fulldict["properties"] = properties
        fulldict["parents"] = parents

        if not without_metadata:
            fulldict["metadata"] = metadata
        return fulldict

    def __str__(self):
        return yaml.dump(self.serialize(False))

    # This seemed like a good solution, but makes it difficult to
    # compare python objects directly:
    #
    # def __repr__(self):
    #     return yaml.dump(self.serialize(True))


class CaosDBPythonRecord(CaosDBPythonEntity):
    pass


class CaosDBPythonRecordType(CaosDBPythonEntity):
    pass


class CaosDBPythonProperty(CaosDBPythonEntity):
    pass


class CaosDBMultiProperty:
    """
    This implements a multi property using a python list.
    """

    def __init__(self):
        raise NotImplementedError()


class CaosDBPythonFile(CaosDBPythonEntity):
    def download(self, target=None):
        if self.id is None:
            raise RuntimeError("Cannot download file when id is missing.")
        f = db.File(id=self.id).retrieve()
        return f.download(target)


BASE_ATTRIBUTES = (
    "id", "name", "description", "version", "path", "file")


def _single_convert_to_python_object(robj: CaosDBPythonEntity,
                                     entity: db.Entity,
                                     references: Optional[db.Container] = None):
    """
    Convert a db.Entity from the standard API to a (previously created)
    CaosDBPythonEntity from the high level API.

    This method will not resolve any unresolved references, so reference properties
    as well as parents will become unresolved references in the first place.

    The optional third parameter can be used
    to resolve references that occur in the converted entities and resolve them
    to their correct representations. (Entities that are not found remain as
    CaosDBPythonUnresolvedReferences.)

    Returns the input object robj.
    """
    for base_attribute in BASE_ATTRIBUTES:
        val = entity.__getattribute__(base_attribute)
        if val is not None:
            if isinstance(val, db.common.models.Version):
                val = val.id
            robj.__setattr__(base_attribute, val)

    for prop in entity.properties:
        robj._set_property_from_entity(prop, entity.get_importance(prop), references)

    for parent in entity.parents:
        robj.add_parent(CaosDBPythonUnresolvedParent(id=parent.id,
                                                     name=parent.name))

    return robj


def _convert_property_value(propval):
    if isinstance(propval, CaosDBPythonUnresolvedReference):
        propval = propval.id
    elif isinstance(propval, CaosDBPythonEntity):
        propval = _single_convert_to_entity(
            standard_type_for_high_level_type(propval)(), propval)
    elif isinstance(propval, list):
        propval = [_convert_property_value(element) for element in propval]

    # TODO: test case for list missing

    return propval


def _single_convert_to_entity(entity: db.Entity,
                              robj: CaosDBPythonEntity):
    """
    Convert a CaosDBPythonEntity to an entity in standard pylib format.

    entity: db.Entity
            An empty entity.

    robj: CaosDBPythonEntity
          The CaosDBPythonEntity that is supposed to be converted to the entity.
    """

    for base_attribute in BASE_ATTRIBUTES:
        if base_attribute in ("file", "path") and not isinstance(robj, CaosDBPythonFile):
            continue

        # Skip version:
        if base_attribute == "version":
            continue

        val = robj.__getattribute__(base_attribute)

        if val is not None:
            entity.__setattr__(base_attribute, val)

    for parent in robj.get_parents():
        if isinstance(parent, CaosDBPythonUnresolvedParent):
            entity.add_parent(name=parent.name, id=parent.id)
        elif isinstance(parent, CaosDBPythonRecordType):
            raise NotImplementedError()
        else:
            raise RuntimeError("Incompatible class used as parent.")

    for prop in robj.get_properties():
        propval = robj.__getattribute__(prop)
        metadata = robj.get_property_metadata(prop)

        propval = _convert_property_value(propval)

        entity.add_property(
            name=prop,
            value=propval,
            unit=metadata.unit,
            importance=metadata.importance,
            datatype=metadata.datatype,
            description=metadata.description,
            id=metadata.id)

    return entity


def convert_to_entity(python_object):
    if isinstance(python_object, db.Container):
        # Create a list of objects:

        return [convert_to_entity(i) for i in python_object]
    elif isinstance(python_object, CaosDBPythonRecord):
        return _single_convert_to_entity(db.Record(), python_object)
    elif isinstance(python_object, CaosDBPythonFile):
        return _single_convert_to_entity(db.File(), python_object)
    elif isinstance(python_object, CaosDBPythonRecordType):
        return _single_convert_to_entity(db.RecordType(), python_object)
    elif isinstance(python_object, CaosDBPythonProperty):
        return _single_convert_to_entity(db.Property(), python_object)
    elif isinstance(python_object, CaosDBPythonEntity):
        return _single_convert_to_entity(db.Entity(), python_object)
    else:
        raise ValueError("Cannot convert an object of this type.")


def convert_to_python_object(entity: Union[db.Container, db.Entity],
                             references: Optional[db.Container] = None):
    """
    Convert either a container of CaosDB entities or a single CaosDB entity
    into the high level representation.

    The optional second parameter can be used
    to resolve references that occur in the converted entities and resolve them
    to their correct representations. (Entities that are not found remain as
    CaosDBPythonUnresolvedReferences.)
    """
    if isinstance(entity, db.Container):
        # Create a list of objects:
        return [convert_to_python_object(i, references) for i in entity]

    return _single_convert_to_python_object(
        high_level_type_for_standard_type(entity)(), entity, references)


def new_high_level_entity(entity: db.RecordType,
                          importance_level: str,
                          name: str = None):
    """
    Create an new record in high level format based on a record type in standard format.

    entity: db.RecordType
            The record type to initialize the new record from.

    importance_level: str
                      None, obligatory, recommended or suggested
                      Initialize new properties up to this level.
                      Properties in the record type with no importance will be added
                      regardless of the importance_level.

    name: str
          Name of the new record.
    """

    r = db.Record(name=name)
    r.add_parent(entity)

    impmap = {
        None: 0, "SUGGESTED": 3, "RECOMMENDED": 2, "OBLIGATORY": 1}

    for prop in entity.properties:
        imp = entity.get_importance(prop)
        if imp is not None and impmap[importance_level] < impmap[imp]:
            continue

        r.add_property(prop)

    return convert_to_python_object(r)


def create_record(rtname: str, name: str = None, **kwargs):
    """
    Create a new record based on the name of a record type. The new record is returned.

    rtname: str
            The name of the record type.

    name: str
          This is optional. A name for the new record.

    kwargs:
            Additional arguments are used to set attributes of the
            new record.
    """
    obj = new_high_level_entity(
        db.RecordType(name=rtname).retrieve(), "SUGGESTED", name)
    for key, value in kwargs.items():
        obj.__setattr__(key, value)
    return obj


def load_external_record(record_name: str):
    """
    Retrieve a record by name and convert it to the high level API format.
    """
    return convert_to_python_object(db.Record(name=record_name).retrieve())


def create_entity_container(record: CaosDBPythonEntity):
    """
    Convert this record into an entity container in standard format that can be used
    to insert or update entities in a running CaosDB instance.
    """
    ent = convert_to_entity(record)
    lse: List[db.Entity] = [ent]
    create_flat_list([ent], lse)
    return db.Container().extend(lse)


def query(query: str, resolve_references: bool = True, references: db.Container = None):
    """

    """
    res = db.execute_query(query)
    objects = convert_to_python_object(res)
    if resolve_references:
        for obj in objects:
            obj.resolve_references(True, references)
    return objects

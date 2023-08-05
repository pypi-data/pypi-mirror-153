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

"""provides utilities for creating revisions of database entries."""
import caosdb as db
from caosdb import INTEGER, LIST


def bend_references(from_id, to_id, except_for=None):
    """redirects all references to a new target.

    All entities having a reference pointing to from_id are found
    and those references are changed to point to to_id.
    entities having an id listed in except_for are excluded.

    params:
    from_id : int
        the old object to which references where pointing
    to_id : int
        the new object to which references will be pointing
    except_for : list of int
        entities with id of this list will not be changed
    """
    if except_for is None:
        except_for = [to_id]
    entities = db.execute_query(
        "FIND ENTITY WHICH references {}".format(from_id))
    for ent in entities:
        if ent.id in except_for:
            continue
        for prop in ent.properties:
            if isinstance(
                    prop.value, int) and (
                        prop.datatype != INTEGER) and (
                            prop.value == from_id):
                prop.value = to_id
            if (isinstance(prop.value, list)
                    and len(prop.value) > 0
                    and isinstance(prop.value[0], int)
                    and (prop.datatype != LIST(INTEGER))
                    and from_id in prop.value):
                index = prop.value.index(from_id)
                prop.value[index] = to_id
        ent.update()


def create_revision(old_id, prop, value):
    """creates a revision of an existing record.

    This function changes the record with id old_id. The value of the
    propertye prop is changed to value.

    params:
    old_id : int
        id of the record to be changed
    prop : string
        name of the property to be changed
    value : type of corresponding property
        the new value of the corresponding property
    """
    record = db.execute_query("FIND {}".format(old_id))[0]
    new_rec = record.copy()
    new_rec.get_property(prop).value = value
    try:
        new_rec.remove_property("revisionOf")
    except BaseException:
        pass
    new_rec.add_property(name="revisionOf", value=record.id)
    new_rec.insert()
    bend_references(record.id, new_rec.id)

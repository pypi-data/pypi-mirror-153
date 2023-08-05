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

"""Utilities for work with PlantUML.

PlantUML (http://plantuml.com) is a converter from a simple
descriptive language to graphviz diagrams.

To convert the output, you can write it into FILENAME.pu and then
convert it with:

plantuml FILENAME.pu -> FILENAME.png
"""

import os
import shutil

import caosdb as db
from caosdb.common.datatype import is_reference, get_referenced_recordtype

from typing import List, Optional

import tempfile

REFERENCE = "REFERENCE"


def get_description(description_str):
    """Extract and format a description string from a record type or property.

    Parameters
    ----------
    description_str : str
                      The description string that is going to be formatted.

    Returns
    -------
    str
       The reformatted description ending in a line break.
    """
    words = description_str.split()
    lines = []
    lines.append("")

    for w in words:
        if len(lines[-1] + w) > 60:
            lines.append("")

        if len(lines[-1]) > 0:
            lines[-1] += " "
        lines[-1] += w
    description = "\n".join(lines)

    return description + "\n"


class Grouped(object):
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents

    def get_parents(self):
        return self.parents


def recordtypes_to_plantuml_string(iterable,
                                   add_properties: bool = True,
                                   add_recordtypes: bool = True,
                                   add_legend: bool = True,
                                   no_shadow: bool = False,
                                   style: str = "default"):
    """Converts RecordTypes into a string for PlantUML.

    This function obtains an iterable and returns a string which can
    be input into PlantUML for a representation of all RecordTypes in
    the iterable.

    Current options for style
    -------------------------

    "default" - Standard rectangles with uml class circle and methods section
    "salexan" - Round rectangles, hide circle and methods section

    Current limitations
    -------------------

    - It is inherently hard to detect if an element should be rendered
      as a class/RecordType or not.  Currently it is rendered if
      either the "type" attribute is None or
      type(element) == RecordType.
    - Inheritance of Properties is not rendered nicely at the moment.

    Parameters
    ----------
    iterable: iterable of caosdb.Entity
      The objects to be rendered with plantuml.

    no_shadow : bool, optional
      If true, tell plantuml to use a skin without blurred shadows.


    Returns
    -------
    out : str
      The plantuml string for the given container.
    """

    # TODO: This function needs a review of python type hints.

    classes = [el for el in iterable
               if isinstance(el, db.RecordType)]
    dependencies = {}
    inheritances = {}
    properties = [p for p in iterable if isinstance(p, db.Property)]
    grouped = [g for g in iterable if isinstance(g, Grouped)]

    def _add_properties(c, importance=None):
        result = ""

        for p in c.get_properties():
            if importance is None or c.get_properties().get_importance(p) == importance:
                if importance is not None and len(result) == 0:
                    result += ".." + importance.lower() + "..\n"
                name = p.name
                p_type = p.datatype

                if p_type is None:
                    # get type from properties

                    for p2 in properties:
                        if p2.name == p.name:
                            p_type = p2.datatype

                if p_type is None:
                    # is reference?

                    for p2 in classes:
                        if p2.name == p.name:
                            p_type = p2

                if isinstance(p_type, db.Entity):
                    p_type = p_type.name
                    dependencies[c].append(p_type)
                elif p_type is not None:
                    for c2 in classes:
                        if c2.name == p_type or db.LIST(c2.name) == p_type:
                            dependencies[c].append(c2.name)
                result += '  {name} ({type})\n'.format(
                    name=name, type=p_type)

        return result

    result = "@startuml\n\n"

    if no_shadow:
        result += "skinparam shadowing false\n"

    if style == "default":
        result += "skinparam classAttributeIconSize 0\n"
    elif style == "salexan":
        result += """skinparam roundcorner 20\n
skinparam boxpadding 20\n
\n
hide methods\n
hide circle\n
"""
    else:
        raise ValueError("Unknown style.")

    if add_properties:
        result += "package Properties #DDDDDD {\n"
        for p in properties:
            inheritances[p] = p.get_parents()
            dependencies[p] = []

            result += "class \"{klass}\" << (P,#008800) >> {{\n".format(klass=p.name)

            if p.description is not None:
                result += get_description(p.description)
            result += "\n..\n"

            if isinstance(p.datatype, str):
                result += "datatype: " + p.datatype + "\n"
            elif isinstance(p.datatype, db.Entity):
                result += "datatype: " + p.datatype.name + "\n"
            else:
                result += "datatype: " + str(p.datatype) + "\n"
            result += "}\n\n"
        result += "}\n\n"

    if add_recordtypes:
        result += "package RecordTypes #DDDDDD {\n"

        for c in classes:
            inheritances[c] = c.get_parents()
            dependencies[c] = []
            result += "class \"{klass}\" << (C,#FF1111) >> {{\n".format(klass=c.name)

            if c.description is not None:
                result += get_description(c.description)

            props = ""
            props += _add_properties(c, importance=db.FIX)
            props += _add_properties(c, importance=db.OBLIGATORY)
            props += _add_properties(c, importance=db.RECOMMENDED)
            props += _add_properties(c, importance=db.SUGGESTED)

            if len(props) > 0:
                result += "__Properties__\n" + props
            else:
                result += "\n..\n"
            result += "}\n\n"

        for g in grouped:
            inheritances[g] = g.get_parents()
            result += "class \"{klass}\" << (G,#0000FF) >> {{\n".format(klass=g.name)
        result += "}\n\n"

        for c, parents in inheritances.items():
            for par in parents:
                result += "\"{par}\" <|-- \"{klass}\"\n".format(
                    klass=c.name, par=par.name)

        for c, deps in dependencies.items():
            for dep in deps:
                result += "\"{klass}\" *-- \"{dep}\"\n".format(
                    klass=c.name, dep=dep)

    if add_legend:
        result += """

package \"B is a subtype of A\" <<Rectangle>> {
 A <|-right- B
 note  "This determines what you find when you query for the RecordType.\\n'FIND RECORD A' will provide Records which have a parent\\nA or B, while 'FIND RECORD B' will provide only Records which have a parent B." as N1
}
"""
        result += """

package \"The property P references an instance of D\" <<Rectangle>> {
 class C {
    P(D)
 }
 C *-right- D
 note  "Employ this when searching for C: 'FIND RECORD C WITH D'\\nOr if the value of D is a Record: 'FIND RECORD C WHICH REFERENCES D' is possible.\\nEmploying this while searching for D: 'FIND RECORD D WHICH IS REFERENCED BY C" as N2
}

"""

    result += "\n@enduml\n"

    return result


def retrieve_substructure(start_record_types, depth, result_id_set=None, result_container=None, cleanup=True):
    """Recursively retrieves CaosDB record types and properties, starting
    from given initial types up to a specific depth.

    Parameters
    ----------
    start_record_types : Iterable[db.Entity]
                         Iterable with the entities to be displayed. Starting from these
                         entities more entities will be retrieved.
    depth : int
            The maximum depth up to which to retriev sub entities.
    result_id_set : set[int]
                    Used by recursion. Filled with already visited ids.
    result_container : db.Container
                       Used by recursion. Filled with already visited entities.
    cleanup : bool
              Used by recursion. If True return the resulting result_container.
              Don't return anything otherwise.

    Returns
    -------
    db.Container
                A container containing all the retrieved entites
                or None if cleanup is False.
    """
    # Initialize the id set and result container for level zero recursion depth:
    if result_id_set is None:
        result_id_set = set()
    if result_container is None:
        result_container = db.Container()

    for entity in start_record_types:
        entity.retrieve()
        if entity.id not in result_id_set:
            result_container.append(entity)
        result_id_set.add(entity.id)
        for prop in entity.properties:
            if (is_reference(prop.datatype) and prop.datatype != db.FILE and depth > 0):
                rt = db.RecordType(
                    name=get_referenced_recordtype(prop.datatype)).retrieve()
                retrieve_substructure([rt], depth-1, result_id_set,
                                      result_container, False)
            # TODO: clean up this hack
            # TODO: make it also work for files
            if is_reference(prop.datatype) and prop.value is not None:
                r = db.Record(id=prop.value).retrieve()
                retrieve_substructure([r], depth-1, result_id_set, result_container, False)
                if r.id not in result_id_set:
                    result_container.append(r)
                    result_id_set.add(r.id)

            if prop.id not in result_id_set:
                result_container.append(prop)
                result_id_set.add(prop.id)

        for parent in entity.parents:
            rt = db.RecordType(id=parent.id).retrieve()
            if parent.id not in result_id_set:
                result_container.append(rt)
            result_id_set.add(parent.id)
            if depth > 0:
                retrieve_substructure([rt], depth-1, result_id_set,
                                      result_container, False)

    if cleanup:
        return result_container
    return None


def to_graphics(recordtypes: List[db.Entity], filename: str,
                output_dirname: Optional[str] = None,
                formats: List[str] = ["tsvg"],
                silent: bool = True,
                add_properties: bool = True,
                add_recordtypes: bool = True,
                add_legend: bool = True,
                no_shadow: bool = False,
                style: str = "default"):
    """Calls recordtypes_to_plantuml_string(), saves result to file and
    creates an svg image

    plantuml needs to be installed.

    Parameters
    ----------
    recordtypes : Iterable[db.Entity]
                  Iterable with the entities to be displayed.
    filename : str
               filename of the image without the extension(e.g. data_structure;
               also without the preceeding path.
               data_structure.pu and data_structure.svg will be created.)
    output_dirname : str
                     the destination directory for the resulting images as defined by the "-o"
                     option by plantuml
                     default is to use current working dir
    formats : List[str]
              list of target formats as defined by the -t"..." options by plantuml, e.g. "tsvg"
    silent : bool
             Don't output messages.
    no_shadow : bool, optional
      If true, tell plantuml to use a skin without blurred shadows.
    """
    pu = recordtypes_to_plantuml_string(iterable=recordtypes,
                                        add_properties=add_properties,
                                        add_recordtypes=add_recordtypes,
                                        add_legend=add_legend,
                                        no_shadow=no_shadow,
                                        style=style)

    if output_dirname is None:
        output_dirname = os.getcwd()

    allowed_formats = [
        "tpng", "tsvg", "teps", "tpdf", "tvdx", "txmi",
        "tscxml", "thtml", "ttxt", "tutxt", "tlatex", "tlatex:nopreamble"]

    with tempfile.TemporaryDirectory() as td:

        pu_filename = os.path.join(td, filename + ".pu")
        with open(pu_filename, "w") as pu_file:
            pu_file.write(pu)

        for format in formats:
            extension = format[1:]
            if ":" in extension:
                extension = extension[:extension.index(":")]

            if format not in allowed_formats:
                raise RuntimeError("Format not allowed.")
            cmd = "plantuml -{} {}".format(format, pu_filename)
            if not silent:
                print("Executing:", cmd)

            if os.system(cmd) != 0:  # TODO: replace with subprocess.run
                raise Exception("An error occured during the execution of "
                                "plantuml when using the format {}. "
                                "Is plantuml installed? "
                                "You might want to dry a different format.".format(format))
            # copy only the final product into the target directory
            shutil.copy(os.path.join(td, filename + "." + extension),
                        output_dirname)

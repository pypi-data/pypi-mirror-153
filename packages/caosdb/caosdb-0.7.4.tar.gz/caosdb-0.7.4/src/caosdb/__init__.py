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

"""CaosDB Python bindings.

Tries to read from the inifile specified in the environment variable `PYCAOSDBINI` or alternatively
in `~/.pycaosdb.ini` upon import.  After that, the ini file `pycaosdb.ini` in the current working
directory will be read additionally, if it exists.
"""

from os import environ, getcwd
# Import of the connection function (which is used to connect to the DB):
from os.path import expanduser, join

# Import of convenience methods:
import caosdb.apiutils
from caosdb.common import administration
from caosdb.common.datatype import (BOOLEAN, DATETIME, DOUBLE, FILE, INTEGER,
                                    LIST, REFERENCE, TEXT)
from caosdb.common.state import State, Transition
# Import of the basic  API classes:
from caosdb.common.models import (ACL, ALL, FIX, NONE, OBLIGATORY, RECOMMENDED,
                                  SUGGESTED, Container, DropOffBox, Entity,
                                  File, Info, Message, Permissions, Property,
                                  Query, QueryTemplate, Record, RecordType,
                                  delete, execute_query, get_global_acl,
                                  get_known_permissions, raise_errors)
from caosdb.configuration import _read_config_files, configure, get_config
from caosdb.connection.connection import configure_connection, get_connection
from caosdb.exceptions import *
try:
    from caosdb.version import version as __version__
except ModuleNotFoundError:
    version = "uninstalled"
    __version__ = version

_read_config_files()

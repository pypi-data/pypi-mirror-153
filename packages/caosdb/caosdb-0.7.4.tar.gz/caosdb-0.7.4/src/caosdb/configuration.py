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

import os
import yaml
import warnings
try:
    optional_jsonschema_validate = None
    from jsonschema import validate as optional_jsonschema_validate
except ImportError:
    pass

try:
    # python2
    from ConfigParser import ConfigParser
except ImportError:
    # python3
    from configparser import ConfigParser

from os import environ, getcwd
from os.path import expanduser, join, isfile


def _reset_config():
    global _pycaosdbconf
    _pycaosdbconf = ConfigParser(allow_no_value=False)


def configure(inifile):
    """read config from file.

    Return a list of files which have successfully been parsed.
    """
    global _pycaosdbconf
    if "_pycaosdbconf" not in globals():
        _pycaosdbconf = None
    if _pycaosdbconf is None:
        _reset_config()
    read_config = _pycaosdbconf.read(inifile)
    validate_yaml_schema(config_to_yaml(_pycaosdbconf))
    return read_config


def get_config():
    global _pycaosdbconf
    return _pycaosdbconf


def config_to_yaml(config):
    valobj = {}
    for s in config.sections():
        valobj[s] = {}
        for key, value in config[s].items():
            # TODO: Can the type be inferred from the config object?
            if key in ["timeout", "debug"]:
                valobj[s][key] = int(value)
            elif key in ["ssl_insecure"]:
                valobj[s][key] = bool(value)
            else:
                valobj[s][key] = value

    return valobj


def validate_yaml_schema(valobj):
    if optional_jsonschema_validate:
        with open(os.path.join(os.path.dirname(__file__), "schema-pycaosdb-ini.yml")) as f:
            schema = yaml.load(f, Loader=yaml.SafeLoader)
        optional_jsonschema_validate(instance=valobj, schema=schema["schema-pycaosdb-ini"])
    else:
        warnings.warn("""
            Warning: The validation could not be performed because `jsonschema` is not installed.
        """)


def _read_config_files():
    """Function to read config files from different paths.

    Checks for path either in ``$PYCAOSDBINI`` or home directory (``.pycaosdb.ini``), and
    additionally in the current working directory (``pycaosdb.ini``).

    Returns
    -------

    ini files: list
      The successfully parsed ini-files. Order: env_var or home directory, cwd. Used for testing the function.

    """
    return_var = []
    if "PYCAOSDBINI" in environ:
        return_var.extend(configure(expanduser(environ["PYCAOSDBINI"])))
    else:
        return_var.extend(configure(expanduser('~/.pycaosdb.ini')))

    if isfile(join(getcwd(), "pycaosdb.ini")):
        return_var.extend(configure(join(getcwd(), "pycaosdb.ini")))
    return return_var

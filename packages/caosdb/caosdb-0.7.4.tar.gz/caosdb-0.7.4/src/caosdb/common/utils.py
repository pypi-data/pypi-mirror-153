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

"""mising docstring."""
from lxml import etree
from multiprocessing import Lock
from uuid import uuid4
from sys import hexversion
_uuid_lock = Lock()


def xml2str(xml):
    return etree.tostring(xml, pretty_print=True, encoding='unicode')


def uuid():
    exc = None
    ret = None
    try:
        _uuid_lock.acquire()
        ret = uuid4()
    except Exception as e:
        exc = e
    finally:
        _uuid_lock.release()
        if exc:
            raise exc
    return ret


def is_int(obj):
    try:
        int(obj)
        return True
    except ValueError:
        return False

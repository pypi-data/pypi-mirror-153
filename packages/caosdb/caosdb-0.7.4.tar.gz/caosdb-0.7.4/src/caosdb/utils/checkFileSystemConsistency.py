#!/usr/bin/python
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

"""requests the server to execute checkFileSystemConsistency job."""

import sys
import caosdb as db

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from _testcapi import raise_exception

__all__ = []
__version__ = 0.1
__date__ = '2016-08-31'
__updated__ = '2016-09-01'


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def runCheck(timeout, location):
    """ Request the caosdb server to check the file system for consistency.

    location == None means that the whole file system is being checked.
    Otherwise only a the directory tree under location is being checked.
    """

    if (timeout is not None):
        db.get_config().set("Connection", "timeout", str(100 + int(timeout)))
    files = db.Container().retrieve(
        unique=False, raise_exception_on_error=False, flags={
            "fileStorageConsistency": (
                "-t " + str(timeout) if timeout else "") + (
                location if location else ""), })
    return files


def main(argv=None):
    """Command line options."""

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by timm fitschen on %s.
  Copyright 2016 BMPG. All rights reserved.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        help="set verbosity level [default: %(default)s]",
        default=0)
    parser.add_argument('-V', '--version', action='version',
                        version=program_version_message)
    parser.add_argument(
        '-t',
        '--timeout',
        dest="timeout",
        help="timeout in seconds for the database requests. [default: %(default)s]",
        metavar="TIMEOUT",
        default="200")

    # Process arguments
    args = parser.parse_args()
    global VERBOSITY

    VERBOSITY = args.verbose
    TIMEOUT = args.timeout

    runCheck(TIMEOUT)

    return 0


if __name__ == "__main__":
    sys.exit(main())

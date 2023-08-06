# Copyright 2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.restful
#
# lazr.restful is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.restful is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.restful.  If not, see <http://www.gnu.org/licenses/>.
"Test harness for doctests."

# pylint: disable=E0611,W0142

__all__ = []

import atexit
import doctest
import os
import re

from pkg_resources import (
    resource_filename,
    resource_exists,
    resource_listdir,
    cleanup_resources,
)
from zope.testing import renormalizing
from zope.testing.cleanup import cleanUp


DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


checker = renormalizing.OutputChecker(
    [
        (re.compile(r"__builtin__\."), "builtins."),
    ]
)


def tearDown(test):
    """Run registered clean-up function."""
    cleanUp()


def load_tests(loader, tests, pattern):
    "Run the doc tests (README.txt and docs/*, if any exist)"
    doctest_files = []
    if resource_exists("lazr.restful", "docs"):
        for name in resource_listdir("lazr.restful", "docs"):
            if name.endswith(".rst"):
                doctest_files.append(
                    os.path.abspath(
                        resource_filename("lazr.restful", "docs/%s" % name)
                    )
                )
    atexit.register(cleanup_resources)
    tests.addTest(
        doctest.DocFileSuite(
            *doctest_files,
            module_relative=False,
            optionflags=DOCTEST_FLAGS,
            tearDown=tearDown,
            encoding="UTF-8",
            checker=checker,
        )
    )
    return tests
